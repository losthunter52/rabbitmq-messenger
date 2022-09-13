from django.urls import path
from . import views

#Generic
urlpatterns = [
    path('', views.auth, name='auth'),
    path('checkauth', views.checkauth, name='checkauth'),
    path('getcontacts', views.getContacts, name='getcontacts'),
    path('getgroups', views.getGroups, name='getgroups'),
    path('sendg', views.sendGroupMessage, name='sendg'),
    path('sendc', views.sendContactMessage, name='sendc'),
    path('getmessagescontact/<int:pk>/', views.getContactMessages, name='getmessagescontact'),
    path('getmessagesgroup/<int:pk>/', views.getGroupMessages, name='getmessagesgroup'),
    path('home/<str:name>/', views.home, name='home'),
]

#Contact Conversation
urlpatterns += [
    path('contacts/<str:name>/add', views.addContact, name='addcontact'),
    path('contacts/<str:name>/<int:pk>', views.contactConversation, name='chatcontact'),
]

#Group Conversation
urlpatterns += [
    path('groups/<str:name>/add', views.addGroup, name='addgroup'),
    path('groups/<str:name>/<int:pk>', views.groupConversation, name='chatgroup'),
]
