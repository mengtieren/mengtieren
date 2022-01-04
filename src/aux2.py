import time
import zmq
import json
from pyftdi.gpio import (GpioAsyncController)


NUM_SSR_OUTPUTS = 8
DEFAULT_DURATION = 5
AUX_SUB_PORT = 5005

class Output:
    def __init__(self, timer_mode = 1, invert_output = 0, duration = DEFAULT_DURATION):
        self.duration = duration 
        self.set_time = 0
        self.timer_mode = timer_mode
        self.invert_output = invert_output
        self.state = 0

    def set(self):
        if self.timer_mode:
            self.set_time = time.time()
        self.state = 1

    def unset(self):
        self.state = 0

    def change_output_mode(self, timer_mode, duration = 1, invert_output = 0):
        self.timer_mode = timer_mode
        self.duration = duration
        self.invert_output = invert_output

    def check(self):
        if self.timer_mode:
            if self.state:
                if time.time() - self.set_time >= self.duration:
                    self.state = False
        return self.state ^ self.invert_output 


def recv_message(_socket):
    #  Wait for next request from client
    print("Waiting for msg from logic...")
    message = _socket.recv()
    print("Recieved msg from logic ...")
    message_json = json.loads(message)
    return message_json

def send_status(_socket, inputs):
    status_msg = {
        "message": "aux_status",
        "inputs": inputs
    }
    print ("sending status message: \n", status_msg)
    _socket.send_string(json.dumps(status_msg)) 

def main():

    ssr_bank = GpioAsyncController()
    ssr_bank.configure("ftdi:///2", direction=0xFF, frequency=1e3, initial=0x0)
    opto_bank = GpioAsyncController()
    opto_bank.configure("ftdi:///3", direction=0x00, frequency=1e3, initial=0x0)
    gpio_bank = GpioAsyncController()
    gpio_bank.configure("ftdi:///4", direction=0x00, frequency=1e3, initial=0x0)

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:" + str(AUX_SUB_PORT))

    outputs = []
    for i in range (NUM_SSR_OUTPUTS):
        outputs.append(Output())
     
    while(1):
        message_json = recv_message(socket)
        if message_json["message"] == "output_pulse_aux":
            outputs[message_json("output")].set()
        
        outputs_total = 0
        for i in range(len(outputs)):
            outputs_total += (2**i)*outputs[i].check()
            print(outputs_total)
            ssr_bank.write(outputs_total)
        
        send_status(socket, opto_bank.read())

if __name__ == '__main__':
    try: 
        print ("Aux running")
        main()
    except KeyboardInterrupt:
        print ("\nexiting")

