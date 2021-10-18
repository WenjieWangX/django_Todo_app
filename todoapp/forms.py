from django.forms import ModelForm
from todoapp.models import Todo, TodoCategory


class TodoForm(ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TodoForm,self).__init__(*args, **kwargs)
        self.fields['category'].queryset = TodoCategory.objects.filter(author=user)
    class Meta:
        model = Todo
        fields = ("title", "description", "completed_date",
                  "priority", "completed", "category",)
