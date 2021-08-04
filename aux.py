
# LOGIC = REQ
# AUX = REP

import time
import zmq
import json
import Jetson.GPIO as GPIO
# Pin Definitions
output_pin = 18  # BOARD pin 12, BCM pin 18
def recv_message(_socket):

    #  Wait for next request from client

    print("Waiting for msg from logic...")
    message = _socket.recv()
    print("Recieved msg from logic ...")
    message_json = json.loads(message)

    #  Send reply back to client
    _socket.send_string("OK") 
    return message_json

def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5004")
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
    while(1):
        message_json = recv_message(socket)
        if message_json["alarm"] == "activated":
            print ("ALARM")
            GPIO.output(output_pin, GPIO.LOW)
        else: 
            GPIO.output(output_pin, GPIO.HIGH)
            print("ALARM DEACTIVATED")
if __name__ == '__main__':
    try: 
        main()
    except KeyboardInterrupt:
        print ("\nexiting")
        GPIO.output(output_pin, GPIO.HIGH)

## in a .vscode folder place following: 
# {
    #"python.pythonPath": "/usr/bin/python"
#}
