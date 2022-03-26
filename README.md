# Aux
To use clone the repo, enter the Aux directory and run "docker-compose up" to run in the foreground where it will output to the console and "docker-compose up -d" to run in the background.

Currently set to receive ana_aux_pulse messages from Analytics. Need  to change these to Logic at some point

The output will toggle according to the  1st character of the  "name" field of the ana_aaux_pulse. i.e. if name is "1_home", then SSR output 1 is triggered. ote that there it is set to a maximum of 8 outputs.

Not set to respod to inputs from the optoisolators