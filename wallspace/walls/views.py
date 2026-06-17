import random
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Wall, WallMember
from .forms import WallForm
from notes.forms import NoteForm
from notes.models import Note

# for api 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from notes.serializers import NoteSerializer
from .serializers import WallSerializer, WallMemberSerializer, InviteMemberSerializer
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
    ).exclude(
        owner=request.user
    )

    context={
        'owned_walls':owned_walls,
        'shared_walls':shared_walls,
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
    member = WallMember.objects.filter(
        wall=wall,
        user=request.user
    ).first()

    is_member = member is not None

    can_edit = is_owner or (
        member and
        member.role == "editor"
    )

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
        if not can_edit:
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
            note.width = 220
            note.height = 120
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
    'is_owner': is_owner,
    'can_edit': can_edit,
    'members': WallMember.objects.filter(
            wall=wall
            ).exclude(
            user=wall.owner
            )
    }

    return render(
        request,
        'walls/wall_detail.html',
        context
    )

@login_required
def delete_wall(request, pk):

    wall = get_object_or_404(
        Wall,
        pk=pk,
        owner=request.user
    )

    if request.method == "POST":

        wall.delete()

        return redirect(
            "home"
        )

    return redirect(
        "wall-detail",
        pk=pk
    )

@login_required
def remove_member(
    request,
    wall_id,
    member_id
):

    wall = get_object_or_404(
        Wall,
        id=wall_id,
        owner=request.user
    )

    member = get_object_or_404(
        WallMember,
        id=member_id,
        wall=wall
    )

    member.delete()

    return redirect(
        'wall-detail',
        pk=wall.id
    )


@login_required
def toggle_role(
    request,
    wall_id,
    member_id
):

    wall = get_object_or_404(
        Wall,
        id=wall_id,
        owner=request.user
    )

    member = get_object_or_404(
        WallMember,
        id=member_id,
        wall=wall
    )

    if member.role == "viewer":

        member.role = "editor"

    else:

        member.role = "viewer"

    member.save()

    return redirect(
        'wall-detail',
        pk=wall.id
    )

@login_required
def rename_wall(request, pk):
    wall = get_object_or_404(Wall, pk=pk, owner=request.user)
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            wall.title = title
            wall.save()
    return redirect("home")



class WallListAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        owned_walls = Wall.objects.filter(
            owner=request.user
        )

        shared_walls = Wall.objects.filter(
            members__user=request.user
        ).exclude(
            owner=request.user
        )

        serializer_owned = WallSerializer(
            owned_walls,
            many=True
        )

        serializer_shared = WallSerializer(
            shared_walls,
            many=True
        )

        return Response({
            "owned_walls":
                serializer_owned.data,

            "shared_walls":
                serializer_shared.data
        })


class CreateWallAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = WallSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                owner=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
class WallDetailAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):

        wall = get_object_or_404(
            Wall,
            pk=pk
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

        is_member = (
            member is not None
        )

        can_edit = (
            is_owner or (
                member and
                member.role == "editor"
            )
        )

        if (
            not is_owner
            and
            not is_member
        ):
            return Response(
                {
                    "error":
                    "Access denied"
                },
                status=403
            )

        wall_serializer = (
            WallSerializer(wall)
        )

        member_serializer = (
            WallMemberSerializer(
                WallMember.objects.filter(
                    wall=wall
                ),
                many=True
            )
        )
        notes_serializer = NoteSerializer(
            wall.notes.all(),
            many=True
        )

        return Response({
            "wall":
                wall_serializer.data,

            "is_owner":
                is_owner,

            "can_edit":
                can_edit,

            "members":
                member_serializer.data,

            "notes":
                notes_serializer.data
        })
    
class UpdateWallAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        wall = get_object_or_404(
            Wall,
            pk=pk,
            owner=request.user
        )

        serializer = WallSerializer(
            wall,
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
    
class DeleteWallAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):

        wall = get_object_or_404(
            Wall,
            pk=pk,
            owner=request.user
        )

        wall.delete()

        return Response(
            {
                "message":
                "Wall deleted successfully"
            },
            status=status.HTTP_200_OK
        )
    
class InviteMemberAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):

        wall = get_object_or_404(
            Wall,
            pk=pk
        )

        # Only owner can invite
        if wall.owner != request.user:

            return Response(
                {
                    "error":
                    "Only owner can invite members"
                },
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = InviteMemberSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        username = serializer.validated_data[
            'username'
        ]

        role = serializer.validated_data[
            'role'
        ]

        try:

            User.objects.get(
                username=username
            )

            member, created = (
                WallMember.objects.get_or_create(
                    wall=wall,
                    user=username,
                    defaults={
                        'role': role
                    }
                )
            )

            if not created:

                return Response(
                    {
                        "message":
                        "User already a member"
                    },
                    status=status.HTTP_200_OK
                )

            return Response(
                {
                    "message":
                    "Member invited successfully"
                },
                status=status.HTTP_201_CREATED
            )

        except User.DoesNotExist:

            return Response(
                {
                    "error":
                    "User not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )
# class WallListCreateAPIView(APIView):

#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         owned_walls = Wall.objects.filter(
#             owner=request.user
#         )

#         shared_walls = Wall.objects.filter(
#             members__user=request.user
#         ).exclude(
#             owner=request.user
#         )

#         serializer_owned = WallSerializer(
#             owned_walls,
#             many=True
#         )

#         serializer_shared = WallSerializer(
#             shared_walls,
#             many=True
#         )

#         return Response({
#             "owned_walls":
#                 serializer_owned.data,

#             "shared_walls":
#                 serializer_shared.data
#         })

#     def post(self, request):

#         serializer = WallSerializer(
#             data=request.data
#         )

#         if serializer.is_valid():

#             serializer.save(
#                 owner=request.user
#             )

#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )