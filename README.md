# Aux
To use clone the repo, enter the Aux directory and run "docker-compose up" to run in the foreground where it will output to the console and "docker-compose up -d" to run in the background.

The Logic will send an security_state_aux message. Aux will react based on the System_state field. Currently hardoced to set or reset SSR_OUT_0 on the aux board dependant on security_state_aux message. The default output is 0. If the intention is to activate the alarm, the SSR_OUT_0 set to 1 for 2 seconds and then returned to 0. This SSR output is used to short the panic button input of the Paradox Alarm panel to ground, which triggers the alarm.

The Aux will respond with aux_status message.




