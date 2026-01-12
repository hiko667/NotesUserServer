import sqlite3
from utilities import Note, DatabaseException, Response, Task
from time import time

class DatabaseAccess():
    def __init__(self, database_name):
        self.connection = sqlite3.connect(database_name, check_same_thread=False)
        self.messenger = self.connection.cursor()
        self.messenger.execute("""CREATE TABLE IF NOT EXISTS users (
                               id INTEGER PRIMARY KEY, 
                               username TEXT NOT NULL, 
                               password TEXT NOT NULL, 
                               token TEXT NOT NULL);""")
        self.messenger.execute("""
                               CREATE TABLE IF NOT EXISTS notes(
                               note_id INTEGER PRIMARY KEY, 
                               user_id INTEGER, 
                               title TEXT,
                               tags TEXT, 
                               category TEXT, 
                               content TEXT, 
                               FOREIGN KEY(user_id) 
                               REFERENCES users(id));""")
        self.messenger.execute("""
                               CREATE TABLE IF NOT EXISTS tasks(
                               task_id INTEGER PRIMARY KEY, 
                               user_id INTEGER, 
                               title TEXT,
                               tags TEXT, 
                               category TEXT, 
                               content TEXT, 
                               priority TEXT,
                               deadline TEXT,
                               FOREIGN KEY(user_id) 
                               REFERENCES users(id));""")
        self.connection.commit()
        #baza danych innit
    #funckje użytkowe
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
            self.messenger.execute("SELECT id FROM users ORDER BY rowid DESC LIMIT 1")
            temp = self.messenger.fetchone()
            new_id =  0 if temp is None else int(temp[0]) + 1 
            new_token = str(int(time()*10000)) + username
            self.messenger.execute("SELECT id FROM users WHERE id = ?", (new_id, ))
            if self.messenger.fetchone() == None:
                self.messenger.execute(f"INSERT INTO users (id, username, password, token) VALUES (?, ?, ?, ?)", (new_id, username, password, new_token))
            else:
                raise DatabaseException("Something went wrong", 400)
            self.connection.commit()
            return Response(True, 201, "Account created successfully", None)
        except DatabaseException as e:
            return Response(False, e.code, e.content, None)
        except Exception as e:
            return Response(False, 400, f"Unhandled error: {e}", None)
    def verify_user(self, username, password)->Response:
        self.messenger.execute("SELECT username, token FROM users WHERE username = ?", (username,))
        res = self.messenger.fetchone()
        return Response(True, 200, "Correct password", {"username": username, "token": res[1]})
    def update_password(self, username, token, new_password)->Response:
        self.messenger.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username, ))
        self.connection.commit()
        return Response(True, 202, "Password updated", None)
    
    def delete_user(self, username, token)->Response:
        id = self.get_user_id(username)
        self.messenger.execute("DELETE FROM users WHERE username = ?", (username, ))
        self.messenger.execute("DELETE FROM notes WHERE user_id = ?", (id, ))
        self.messenger.execute("DELETE FROM tasks WHERE user_id = ?", (id, ))
        self.connection.commit()
        return Response(True, 202, "Account deleted", None)
    ##the fetch function
    def fetch_content(self, username, token)->Response:
        user_id = self.get_user_id(username)
        self.messenger.execute("SELECT * FROM notes WHERE user_id = ?", (user_id, ))
        notes = self.messenger.fetchall()
        if notes is not None:
            notes_package = [
                {
                    "note_id": n[0],
                    "title" : n[2],
                    "tags": n[3].split(";") if n[3] else [],
                    "category": n[4],
                    "content": n[5]
                }
                for n in notes
            ]
        else: 
            notes_package = None
        self.messenger.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id, ))
        tasks = self.messenger.fetchall()
        if tasks is not None:
            tasks_package = [
                {
                    "task_id" : t[0],
                    "title" : t[2],
                    "tags": t[3].split(";") if t[3] else [],
                    "category": t[4],
                    "content": t[5],
                    "priority": t[6],
                    "deadline": t[7]
                }
                for t in tasks
            ]
        else:
            tasks_package = None
        res = {"notes" : notes_package, "tasks" : tasks_package}
        return Response(True, 200, "Fetched notes and tasks succesfully", res)
    #note handling
    def new_note(self, username, token, newnote : Note)->Response:
            user_id = self.get_user_id(username)
            self.messenger.execute("SELECT note_id FROM notes ORDER BY rowid DESC LIMIT 1")
            temp = self.messenger.fetchone()
            new_id =  0 if temp is None else int(temp[0]) + 1
            self.messenger.execute("INSERT INTO notes (note_id, user_id, title, tags, category, content) VALUES (?, ?, ?, ?, ?, ?)", (new_id, user_id, newnote.title, newnote.tagsToString(), newnote.category, newnote.content))
            self.connection.commit()
            return Response(True, 201, "Note created successfully", {"id" : new_id})

    def delete_note(self, username, token, note_id)->Response:
        self.messenger.execute("SELECT user_id FROM notes WHERE note_id = ?", (note_id))
        target_note = self.messenger.fetchone()
        if target_note == None:
            raise DatabaseException("Note by selected id does not exist", 404)
        if target_note[0] != self.get_user_id(username):
            raise DatabaseException("Client error: sent id of note that does not belong to you. Notify server handler", 401)
        self.messenger.execute("DELETE FROM notes WHERE note_id = ?", (note_id, ))
        self.connection.commit()
        return Response(True, 202, "Deleted successfully", None)
    def update_note(self, username, token, newnote : Note, note_id)->Response:
        self.messenger.execute("SELECT user_id FROM notes WHERE note_id = ?", (note_id))
        target_note = self.messenger.fetchone()
        if target_note == None:
            raise DatabaseException("Note by selected id does not exist", 404)
        if target_note[0] != self.get_user_id(username):
            raise DatabaseException("Client error: sent id of note that does not belong to you. Notify server handler", 401)
        self.messenger.execute("UPDATE notes SET title = ?, tags = ?, category = ?, content = ? WHERE note_id = ?", (newnote.title, newnote.tagsToString(), newnote.category, newnote.content, note_id) )
        self.connection.commit()
        return Response(True, 200, "Note updated successfully", None)
    ##tasks handling
    def new_task(self, username, token, newtask: Task)->Response:
        user_id = self.get_user_id(username)
        self.messenger.execute("SELECT task_id FROM tasks ORDER BY rowid DESC LIMIT 1")
        temp = self.messenger.fetchone()
        new_id =  0 if temp is None else int(temp[0]) + 1
        self.messenger.execute("INSERT INTO tasks (task_id, user_id, title, tags, category, content, priority, deadline) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (new_id, user_id, newtask.title, newtask.tagsToString(), newtask.category, newtask.content, newtask.priority, newtask.deadline))
        self.connection.commit()
        return Response(True, 201, "Task created successfully", {"id" : new_id})
    def delete_task(self, username, token, task_id)->Response:
        self.messenger.execute("SELECT user_id FROM tasks WHERE task_id = ?", (task_id,))
        target_task = self.messenger.fetchone()
        if target_task == None:
            raise DatabaseException("Note by selected id does not exist", 404)
        if target_task[0] != self.get_user_id(username):
            raise DatabaseException("Client error: sent id of task that does not belong to you. Notify server handler", 401)
        self.messenger.execute("DELETE FROM tasks WHERE task_id = ?", (task_id, ))
        self.connection.commit()
        return Response(True, 202, "Deleted successfully", None)
    def update_task(self, username, token, newtask:Task, task_id):
        self.messenger.execute("SELECT user_id FROM tasks WHERE task_id = ?", (task_id,))
        target_task = self.messenger.fetchone()
        if target_task == None:
            raise DatabaseException("Note by selected id does not exist", 404)
        if target_task[0] != self.get_user_id(username):
            raise DatabaseException("Client error: sent id of task that does not belong to you. Notify server handler", 401)
        self.messenger.execute("UPDATE tasks SET title = ?, tags = ?, category = ?, content = ?, priority = ?, deadline = ? WHERE task_id = ?", (newtask.title, newtask.tagsToString(), newtask.category, newtask.content, newtask.priority, newtask.deadline, task_id) )
        self.connection.commit()
        return Response(True, 200, "Task updated successfully", None)