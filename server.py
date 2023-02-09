import socket
import threading
import sys

from server_info import ServerInfo


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
        
    def __broadcast(self, message: str) -> None:
        """Send message to all clients"""
        flag = True
        for client in self.__client_socket_list:
            try:
                client.send(message.encode(ServerInfo.ENCODER))
            except socket.error:
                flag = False
                index = self.__client_socket_list.index(client)
                name = self.__client_name_list[index]
                print(f"Message has not been sent to {name}!!\n\n")
        if flag: print("INFO: Message has been sent to all clients!\n\n")
        
    def __connect_new_client(self) -> None:
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
                client_thred = threading.Thread(target=self.__receive_message, args=(client,))
                client_thred.start()
                
    def __receive_message(self, client: socket.socket) -> None:
        """Receive message from clients and then forward them to broadcast function"""
        # get client info
        index = self.__client_socket_list.index(client)
        name = self.__client_name_list[index]
        while True:
            try:
                # receive single message
                message = client.rcv(ServerInfo.BYTESIZE).decode(ServerInfo.ENCODER)
                message = f"{name}: {message}"
                self.__broadcast(message)    
            except:
                # something is no yes :D :D
                message = f"Unfortunately {name} has been thrown out from the room!!"
                self.__broadcast(message)
                
                # remove client from client lists
                self.__client_name_list.remove(name)
                self.__client_socket_list.remove(client)
                
                client.close()    
                break            
        
    def __single_message(self, client_dest: str, message: str, sender: socket.socket | str = "admin" ) -> None:
        """Send message to single client"""
        if sender == "admin":
            """Message send if error with sending single message by client"""
            pass
        else:
            """Message from one client to other"""
            index = self.__client_name_list.index(client_dest)
            client = self.__client_socket_list[index]
            index_sen = self.__client_socket_list.index(sender)
            sender_name = self.__client_name_list[index_sen]
            message = f"[{sender_name}]: {message}".encode(ServerInfo.ENCODER)
            client.send(message)
        
    def run(self):
        """Start the server"""
        print("Server is starting...\n\n")
        self.__connect_new_client()
        

def main() -> None:
    server = Server()
    server.run()
    

if __name__ == "__main__":
    main()
                