from django.shortcuts import render
from .models import Note
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import NoteSerializer

# Create your views here.
# In here safe means we can send more data then just json. safe dont'work with response it work with only json
@api_view(['GET','POST'])
def getRoutes(request):
    routes = [
        {
            "header":"headers",
            "Description":"loerm ipsum "
        },
        {
            "header":"headers2",
            "Description":"loerm ipsum2"
        }
    ]
    return Response(routes)  






@api_view(['GET'])
# many means we can serialize more data 
def getNotes(request):
    notes  = Note.objects.all().order_by('-updated')
    serializer = NoteSerializer(notes,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getNote(request,pk):
    notes = Note.objects.get(id=pk)
    serializer  = NoteSerializer(notes,many=False)
    return Response(serializer.data)

@api_view(['POST'])
def createNote(request):
    data = request.data
    note  = Note.objects.create(
        body = data['body']
    )
    serializer = NoteSerializer(note,many=False)

    # if serializer.is_valid():
    #     serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
def updateNote(request,pk):
    data = request.data
    note = Note.objects.get(id=pk)
    serializer = NoteSerializer(instance=note,data=data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
def deleteNote(request,pk):
    note = Note.objects.get(id=pk)
    note.delete()
    return Response('Not was deleted')