from main_classes import ServiceProxy
if __name__ == '__main__':
    service = ServiceProxy()
    service.app.run(debug=True)