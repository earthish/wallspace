from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Wall
from .forms import WallForm
# Create your views here.

@login_required #decorator, it checks automatically if a certain condition is satisfied or not
def home(request):
    if request.method=='POST':
        # 1. Grab the submitted data and stuff it into the form template
        form=WallForm(request.POST)
        # 2. Make sure the data follows the rules (e.g., character lengths, not empty)
        if form.is_valid():

            # 3. The magic trick: Pause saving to the database
            wall = form.save(commit=False)
            # 4. Manually assign the owner column to the logged-in user
            wall.owner= request.user
            # 5. Now, officially commit it to the database
            wall.save()
            # 6. Clear the page and reload to prevent duplicate submissions
            return redirect('home')
    
    else:
        # If they are just looking at the page, give them a blank, empty form
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