######
# Activity 2.01: Populate the database with an example and write a query displaying the
# list of tasks associated with a given project.
######

from projects.models import Project, Task
from datetime import date

project = Project.objects.create(
    name="Get Good",
    description="Sprints and tasks so you can `get good` in Python.",
    key="GG",
)

Task.objects.create(
    title="Read book 'Expert Python Programming'",
    project=project,
    completed=True,
)

Task.objects.create(
    title="Read book 'Object Oriented Programming in Python'",
    project=project,
)

Task.objects.create(
    title="Read book 'Expert Object Oriented Programming in Python'", project=project
)

Task.objects.create(
    title="Create TopAnswers clone using Django and HTMX",
    details="We might be able to integrate this with the API created using FastAPI ",
    due_date=date(2021, 11, 1),
    priority="!!!",
    project=project,
)

Task.objects.create(
    title="Create API for TopAnswers using FastAPI",
    details="We might be able to integrate this with our Django app",
    due_date=date(2021, 11, 1),
    priority="!!!",
    project=project,
)

##############
# Query for all tasks in a project
##############

tasks = project.task_set.all()
