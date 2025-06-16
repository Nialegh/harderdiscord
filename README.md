Discord bot that connects to local Intiface server and broadcasts local BLE advertisements so as to activate haptic feedback devices in response to discord channel keywords and commands.

Requirements from pip:
discord

app/ 
  This folder contains application code (and will contain the .env file once it is created during the setup process)
config/
  This folder contains app config information, currently one json config is present to set action keywords and commands, and their corresponding haptic feedback responses
vendor/
  This folder contains a helper program compiled exe and its source in the src/ folder. It's in c# and should be compiled with .NET 8.0 target using any preferred method (it's very simple)
  The helper program takes command line int params as duration and strength, and turns on the Intiface haptic feedback available actuators with those params
  This is automatically detected and run as needed on the python side where orchestration happens, no user interface is needed directly. 
  A compiled binary is already provided and will work on most systems, if needed the src/ folder can be used to recompile on a target machine

Setup:
  Ensure if you are using secure feedback devices that you have Intiface Central installed on your machine
  Ensure your haptic feedback devices are either available and turned on (promiscious) or that the Intiface server is running and is connected to your devices (secure)
  
  Configure commands and actions in config folder json
  Configure discord auth key in new app/.env file as DISCORD_SECRET=<value>
      The discord auth key is retrieved from discord dev portal, where a corresponding new application space is being configured for this same bot. My key is not in the repo for security purposes
      To get a new Discord bot api key :: Log into Discord Dev Portal, navigate to New Program and follow the steps, navigate to New Bot and follow the steps, 
                                                   navigate to the Build-A-Bot widget and there you can retrieve or reset your bot api key.
  
  Run with python app/readmessages.py
  Test by sending keywords to the linked Discord channel and confirming that the bot and haptic feedback devices react -- 
    the bot will output a lot of messages related to discord actions and haptic feedback devices and on success cases there should be no errors 

Software is exceptionally experimental -- subject to change though I'll try to keep the working versions and documentation here
