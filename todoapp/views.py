from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django import forms
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
import requests
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import TodoCategory, Todo
from django.db.models import Q
from .forms import TodoForm

# Create your views here.
""" HomePage """


class HomePage(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = {
            'current_tasks': Todo.objects.order_by('-pk')[:5],
            'latest_categories': TodoCategory.objects.order_by('-pk')[:5],
        }
        return render(request, self.template_name, context)


""" TodoCategory Logic Views  """


class TodoCategoryView(LoginRequiredMixin, ListView):
    template_name = 'categories.html'
    context_object_name = "categories"
    login_url = 'login'

    def get_queryset(self):
        return TodoCategory.objects.filter(author=self.request.user)


class TodoCategoryCreateView(LoginRequiredMixin, CreateView):
    model = TodoCategory
    template_name = 'update/category_new.html'
    fields = ('name',)
    login_url = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TodoCategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = TodoCategory
    template_name = 'update/category_delete.html'
    login_url = 'login'
    success_url = reverse_lazy('categories')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class TodoCategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = TodoCategory
    template_name = 'update/category_edit.html'
    login_url = 'login'
    fields = ("name",)

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class TodoCategoryDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = TodoCategory
    login_url = 'login'
    template_name = 'category_detail.html'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


@login_required
def categoryDetail(request, pk):
    category = get_object_or_404(TodoCategory, pk=pk)
    todos = Todo.objects.filter(category=category).all()
    return render(request, 'category_detail.html', {'category': category, 'todos': todos})


""" Todo Logic Views  """


class TodoView(LoginRequiredMixin,  ListView):
    template_name = 'tasks.html'
    login_url = 'login'
    context_object_name = "tasks"

    def get_queryset(self):
        return Todo.objects.filter(author=self.request.user)


@login_required()
def completed_tasks(request):
    tasks = Todo.objects.order_by('-id').filter(completed=True)

    context = {
        'tasks': tasks
    }
    return render(request, 'todo_complete.html', context)


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'update/todo_new.html'
    login_url = 'login'
    form_class = TodoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TodoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Todo
    template_name = 'update/todo_edit.html'
    login_url = 'login'
    form_class = TodoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        obj = self.get_object()

        return obj.author == self.request.user


class TodoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Todo
    template_name = 'update/todo_delete.html'
    login_url = 'login'
    success_url = reverse_lazy('tasks')

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class TodoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Todo
    template_name = 'todo_detail.html'
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


@login_required()
def complete(request, task_id):
    task = get_object_or_404(Todo, pk=task_id, author=request.user)
    if request.method == 'POST':
        task.completed_date = timezone.now()
        task.save()
        messages.success(request, "Task completed.")
        return redirect('tasks')


@login_required()
def complete_task(request, task_id):
    task = get_object_or_404(Todo, pk=task_id, author=request.user)

    if not task.completed:
        task.completed_date = timezone.now()
        task.completed = True
        task.save()
        messages.success(request, "Task completed.")
        return redirect('tasks')
    else:
        task.completed = False
        task.save()
        messages.success(request, "Task set incomplete.")
        return redirect('tasks')


@login_required()
def set_important(request, task_id):
    task = get_object_or_404(Todo, pk=task_id, author=request.user)

    if not task.priority:
        task.priority = True
        task.save()
        messages.success(request, "Task set as important.")
        return redirect('tasks')
    else:
        task.priority = False
        task.save()
        messages.info(request, 'Task set as unimportant.')
        return redirect('tasks')


def home(request):
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)

    if search is None or search == "top":
        # get the top news
        url = "https://newsapi.org/v2/top-headlines?country={}&page={}&apiKey={}".format(
            "us", 1, settings.APIKEY
        )
    else:
        # get the search query request
        url = "https://newsapi.org/v2/everything?q={}&sortBy={}&page={}&apiKey={}".format(
            search, "popularity", page, settings.APIKEY
        )
    r = requests.get(url=url)

    data = r.json()
    if data["status"] != "ok":
        return HttpResponse("<h1>Request Failed</h1>")
    data = data["articles"]
    context = {
        "success": True,
        "data": [],
        "search": search
    }
    # seprating the necessary data
    for i in data[:10]:
        context["data"].append({
            "title": i["title"],
            "description":  "" if i["description"] is None else i["description"],
            "url": i["url"],
            "image": i["urlToImage"],
            "publishedat": i["publishedAt"]
        })
    # send the news feed to template in context
    return render(request, 'home.html', context=context)
