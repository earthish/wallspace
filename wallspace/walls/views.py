import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Wall, WallMember
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

    owned_walls = Wall.objects.filter(
        owner=request.user
    )
    shared_walls = Wall.objects.filter(
    members__user=request.user
    )
    walls = (
        owned_walls | shared_walls
    ).distinct()

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
        pk=pk,
    )
    is_owner = (
        wall.owner == request.user
    )
    is_member = WallMember.objects.filter(
        wall=wall,
        user=request.user
    ).exists()

    if not is_owner and not is_member:
        return redirect("home")

    notes = wall.notes.all()

    if request.method == 'POST':

        # Invite member logic
        if "invite_member" in request.POST:

            username = request.POST.get(
                "username"
            )

            role = request.POST.get(
                "role"
            )

            try:

                user = User.objects.get(
                    username=username
                )

                WallMember.objects.get_or_create(
                    wall=wall,
                    user=user,
                    defaults={
                        "role": role
                    }
                )

            except User.DoesNotExist:
                pass

            return redirect(
                'wall-detail',
                pk=wall.pk
            )

        # Add note logic
        form = NoteForm(request.POST)

        if form.is_valid():

            note = form.save(
                commit=False
            )

            note.wall = wall
            note.creator = request.user
            note.x_position = random.randint(50, 600)
            note.y_position = random.randint(50, 400)
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
    'notes': wall.notes.all(),
    'is_owner': is_owner
    }

    return render(
        request,
        'walls/wall_detail.html',
        context
    )   