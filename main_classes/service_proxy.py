from main_classes.database_security_proxy import DatabaseSecurityProxy
from flask import Flask, jsonify, request
from utilities.response import Response
from utilities.note_classes import Note, Task
class Service():
    def __init__(self):
        ##boilerplate
        self.db_access = DatabaseSecurityProxy("database.db")
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
            token = data.get("token")
            rez = self.db_access.delete_user(username, token)
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
            tags = data.get("tags")
            category = data.get("category")
            content = data.get("content")
            rez = self.db_access.new_note(username, token, Note(title, tags, category, content))
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
            tags = data.get("tags")
            category = data.get("category")
            content = data.get("content")
            note_id = data.get("note_id")
            rez = self.db_access.update_note(username, token, Note(title, tags, category, content), note_id)
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
        ##tasks handling
        @self.app.route('/api/tasks/new', methods = ['POST'])
        def new_task():
            data = request.get_json()
            username = data.get("username")
            token = data.get("token")
            title  = data.get("title")
            tags = data.get("tags")
            category = data.get("category")
            content = data.get("content")
            priority = data.get("priority")
            deadline = data.get("deadline")
            rez = self.db_access.new_task(username, token, Task(title, tags, category, content, priority, deadline))
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
            tags = data.get("tags")
            category = data.get("category")
            content = data.get("content")
            priority = data.get("priority")
            deadline = data.get("deadline")
            task_id = data.get("task_id")
            rez = self.db_access.update_task(username, token, Task(title, tags, category, content, priority, deadline), task_id)   
            return jsonify({"status": rez.status, "message": rez.operation_message, "data": rez.data_bundle}), rez.http_response
