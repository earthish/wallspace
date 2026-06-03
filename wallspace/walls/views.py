from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .models import Wall
from .forms import WallForm
from notes.forms import NoteForm
from notes.models import Note
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

@login_required
def wall_detail(request, pk):

    wall = get_object_or_404(
        Wall,
        pk=pk
    )
    if request.method == 'POST':

        form = NoteForm(request.POST)

        if form.is_valid():

            note = form.save(
                commit=False
            )

            note.wall = wall
            note.creator = request.user

            note.save()

            return redirect(
                'wall-detail',
                pk=wall.pk
            )

    else:

        form = NoteForm()

    context = {
        'wall': wall,
        'form': form,
    }

    return render(
        request,
        'walls/wall_detail.html',
        context
    )   