from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Wall
from .forms import WallForm
# Create your views here.

@login_required #decorator, it checks automatically if a certain condition is satisfied or not
def home(request):
    if request.method=='POST':
        form=WallForm(request.POST)

        if form.is_valid():
            wall = form.save(commit=False)
            wall.owner= request.user
            wall.save()

            return redirect('home')
    
    else:
        form = WallForm()

    walls = Wall.objects.filter(
        owner=request.user
    )

    context={
        'walls':walls,
        'form':form
    }

    return render(
        request, 'walls/home.html', context

    )