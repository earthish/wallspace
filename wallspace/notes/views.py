from django.shortcuts import render
from django.http import JsonResponse
from .models import Note
import json
# Create your views here.

def update_position(request):
    if request.method=='POST':

        data = json.loads(
            request.body
        )

        note = Note.objects.get(
            id=data['note_id']
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
