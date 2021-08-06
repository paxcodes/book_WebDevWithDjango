from django.db import models

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    creation_time = models.DateTimeField(auto_now_add=True)
    key = models.CharField(
        max_length=5, help_text="Unique project code; Usually the acronym of the name."
    )

    def __str__(self):
        return self.name


class Task(models.Model):
    class TaskPriority(models.TextChoices):
        LOW = "!", "Low"
        MEDIUM = "!!", "Medium"
        HIGH = "!!!", "HIGH"

    title = models.CharField(max_length=200)
    details = models.CharField(null=True, max_length=1000)
    due_date = models.DateField(null=True)
    completed = models.BooleanField(default=False, help_text="Task completion status")
    priority = models.CharField(
        choices=TaskPriority.choices, max_length=20, default=TaskPriority.LOW
    )

    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
