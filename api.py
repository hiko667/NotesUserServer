from flask import Flask, request, jsonify
import sqlite3
import time

class response():
    def __init__(self, operation_success, http_response, operation_message, data_bundle):
        self.status = "success" if operation_success else "error"
        self.http_response = http_response
        self.operation_message = operation_message
        self.data_bundle = data_bundle

class databaseException(Exception):
    def __init__(self, content, code):
        self.content = content
        self.code = code

class note():
    def __init__(self, title, tags, category, content):
        self.title = title
        self.tags = tags
        self.category = category
        self.content = content
    def tagsToString(self):
        if self.tags == None:
            return None
        return ";".join(self.tags)
class task(note):
    def __init__(self, title, tags, category, content, priority, deadline):
        super().__init__(title, tags, category, content)
        self.deadline = deadline
        self.priority = priority

class database_access():
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
            raise databaseException("One of the following was not given: username, token", 400)
        elif not self.user_exists(username):
            raise databaseException(f"Can not find user: {username}", 404)
        elif not self.verify_token(username, token):
            raise databaseException("Wrong or damaged token", 401)
        
    #user handling
    def new_user(self, username, password)->response:
        try:
            if not username or not password:
                raise databaseException("One of the following was not given: username, password", 400)
            if self.user_exists(username):
                raise databaseException(f"User {username} already exists", 400)
            self.messenger.execute("SELECT id FROM users ORDER BY rowid DESC LIMIT 1")
            temp = self.messenger.fetchone()
            new_id =  0 if temp is None else int(temp[0]) + 1 
            print("alan")
            new_token = str(int(time.time()*10000)) + username
            # print(new_id, new_token, username, password)
            self.messenger.execute("SELECT id FROM users WHERE id = ?", (new_id, ))
            if self.messenger.fetchone() == None:
                self.messenger.execute(f"INSERT INTO users (id, username, password, token) VALUES (?, ?, ?, ?)", (new_id, username, password, new_token))
            self.connection.commit()
            return response(True, 201, "Account created successfully", None)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
    
      
    def verify_user(self, username, password)->response:
        try: 
            if not username or not password:
                raise databaseException("One of the following was not given: username, password", 400)
            self.messenger.execute("SELECT username, password, token FROM users WHERE username = ?", (username,))
            res = self.messenger.fetchone()
            if res == None:
                raise databaseException(f"Can not find user: {username}", 404)
            else:
                if password == res[1]:
                    return response(True, 200, "Correct password", {"username": username, "token": res[2]})
                else:
                    raise databaseException("Wrong password", 401)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)

    def update_password(self, username, token, new_password)->response:
        try:
            self.verify_access(username, token)
            self.messenger.execute("UPDATE users SET password = ? WHERE username = ?", (new_password, username, ))
            self.connection.commit()
            return response(True, 202, "Password updated", None)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
        
        
    def delete_user(self, username, password, token)->response:
        try:
            if not username or not password or not token:
                raise databaseException("One of the following was not given: username, password, token", 400)
            res = self.verify_user(username, password)
            if res.status == "error":
                return res
            elif res.data_bundle["token"] == token:
                id = self.get_user_id(username)
                self.messenger.execute("DELETE FROM users WHERE username = ?", (username, ))
                self.messenger.execute("DELETE FROM notes WHERE user_id = ?", (id, ))
                self.messenger.execute("DELETE FROM tasks WHERE user_id = ?", (id, ))
                self.connection.commit()
                return response(True, 202, "Account deleted", None)
            else:
                raise databaseException("Wrong or damaged token", 401)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandleda error: {e}", None)
        
    ##the fetch function
    def fetch_content(self, username, token)->response:
        try:
            self.verify_access(username, token)
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
            return response(True, 200, "Fetched notes and tasks succesfully", res)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
        
    #note handling
    def new_note(self, username, token, newnote : note)->response:
        try:
            self.verify_access(username, token)
            user_id = self.get_user_id(username)
            self.messenger.execute("SELECT note_id FROM notes ORDER BY rowid DESC LIMIT 1")
            temp = self.messenger.fetchone()
            new_id =  0 if temp is None else int(temp[0]) + 1
            self.messenger.execute("INSERT INTO notes (note_id, user_id, title, tags, category, content) VALUES (?, ?, ?, ?, ?, ?)", (new_id, user_id, newnote.title, newnote.tagsToString(), newnote.category, newnote.content))
            self.connection.commit()
            return response(True, 201, "Note created successfully", None)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
    
    def delete_note(self, username, token, note_id)->response:
        try:
            self.verify_access(username, token)
            self.messenger.execute("DELETE FROM notes WHERE note_id = ?", (note_id, ))
            self.connection.commit()
            return response(True, 202, "Deleted successfully", None)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
    def update_note(self, username, token, newnote : note, note_id)->response:
        try:
            self.verify_access(username, token)
            self.messenger.execute("UPDATE notes SET title = ?, tags = ?, category = ?, content = ? WHERE note_id = ?", (newnote.title, newnote.tagsToString(), newnote.category, newnote.content, note_id) )
            self.connection.commit()
            return response(True, 200, "Note updated successfully", None)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
    ##tasks handling
    def new_task(self, username, token, newtask: task)->response:
        try:
            self.verify_access(username, token)
            user_id = self.get_user_id(username)
            self.messenger.execute("SELECT task_id FROM tasks ORDER BY rowid DESC LIMIT 1")
            temp = self.messenger.fetchone()
            new_id =  0 if temp is None else int(temp[0]) + 1
            self.messenger.execute("INSERT INTO tasks (task_id, user_id, title, tags, category, content, priority, deadline) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (new_id, user_id, newtask.title, newtask.tagsToString(), newtask.category, newtask.content, newtask.priority, newtask.deadline))
            self.connection.commit()
            return response(True, 201, "Task created successfully", None)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
    def delete_task(self, username, token, task_id)->response:
        try:
            self.verify_access(username, token)
            self.messenger.execute("DELETE FROM tasks WHERE task_id = ?", (task_id, ))
            self.connection.commit()
            return response(True, 202, "Deleted successfully", None)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)
    def update_task(self, username, token, newtask:task, task_id):
        try:
            self.verify_access(username, token)
            self.messenger.execute("UPDATE tasks SET title = ?, tags = ?, category = ?, content = ?, priority = ?, deadline = ? WHERE task_id = ?", (newtask.title, newtask.tagsToString(), newtask.category, newtask.content, newtask.priority, newtask.deadline, task_id) )
            self.connection.commit()
            return response(True, 200, "Task updated successfully", None)
        except databaseException as e:
            return response(False, e.code, e.content, None)
        except Exception as e:
            return response(False, 400, f"Unhandled error: {e}", None)  

