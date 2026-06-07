from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Note
import json
from walls.models import WallMember
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def update_position(request):
    if request.method=='POST':

        data = json.loads(
            request.body
        )

        note = get_object_or_404(
            Note,
            id=data['note_id']
        )
        wall=note.wall
        is_owner = (
            wall.owner == request.user
        )
        member = WallMember.objects.filter(
            wall=wall,
            user=request.user
        ).first()

        can_edit = is_owner or (
            member and
            member.role == "editor"
        )

        if not can_edit:
                return JsonResponse(
                    {
                        'error':
                        'Invalid request'
                    },
                    status=400
                )

            


        note.x_position = data['x']
        note.y_position = data['y']

        note.save()
        return JsonResponse({
            'status': 'success'
        })
    return JsonResponse({
        'status':'error'
    })

@login_required
def delete_note(
    request,
    note_id
):

    note = get_object_or_404(
        Note,
        id=note_id
    )

    wall = note.wall

    is_owner = (
        wall.owner == request.user
    )

    member = WallMember.objects.filter(
        wall=wall,
        user=request.user
    ).first()

    can_edit = is_owner or (
        member and
        member.role == "editor"
    )

    if not can_edit:

        return redirect(
            'wall-detail',
            pk=wall.id
        )

    note.delete()

    return redirect(
        'wall-detail',
        pk=wall.id
    )