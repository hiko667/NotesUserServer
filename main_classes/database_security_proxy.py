import sqlite3
from utilities import Note, DatabaseException, Response, Task
from main_classes.database_access import DatabaseAccess

class DatabaseSecurityProxy():
    def __init__(self, database_name):
        self.database_access = DatabaseAccess(database_name)
        self.connection = sqlite3.connect(database_name, check_same_thread=False)
        self.messenger = self.connection.cursor()

    def verify_token(self, username, token)->bool: 
        self.messenger.execute("SELECT token FROM users WHERE username=?", (username,))
        res = self.messenger.fetchone()
        return False if res == None else bool(token == res[0])
        
    def user_exists(self, username)->bool:
        self.messenger.execute("SELECT COUNT (*) FROM users WHERE username = ?", (username, ))
        res = self.messenger.fetchone()
        return False if res == None else bool(res[0] == 1)
        
    def get_user_id(self, username)->int:
        self.messenger.execute("SELECT id FROM users WHERE username = ?", (username, ))
        return int(self.messenger.fetchone()[0])
    
    def verify_access(self, username, token):
        if not username or not token:
            raise DatabaseException("One of the following was not given: username, token", 400)
        elif not self.user_exists(username):
            raise DatabaseException(f"Can not find user: {username}", 404)
        elif not self.verify_token(username, token):
            raise DatabaseException("Wrong or damaged token", 401)
        
    #user handling
    def new_user(self, username, password)->Response:
        try:
            if not username or not password:
                raise DatabaseException("One of the following was not given: username, password", 400)
            if self.user_exists(username):
                raise DatabaseException(f"User {username} already exists", 400)

            return self.database_access.new_user(username, password)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)

    def verify_user(self, username, password)->Response:
        try:
            if not username or not password:
                raise DatabaseException("One of the following was not given: username, password", 400)
            self.messenger.execute("SELECT username, password FROM users WHERE username = ?", (username,))
            res = self.messenger.fetchone()
            if res == None:
                raise DatabaseException(f"Can not find user: {username}", 404)
            else:
                if password == res[1]:
                    return self.database_access.verify_user(username, password)
                else:
                    raise DatabaseException("Wrong password", 401)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)
    def update_password(self, username, token, new_password)->Response:
        try:
            self.verify_access(username, token)
            return self.database_access.update_password(username, token, new_password) 
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)
    def delete_user(self, username, token)->Response:
        try:
            self.verify_access(username, token)
            return self.database_access.delete_user(username, token)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)

    ##the fetch function
    def fetch_content(self, username, token)->Response:
        try:
            self.verify_access(username, token)
            return self.database_access.fetch_content(username, token)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)
    #note handling
    def new_note(self, username, token, newnote : Note)->Response:
        try:
            self.verify_access(username, token)
            return self.database_access.new_note(username, token, newnote)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)
    def delete_note(self, username, token, note_id)->Response:
        try:
            self.verify_access(username, token)
            return self.database_access.delete_note(username, token, note_id)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)
    def update_note(self, username, token, newnote : Note, note_id)->Response:
        try:
            self.verify_access(username, token)
            return self.database_access.delete_note(username, token, newnote, note_id)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)
    ##tasks handling
    def new_task(self, username, token, newtask: Task)->Response:
        try:
            self.verify_access(username, token)
            return self.database_access.new_task(username, token, newtask)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)
    def delete_task(self, username, token, task_id)->Response:
        try:
            self.verify_access(username, token)
            return self.database_access.delete_task(username, token, task_id)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)
    def update_task(self, username, token, newtask:Task, task_id):
        try:
            self.verify_access(username, token)
            return self.database_access.update_task(username, token, newtask, task_id)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)