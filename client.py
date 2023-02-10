import socket
import threading
from server_info import ServerInfo


class Client:
    
    def __init__(self):
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((ServerInfo.HOST, ServerInfo.PORT))
        
    def __send(self) -> None:
        """
        Send message to the server
        OPTIONS:
            #[name] - send message to specific client
            ... soon ...
        """
        while True:
            message = input("")            
            self.__client.send(message.encode(ServerInfo.ENCODER))
            
    def __receive(self) -> None:
        """Receive incoming message from the server"""
        while True:
            try:
                message = self.__client.recv(ServerInfo.BYTESIZE) 
                if message == "Hello! Say your name: ":
                    # send client name
                    name = input(message.decode(ServerInfo.ENCODER))
                    self.__client.send(name)
                else:
                    # print message
                    print(message.decode(ServerInfo.ENCODER))
            except socket.error:
                print("An error...")
                self.__client.close()
                
                
    def run(self) -> None:
        send_thread = threading.Thread(target=self.__send)
        receive_thread = threading.Thread(target=self.__receive)
        
        send_thread.start()
        receive_thread.start()
        


client = Client()
client.run()