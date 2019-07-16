from django.urls import path
from . import views
urlpatterns=[
    path('test/',views.index,name='index'),
    path('getCommentByUUID/',views.getCommentByUUID,name='getCommentByUUID'),
    path('index/',views.indexhtml,name='indexhtml'),
    path('commenthtml/',views.commenthtml,name='commenthtml')
]