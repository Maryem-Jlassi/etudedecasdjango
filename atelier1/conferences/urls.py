from django.urls import path
from .views import *

urlpatterns=[
         path('list/',conferenceList,name='listeconf'),
         path('listViewConference/',ConferenceListView.as_view(), name="listeViewconf"),
         path('details/<int:pk>/',DetailViewConference.as_view(),name="DetailConf")


]