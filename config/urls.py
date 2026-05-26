from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from assistant.views import (
    home,
    dashboard,
    tasks,
    analytics,
    settings as user_settings,
    user_login,
    register,
    user_logout,
    task_detail,
    update_status,
    ai_api
)

urlpatterns = [

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        home,
        name='home'
    ),

    path(
        'dashboard/',
        dashboard,
        name='dashboard'
    ),

    path(
        'tasks/',
        tasks,
        name='tasks'
    ),

    path(
        'analytics/',
        analytics,
        name='analytics'
    ),

    path(
        'settings/',
        user_settings,
        name='settings'
    ),

    path(
        'login/',
        user_login,
        name='login'
    ),

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'logout/',
        user_logout,
        name='logout'
    ),

    path(
        'task/<int:task_id>/',
        task_detail,
        name='task_detail'
    ),

    path(
        'update-status/<int:id>/',
        update_status,
        name='update_status'
    ),

    path(
        'api/ai/',
        ai_api,
        name='ai_api'
    )
]

if settings.DEBUG:

    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )