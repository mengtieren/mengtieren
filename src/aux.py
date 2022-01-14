import time
import zmq
import os
import json
from multiprocessing import Process, Queue
from pyftdi.gpio import (GpioAsyncController)


NUM_SSR_OUTPUTS = 8
DEFAULT_DURATION = 1


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

    def change_output_mode(self, timer_mode, duration = DEFAULT_DURATION, invert_output = 0):
        self.timer_mode = timer_mode
        self.duration = duration
        self.invert_output = invert_output

    def check(self):
        if self.timer_mode:
            if self.state:
                life = time.time() - self.set_time 
                #print ("life, duration: ", life, self.duration)
                if life >= self.duration:
                    print ("resetting")
                    self.state = False
        return self.state ^ self.invert_output 


def recv_messages(msg_q):
    #  Wait for next request from client
    address_pub_logic = os.environ.get('SERVER_PUB_LOGIC_CONNECT_URI')

    while True:
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect(address_pub_logic)
        socket.subscribe("")
        print("Waiting for msg from: ", address_pub_logic)
        message = socket.recv()
        #print("Recieved msg from logic ...")
        msg_q.put(json.loads(message))

# def send_status(_socket, inputs):
#     status_msg = {
#         "message": "aux_status",
#         "inputs": inputs
#     }
#     print ("sending status message: \n", status_msg)
#     _socket.send_string(json.dumps(status_msg)) 

def main(ssr_bank, opto_bank):

    print ("in Aux")
    msg_q = Queue()
    msg_proc = Process(target=recv_messages, args=(msg_q, ), daemon = True)
    msg_proc.start()

    aux_board_present = False

    while aux_board_present == False:
        try:
            ssr_bank.configure("ftdi:///2", direction=0xFF, frequency=1e3, initial=0x0)
            opto_bank.configure("ftdi:///3", direction=0x00, frequency=1e3, initial=0x0)
            aux_board_present = True
        except:
            print (time.time(), "No Aux board connected")
            time.sleep(1)



    outputs = []
    for i in range (NUM_SSR_OUTPUTS):
        outputs.append(Output())
    message_type = os.environ.get("AUX_PULSE_MESSAGE")
    while(1):
        if msg_q.qsize() > 0:
            
            message = msg_q.get()
            if message["message"] == message_type:
                print (message)
                char0 = message["name"][0]
                if char0 in ["1","2","3","4","5","6","7","8"]:
                    print("setting output", char0)
                    outputs[int(char0)-1].set()

          
            

                

        
        outputs_total = 0
        for i in range(len(outputs)):
            outputs_total += (2**i)*outputs[i].check()
            ssr_bank.write(outputs_total)
        
        #inputs = opto_bank.read()
        #send_status(socket, inputs)

if __name__ == '__main__':
    print ("Aux running")
    ssr_bank = GpioAsyncController()
    opto_bank = GpioAsyncController()
    try: 
        main(ssr_bank, opto_bank)
    except KeyboardInterrupt:
        ssr_bank.close()
        opto_bank.close()
        print ("\nExiting Aux")

