from django.urls import path
from . import views

urlpatterns = [
    path('',views.profiles,name='profiles'),
    path('user-profile/<str:pk>/',views.user_profile,name='user-profile'),

    path('login/',views.login_user,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/',views.logout_user,name='logout'),

    path('my-account/',views.my_account,name='my-account'),
    path('edit-account/',views.edit_account,name='edit-account'),

    path('create-skill',views.create_skill,name='create-skill'),
    path('update-skill/<str:pk>',views.update_skill,name='update-skill'),
    path('delete-skill/<str:pk>',views.delete_skill,name='delete-skill'),

    path('inbox/',views.inbox,name='inbox'),
    path('message/<str:pk>/',views.view_message,name='message'),
    path('send-message/<str:pk>/',views.send_message,name='send-message')
]
