from django.urls import path

from .views import (HomePage, TodoView, TodoCategoryView, TodoCategoryCreateView, TodoCreateView, TodoDetailView,
                    TodoUpdateView, TodoDeleteView, TodoCategoryDetailView, TodoCategoryUpdateView, TodoCategoryDeleteView)
from . import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('', HomePage.as_view(), name='home'),
    path('tasks/', TodoView.as_view(), name='tasks'),
    path('create/todo/', TodoCreateView.as_view(), name='todo_create'),
    path('tasks/<int:pk>/', TodoDetailView.as_view(), name='todo_detail'),
    path('tasks/<int:pk>/edit/', TodoUpdateView.as_view(), name='todo_edit'),
    path('tasks/<int:pk>/delete/', TodoDeleteView.as_view(), name='todo_delete'),
    path('tasks/completed/', views.completed_tasks, name='completed_tasks'),
    path('complete/<int:task_id>', views.complete, name='complete'),
    path('complete_task/<int:task_id>',
         views.complete_task, name='complete_task'),
    path('important/<int:task_id>', views.set_important, name='important'),
    path('categories/', TodoCategoryView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.categoryDetail, name='category_detail'),
    path('categories/<int:pk>/edit/',
         TodoCategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/',
         TodoCategoryDeleteView.as_view(), name='category_delete'),
    path('create/todo_category/', TodoCategoryCreateView.as_view(),
         name='todo_category_create'),
]
