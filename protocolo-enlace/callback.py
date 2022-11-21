class Callback():
    def __init__(self, serial, tout):
        self.__serial = serial
        self.__tout = tout
        
    def handle(self):
        print('handle')
        ##return super().handle()
    
    def handle_timeout():
         print('Timeout')