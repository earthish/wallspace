from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

#for api
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

# Create your views here.



def register(request):

    if request.method == 'POST':

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'login'
            )

    else:

        form = UserCreationForm()

    return render(
        request,
        'users/register.html',
        {'form': form}
    )

class RegisterAPIView(APIView):

    permission_classes = []

    def post(self, request):
        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "status": "success",
                    "message": "User registered successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )