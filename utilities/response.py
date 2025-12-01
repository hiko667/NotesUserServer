class Response():
    def __init__(self, operation_success, http_response, operation_message, data_bundle):
        self.status = "success" if operation_success else "error"
        self.http_response = http_response
        self.operation_message = operation_message
        self.data_bundle = data_bundle