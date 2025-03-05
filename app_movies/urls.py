from django.urls import path, include
from app_movies import views
from app_movies.views import CommentDetail, CommentListApiView
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, ActorViewSet, CommentViewSet, MovieList
from .views import MovieList, MovieDetail
from app_movies.views import MovieDetail

app_name = "app_movies"


router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'comments', CommentViewSet)
\

urlpatterns = [
    path('<int:pk>/', MovieDetail.as_view(), name='movie_detail'),
]


urlpatterns = [
    path('', include(router.urls)),
    path("",views.MovieList.as_view(),name="movie_list"),
    path('', MovieList.as_view(), name='movie_list'),
    path('', views.movie_list, name='movie_list'),
    
    path('<int:pk>/', MovieDetail.as_view(), name='movie_detail'),
    path('<int:pk>/', views.MovieDetail.as_view(), name='movie_detail'),
   
    path("actor/",views.ActorList.as_view(),name="actor_list"),
    path("actor/<int:pk>/",views.ActorDetail.as_view(),name="actor_detail"),

    path('<int:movie_id>/comments/', CommentListApiView.as_view(), name='movie-comments-list'),
    path('comments/<int:pk>/', CommentDetail.as_view(), name='movie-comments-detail'),
]
