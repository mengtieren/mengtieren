#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import json
import Jetson.GPIO as GPIO

# Pin Definitions
output_pin = 18  # BOARD pin 12, BCM pin 18




def recv_message(_socket):
    #  Wait for next request from client
    message = _socket.recv()
    message_json = json.loads(message)
    #  Send reply back to client
    _socket.send_string("OK")
    return message_json


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
    while(1):
        message_json = recv_message(socket)
        print (message_json["timestamp"])

        if message_json["alarm"] == "activated":
            print ("ALARM")
            GPIO.output(output_pin, GPIO.LOW)
        else: GPIO.output(output_pin, GPIO.HIGH)
        time.sleep(5)



if __name__ == '__main__':
    main()