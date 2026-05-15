from django.urls import path
from . import views

urlpatterns = [
    path('api/ai/', views.ai_api, name='ai_api'),   # FIXED
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('task/<int:task_id>/', views.task_detail, name='task_detail'),
]



# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('dashboard/', views.dashboard, name='dashboard'),
#     path('task/<int:task_id>/', views.task_detail, name='task_detail'),
#     path('api/ai/', views.ai_api),
# ]