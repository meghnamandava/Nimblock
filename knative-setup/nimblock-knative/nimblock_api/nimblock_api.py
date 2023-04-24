from flask import Flask, request, jsonify
import subprocess
import socket
import os
import sys
import json
import select
import time

HOST = '192.17.102.15'
PORT = 8000

app = Flask(__name__)
app.config['PER_REQUEST_TIMEOUT'] = 300

@app.route("/", methods=["POST"])
def custom_function():
    # Get function code from the request
    function_code = request.get_data()
    # Write function code to a file
    #with open('/tmp/function.py', 'wb') as f:
    #    f.write(function_code)

    # Execute function using Python subprocess module
    #result = subprocess.check_output(['python', '/tmp/function.py'])

    # Return result as JSON
    #response = {'result': result.decode('utf-8')}
    response = send_to_nimblock(function_code)
    #return jsonify(response)
    return response


def send_to_nimblock(json_data):
    start_time = time.time()
    fpga_host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    fpga_host_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    fpga_host_socket.connect((HOST, PORT))
    fpga_host_socket.settimeout(600)
    """
    json_data = {
        'app': in_app,
        'batch': in_batch,
        'priority': in_priority,
    }
    """
    print("Connected to socket")
    #client_socket.send(json.dumps(json_data).encode('utf-8'))
    fpga_host_socket.send(json_data)
    #sockets = [fpga_host_socket]
    #while True:
    #    readable, writable, in_error = select.select(sockets, [], [])
    #    if len(readable) != 0:
    while True:
        response = fpga_host_socket.recv(1024)
        if len(response) > 1:
            end_time = time.time()
            break
    fpga_host_socket.close()
    response = str(response) + "Dest: FPGA" + ", Start time: " + str(start_time) + ", End time: " + str(end_time) + "\n"
    return response



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

    


