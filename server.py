import socket
import threading
import sys

from server_info import ServerInfo
from validators import name_validate


class Server:
    
    def __init__(self) -> None:
        try:
            self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__server.bind((ServerInfo.HOST, ServerInfo.PORT))
            self.__server.listen()
        except socket.error:
            print("Sorry. Server has not been created!\n\n")
            sys.exit(1)
        self.__client_name_list = []
        self.__client_socket_list = []
        
        
    def __broadcast(self, message: str, sender: socket.socket = None) -> None:
        """Send message to all clients"""
        flag = True
        for client in self.__client_socket_list:
            if client != sender:
                try:
                    client.send(message.encode(ServerInfo.ENCODER))
                except socket.error:
                    flag = False
                    index = self.__client_socket_list.index(client)
                    name = self.__client_name_list[index]
                    print(f"Message has not been sent to {name}!!\n\n")
        
        for cl in self.__client_name_list:
            print(cl)
        
        if flag: print("INFO: Message has been sent to all clients!\n\n")
      
        
    def __connect(self) -> None:
        """Connect new client and check if room is full"""
        while True:
            client, _ = self.__server.accept()
            if len(self.__client_socket_list) >= 8:
                """Send message to client it is imposible to connect because room is full"""
                message = "Sorry, but chat room is nowfull. Try again later.".encode(ServerInfo.ENCODER)
                # error handling hear is redundant - client is no connect
                client.send(message)
                client.close()
            else:
                """Welcome new client on server"""
                print("New client connected!\n\n")
                # aquisition of information about new client
                try:
                    client.send("Hello! Say your name: ".encode(ServerInfo.ENCODER))
                    client_name = client.recv(ServerInfo.BYTESIZE).decode(ServerInfo.ENCODER)
                except socket.error:
                    print("Error with adding new client\n\n")
                    client.close()
                    continue
                             
                # append client info to client lists
                self.__client_name_list.append(client_name)
                self.__client_socket_list.append(client)
                
                # welcome new client: individual, server, all
                client.send(f"Thanks! You've connected to the room!".encode(ServerInfo.ENCODER))
                print(f"{client_name} has joined to the room")
                self.__broadcast(f"{client_name} has joined the chat")
                
                # start new thread for receive messages for every new client
                client_thred = threading.Thread(target=self.__receive, args=(client,))
                client_thred.start()
            
                
    def __receive(self, client: socket.socket) -> None:
        """Receive message from clients and then forward them to broadcast function"""
        # get client info
        index = self.__client_socket_list.index(client)
        sender = self.__client_name_list[index]
        while True:
            try:
                # receive single message
                message = client.recv(ServerInfo.BYTESIZE).decode(ServerInfo.ENCODER)
                # TODO  options!! 
                # OPTIONS:
                # #[name] - send message to specific client,
                # #[list] - print lists of users
                # #[color <color>] - change color of messages (class for user?)
                # soon :D
                single, name = name_validate(message, self.__client_name_list) 
                if single:
                    self.__private(name, message, sender)
                else:
                    message = f"{sender}: {message}"
                    self.__broadcast(message, client)    
            except socket.error:
                # something is no yes :D :D
                message = f"Unfortunately {sender} has been thrown out from the room!!"
                self.__broadcast(message, client)
                
                # remove client from client lists
                self.__client_name_list.remove(sender)
                self.__client_socket_list.remove(client)
                
                client.close()    
                break            
      
        
    def __private(self, client_name: str, message: str, sender: str = "admin" ) -> None:
        """Send message to single client"""
        if sender == "admin":
            """Message send if error with sending single message by client"""
            pass
        else:
            """Message from one client to other"""
            index = self.__client_name_list.index(client_name)
            client = self.__client_socket_list[index]
            # delete  #[name] from message
            message = message[message.index(']'):] 
            message = f"[{sender} sent]: {message}".encode(ServerInfo.ENCODER)
            client.send(message)
        
        
    def run(self):
        """Start the server"""
        print("Server is starting...\n\n")
        self.__connect()
        

def main() -> None:
    server = Server()
    server.run()
    

if __name__ == "__main__":
    main()
                