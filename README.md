# Aux
To use run "docker-compose up -d"

send an security_state_aux message. Aux will respond with aux_status message

Currently hardwire to set or reset SSR_OUT_0 on the aux board dependant on security_state_aux message. The default output is 0. If the intention is to activate the alarm, the SSR_OUT_0 set to 1 for 2 seconds and then returned to 0. 

Currently the SSR output is used to short the panic button input of the Paradox Alarm panel to ground, which triggers the alarm.


