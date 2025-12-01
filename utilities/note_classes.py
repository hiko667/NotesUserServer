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