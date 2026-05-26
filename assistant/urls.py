from django.urls import path
from . import views


urlpatterns=[

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'tasks/',
        views.tasks,
        name='tasks'
    ),

    path(
        'analytics/',
        views.analytics,
        name='analytics'
    ),

    path(
        'settings/',
        views.settings,
        name='settings'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'task/<int:task_id>/',
        views.task_detail,
        name='task_detail'
    ),

    path(
        'update-status/<int:id>/',
        views.update_status,
        name='update_status'
    ),

    path(
        'api/ai/',
        views.ai_api,
        name='ai_api'
    )

]