from cmath import phase
from django.http import HttpResponse
from django.shortcuts import render,redirect
import paho.mqtt.client as mqtt
from mqttApp.mqtt_example import connect_Mqtt
from threading import Thread
from .forms import UserCreationForm,NewUserForm
from django.contrib import messages
from django.contrib.auth import login as auth_login, authenticate
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
import redis
import redis
from datetime import datetime
import waitress
from mqttApp.mqtt_example import r
import json
# Create your views here.

def register(request):
    t=Thread(target=connect_Mqtt)
    t.start()
    print('started')
    form=NewUserForm()
    if request.method=='POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(login)
        else:
            return render(request,'index.html',{"form":form})
    else:
        return render(request,'index.html',{"form":form})

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(details)
            else:
                return render(request=request, template_name="login.html", context={"login_form":form})
        else:
            return render(request=request, template_name="login.html", context={"login_form":form})
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"login_form":form})



@login_required
def details(request):
    keys=set()
    for key in r.scan_iter("GPM*"):
    # delete the key
        keys.add(key.decode('utf8'))
    length=len(keys)
    return render(request,'details.html',{'keys':keys})

@login_required
def deviceDetails(request,id,name):
    context=json.loads(r.get(id).decode('utf8'))
    meter_address=context['meter_address']
    device_name=name
    frequency=context['frequency']
    phase_current=context['phase_current']
    voltage=context['voltage']
    print(context['meter_address'])
    return render(request,'deviceDetails.html',{'meter_address':meter_address,'device_name':device_name
    ,'frequency':frequency,'phase_current':phase_current,'voltage':voltage})
