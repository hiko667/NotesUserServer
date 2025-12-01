class DatabaseException(Exception):
    def __init__(self, content, code):
        self.content = content
        self.code = code