class service_proxy():
    def __init__(self):
        ##boilerplate
        self.db_access = database_access("database.db")
        self.app = Flask(__name__)
        @self.app.route('/')
        def home():
            return "<h1>You should not be here</h1>"
        
        ##user handling
        @self.app.route('/api/user/new', methods = ["POST"])
        def new_user():
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            rez = self.db_access.new_user(username, password)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/user/verify_login', methods = ['POST'])
        def verify_user():
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            rez = self.db_access.verify_user(username, password)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/user/update', methods = ['PATCH'])
        def update_password():
            data = request.get_json()
            username = data.get("username")
            new_password = data.get("new_password")
            token = data.get("token")
            rez = self.db_access.update_password(username, token, new_password)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/user/delete', methods = ['DELETE'])
        def delete_user():
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")
            token = data.get("token")
            rez = self.db_access.delete_user(username, password, token)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/users/fetch', methods = ['POST'])
        def fetch_content():
            data = request.get_json()
            username = data.get("username")
            token = data.get("token")
            rez = self.db_access.fetch_content(username, token)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        
        ##notes handling
        @self.app.route('/api/notes/new', methods = ['POST'])
        def new_note():
            data = request.get_json()
            username = data.get("username")
            token = data.get("token")
            title  = data.get("title")
            tags = (v := data.get("tags")) if v and v.strip() else None
            category = (v := data.get("category")) if v and v.strip() else None
            content = data.get("content")
            rez = self.db_access.new_note(username, token, note(title, tags, category, content))
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        
        @self.app.route('/api/notes/delete', methods = ['DELETE'])
        def delete_note():
            data = request.get_json()
            username = data.get("username")
            token = data.get("token")
            note_id = data.get("note_id")
            rez = self.db_access.delete_note(username, token, note_id)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/notes/update', methods = ['PATCH'])
        def update_note():
            data = request.get_json()
            username = data.get("username")
            token = data.get("token")
            title  = data.get("title")
            tags = (v := data.get("tags")) if v and v.strip() else None
            category = (v := data.get("category")) if v and v.strip() else None
            content = data.get("content")
            note_id = data.get("note_id")
            rez = self.db_access.update_note(username, token, note(title, tags, category, content), note_id)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        ##tasks handling
        @self.app.route('/api/tasks/new', methods = ['POST'])
        def new_task():
            data = request.get_json()
            username = data.get("username")
            token = data.get("token")
            title  = data.get("title")
            tags = (v := data.get("tags")) if v and v.strip() else None
            category = (v := data.get("category")) if v and v.strip() else None
            content = data.get("content") 
            priority = (v := data.get("priority")) if v and v.strip() else None
            deadline = (v := data.get("deadline")) if v and v.strip() else None
            rez = self.db_access.new_task(username, token, task(title, tags, category, content, priority, deadline))
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/tasks/delete', methods = ['DELETE'])
        def delete_task():
            data = request.get_json()
            username = data.get("username")
            token = data.get("token")
            task_id = data.get("task_id")
            rez = self.db_access.delete_task(username, token, task_id)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        @self.app.route('/api/tasks/update', methods = ['PATCH'])
        def update_task():
            data = request.get_json()
            username = data.get("username")
            token = data.get("token")
            title  = data.get("title")
            tags = (v := data.get("tags")) if v and v.strip() else None
            category = (v := data.get("category")) if v and v.strip() else None
            content = data.get("content")
            priority = (v := data.get("priority")) if v and v.strip() else None
            deadline = (v := data.get("deadline")) if v and v.strip() else None
            task_id = data.get("task_id")
            rez = self.db_access.update_task(username, token, task(title, tags, category, content, priority, deadline), task_id)   
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response


if __name__ == '__main__':
    service = service_proxy()
    service.app.run(debug=True)