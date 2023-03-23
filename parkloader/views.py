from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import MyForm,LoginForm, registerForm,ParkingLotForm, BillingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth.decorators import login_required
from django.contrib import messages



# Create your views here.


# def home(request):
#     detail= parkingLoader.objects.last()
#     if request.method == "POST":
#         parking_lot_form = ParkingLotForm(request.POST)
#         form1 = MyForm(request.POST)
#         if form1.is_valid() and parking_lot_form.is_valid():
#            parking_lot = parking_lot_form.save()
#            vehicle = form1.save(commit=False)
#            vehicle.parking_lot = parking_lot
#            vehicle.save()
#     else:
#         form1 = MyForm()
#         parking_lot_form=ParkingLotForm()
#     return render(request, 'home.html', {'form': form1,'parking_lot_form':parking_lot_form,'detail': detail})
def home(request):
    parking_lots = ParkingLot.objects.all()
    parking_lot_choices = [(parking_lot.id, f"{parking_lot.location} ({parking_lot.available_slots} available)") for parking_lot in parking_lots]

    if request.method == 'POST':
        vehicle_form = MyForm(request.POST)
        if vehicle_form.is_valid():
            # Get the parking lot object associated with the selected parking location
            parking_lot = ParkingLot.objects.get(id=request.POST.get('parking_lot'))

            # Check if there are available slots
            if parking_lot.available_slots > 0:
                # Save the vehicle object and reduce the number of available slots
                vehicle = vehicle_form.save(commit=False)
                vehicle.user = request.user  # Add this line to set the user value
                vehicle.parking_lot = parking_lot
                vehicle.save()
                parking_lot.available_slots -= 1
                parking_lot.save()
                return redirect('/home')
            else:
                # Display an error message if there are no available slots
                vehicle_form.add_error('parking_lot', 'There are no available parking slots in this location.')
    else:
        vehicle_form = MyForm(user=request.user)
    return render(request, 'home.html', {'vehicle_form': vehicle_form, 'parking_lot_choices': parking_lot_choices})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        #form = registerForm()
        if form.is_valid(): 
            form.save()
            form1 = AuthenticationForm(request, data=request.POST)
            user = form1.get_user()
            user_plan = Billing.objects.filter(user=user).first()
            if user_plan:
                return redirect('/home')
            else:
                # User doesn't have a plan selected, redirect to the select plan page
                return redirect("/home/billing_info/")    
        else:
            error_message = "Invalid username or password."
            return render(request, 'signUp.html', {'form': form, 'error_message': error_message})  
    else:
        form = registerForm
        return render(request, 'signUp.html', { 'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user_plan = Billing.objects.filter(user=user).first()
            if user_plan:
                return redirect('/home')
            else:
                # User doesn't have a plan selected, redirect to the select plan page
                return redirect("home/billing_info/")
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'form': form, 'error_message': error_message})  
    else:
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form, 'error_message': ""})


def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0795504241'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://darajambili.herokuapp.com/express-payment';
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

def stk_push_callback(request):
        data = request.body
        
        return HttpResponse("STK Push in Django👋")



def billing_info(request):
    billing_basic = BillingPlan.objects.first()
    billing_advance = BillingPlan.objects.all()[1]
    billing_platinum = BillingPlan.objects.last()
    return render(request, 'billing.html', {'billing_basic': billing_basic,'billing_advance': billing_advance,'billing_platinum': billing_platinum})

def billing(request):
    plans = BillingPlan.objects.all()
    user = request.user
    try:
        billing = user.billing
    except Billing.DoesNotExist:
        billing = None

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            if billing is None:
                billing = form.save(commit=False)
                billing.user = user
            else:
                billing.plan = form.cleaned_data['plan']
                billing.card_number = form.cleaned_data['card_number']
                billing.card_expiry = form.cleaned_data['card_expiry']
                billing.cvv = form.cleaned_data['cvv']
            billing.save()
            messages.success(request, 'Billing details successfully updated!')
            return redirect('/home')
    else:
        if billing is None:
            form = BillingForm()
        else:
            form = BillingForm(initial={
                'plan': billing.plan,
                'card_number': billing.card_number,
                'card_expiry': billing.card_expiry,
                'cvv': billing.cvv
            })
        context = {'plans': plans, 'form': form}
        return render(request, 'billingplans.html', context)


@login_required
def plans(request):
    plans = BillingPlan.objects.all()

    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            plan_id = form.cleaned_data['plan']
            request.user.profile.billing_plan = BillingPlan.objects.get(id=plan_id)
            request.user.profile.save()
            messages.success(request, 'Billing plan successfully selected!')
            return redirect('home/')
    else:
        form = BillingForm()

        context = {'plans': plans, 'form': form}
        return render(request, 'plans/plans.html', context)