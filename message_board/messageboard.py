from ezmpncgame import EZMPNCApplication
from datetime import datetime

class MessageBoard(EZMPNCApplication):
    ##
    # Decorators
    def preprocess_request(fn):
        def preprocess_request_wrapper(self, request):
            request = [unstripped_index.strip() for unstripped_index in request.split('|')]
            if len(request) == 0 or request[0] == '':
                return self.toplevel_str()
            else:
                return fn(self, request)
        return preprocess_request_wrapper
    
    ##
    # Magic functions
    def __init__(self):
        self.threads = list()
        self.messages = dict()
    
    ##
    # Overloaded functions
    @preprocess_request
    def process_request(self, request: str) -> str:
        if len(request) >= 2:
            thread, message = request[0], request[1]
            self.post(thread, message)
            return self.thread_str(thread)
        elif len(request) == 1:
            thread = request[0]
            if request[0] not in self.threads:
                self.threads.append(thread)
                self.messages[thread] = list()
                self.post(thread, 'Thread created.')
            return self.thread_str(thread)
        elif len(request) == 0:
            return self.toplevel_str()
            
    ##
    #
    def post(self, thread: str, message: str) -> None:
        post_msg = f'{datetime.now().strftime("%H:%M:%S")} - {message}'
        self.messages[thread].append(post_msg)
    
    def toplevel_str(self) -> str:
        resp = 'Threads:\n'
        for thread in self.threads:
            resp += f'{thread}\n'
        return resp
    
    def thread_str(self, thread: str) -> str:
        resp = f'Contents of \'{thread}\':\n'
        for message in self.messages[thread]:
            resp += f'{message}\n'
        return resp