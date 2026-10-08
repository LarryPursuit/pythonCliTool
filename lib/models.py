class Task:
    """A single to-do item with a title and a completion status."""

    def __init__(self, title: str) -> None:
        self.title = title
        self.completed = False

    def complete(self) -> None:
        """Mark the task as completed and confirm in the terminal."""
        self.completed = True
        print(f"✅ Task '{self.title}' completed.")


class User:
    """A named user who owns a list of tasks."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        """Attach a task to this user and confirm in the terminal."""
        self.tasks.append(task)
        print(f"📌 Task '{task.title}' added to {self.name}.")

    def get_task_by_title(self, title: str) -> Task | None:
        """Return the first task matching the given title, or None."""
        return next((task for task in self.tasks if task.title == title), None)
