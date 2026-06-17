from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Note
import json
from walls.models import WallMember, Wall
from django.contrib.auth.decorators import login_required

#for api 
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import NoteSerializer

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

@login_required
def edit_note(
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

    if request.method == "POST":

        note.title = request.POST.get(
            "title"
        ).strip()

        note.content = request.POST.get(
            "content"
        ).strip()

        note.color = request.POST.get(
            "color"
        ).strip()

        note.save()

    return redirect(
        'wall-detail',
        pk=wall.id
    )

@login_required
def update_size(request):

    if request.method == "POST":

        data = json.loads(
            request.body
        )

        note = get_object_or_404(
            Note,
            id=data["note_id"]
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

            return JsonResponse(
                {
                    "error":
                    "Permission denied"
                },
                status=403
            )

        note.width = data["width"]
        note.height = data["height"]

        note.save()

        return JsonResponse(
            {
                "status":
                "success"
            }
        )

    return JsonResponse(
        {
            "error":
            "Invalid request"
        },
        status=400
    )
class CreateNoteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        wall_id = request.data.get(
            'wall_id'
        )

        wall = get_object_or_404(
            Wall,
            id=wall_id
        )

        is_owner = (
            wall.owner == request.user
        )

        member = (
            WallMember.objects.filter(
                wall=wall,
                user=request.user
            ).first()
        )

        can_edit = (
            is_owner or (
                member and
                member.role == "editor"
            )
        )

        if not can_edit:

            return Response(
                {
                    "error":
                    "You do not have permission to create notes"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = NoteSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                creator=request.user,
                wall=wall,
                x_position=random.randint(
                    50,
                    600
                ),
                y_position=random.randint(
                    50,
                    400
                ),
                width=220,
                height=120
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class UpdateNoteAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        note = get_object_or_404(
            Note,
            pk=pk
        )

        wall = note.wall

        is_owner = (
            wall.owner == request.user
        )

        member = (
            WallMember.objects.filter(
                wall=wall,
                user=request.user
            ).first()
        )

        can_edit = (
            is_owner or (
                member and
                member.role == "editor"
            )
        )

        if not can_edit:

            return Response(
                {
                    "error":
                    "Permission denied"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = NoteSerializer(
            note,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )