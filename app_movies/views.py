from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, viewsets 
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app_movies.models import Movie

from app_movies.models import Movie, Actor, Comment
from app_movies.permissions import IsAdminOrReadOnly

from rest_framework.decorators import action
from .models import Movie, Actor, Comment
from .serializers import MovieSerializer, ActorSerializer, CommentSerializer
from django.db import models

from django.http import JsonResponse


def movie_list(request):
    return JsonResponse({'movies': []}) 


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    @action(detail=True, methods=['post']) 
    def add_actor(self, request, pk=None):
        movie = self.get_object()
        actor_id = request.data.get('actor_id')

        try:
            actor = Actor.objects.get(id=actor_id)
            movie.actor.add(actor)
            return Response({"message": "Actor added successfully!"}, status=status.HTTP_200_OK)
        except Actor.DoesNotExist:
            return Response({"error": "Actor not found"}, status=status.HTTP_404_NOT_FOUND)



class MovieList(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    
    
class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
     permission_classes = [IsAdminOrReadOnly]
     queryset = Movie.objects.all()
     serializer_class = MovieSerializer


class ActorList(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
     permission_classes = [IsAdminOrReadOnly]
     queryset = Actor.objects.all()
     serializer_class = ActorSerializer
     

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class CommentListApiView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, movie_id):
        comments = Comment.objects.filter(movie__id=movie_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, movie_id):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            movie = Movie.objects.get(id=movie_id)
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
     permission_classes = [IsAdminOrReadOnly,IsAuthenticated]
     serializer_class = CommentSerializer

     def get_queryset(self):
         comment_id = self.kwargs.get('pk')
         return Comment.objects.filter(id=comment_id)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

