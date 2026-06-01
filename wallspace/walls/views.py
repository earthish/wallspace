from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Wall
from .forms import WallForm
# Create your views here.

@login_required 