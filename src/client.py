
import zmq
import time
import json
from datetime import datetime  as dt


def send_message(socket, message_dict):  
    now = dt.now()
    message_dict["timestamp"] = now.strftime("%H:%M:%S")
    message_json = json.dumps(message_dict)
    print ("Sending: ", message_json)
    #  Send reply back to client
    socket.send_string(message_json)
    response = socket.recv()
    return response

def main():
    context = zmq.Context()

    #  Socket to talk to Aux
    print("Connecting to Aux...")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    message_dict = {"message" :"security_state_aux",
        "arm" : "activated",
        "alarm" : "activated",
        "timestamp" : ""}   

    while (1):
        send_message(socket, message_dict)
        time.sleep(1)

if __name__ == '__main__':
    main()



