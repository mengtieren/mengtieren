import time
import zmq
import json
from pyftdi.gpio import (GpioAsyncController)


def recv_message(_socket):

    #  Wait for next request from client

    print("Waiting for msg from logic...")
    message = _socket.recv()

    print("Recieved msg from logic ...")
    message_json = json.loads(message)

    ok_msg = {
        "message": "aux_status",
        "status_code": "ok"
    }

    #  Send reply back to client
    _socket.send_string(json.dumps(ok_msg)) 
    return message_json

def main():
    ssr_bank = GpioAsyncController()
    ssr_bank.configure("ftdi:///2", direction=0xFF, frequency=1e3, initial=0x0)
    opto_bank = GpioAsyncController()
    opto_bank.configure("ftdi:///3", direction=0x00, frequency=1e3, initial=0x0)
    gpio_bank = GpioAsyncController()
    gpio_bank.configure("ftdi:///4", direction=0x00, frequency=1e3, initial=0x0)

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5004")

    while(1):
        message_json = recv_message(socket)

        if message_json["alarm"] == "activated":
            print ("ALARM ACTIVATED")
            ssr_bank.write(0x01) 
            time.sleep(2)
            ssr_bank.write(0x00) 

if __name__ == '__main__':
    try: 
        main()
    except KeyboardInterrupt:
        print ("\nexiting")


## in a .vscode folder place following: 
# {
    #"python.pythonPath": "/usr/bin/python"
#}

