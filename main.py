import sys
project_home = '/home/logan667/mysite'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path
    
from main_classes import Service
service = Service()
##for localhost testing uncomment this:
application = service.app.run(debug=True)
##for server (like pythonanywhere) uncomment this:
# application = service.app
