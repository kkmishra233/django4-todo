from rest_framework import generics
from todo.models import Todo
from todo.serializers import TodoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class TodoList(generics.ListCreateAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TodoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class StatusCheck(APIView):
    """
    API endpoint to check the status of the application.
    """
    def get(self, request):
        # You can perform any checks here to determine the status of your application
        # For simplicity, let's just return a success response
        return Response({'status': 'OK'})