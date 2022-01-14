import zmq
import time
import json

ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)
sock.bind("tcp://*:4321")

print("Starting loop...")
i = 1
while True:
    msg = json.dumps({"message":"ana_aux_pulse","cort_id":"F_1_Outside","name": str(i) + "Testing","index":i})
    sock.send_string(msg)
    print("Sent string: %s ..." % msg)
    i += 1
    if i > 8: i = 1
    time.sleep(0.2)

sock.close()
ctx.term()