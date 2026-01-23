class Note():
    def __init__(self, title, tags, category, content):
        self.title = title
        self.tags = tags
        self.category = category
        self.content = content
    def tagsToString(self):
        if self.tags == None:
            return None
        return ";".join(self.tags)
class Task(Note):
    def __init__(self, title, tags, category, content, priority, deadline):
        super().__init__(title, tags, category, content)
        self.deadline = deadline
        self.priority = priority

class ListTask():
    def __init__(self, title, deadline):
        self.title = title
        self.deadline = deadline

class List():
    def __init__(self, title, tags, category, priority):
        self.title = title
        self.tags = tags
        self.category = category
        self.priority = priority
        self.tasks = []
    def __iter__(self):
        return iter(self.tasks)
    def tagsToString(self):
        if self.tags == None:
            return None
        return ";".join(self.tags)
    def add_task(self, task : ListTask):
        self.tasks.append(task)