# XMPP protocol in practice

This repository includes a functional program that manages the XMPP's protocol with too many tools
for make differents actions like send a message or register a user into a server. Below in this readme 
You will Read the description of all the scripts and how to execute the project correctly.

DESCRIPTIONS:

  -main.py (The principal program, this script imports the others also uses them to make a program that has different tools
  all these tools are describing into the menu of the program).

  -login_send_message.py (this script has 4 different classes, these classes are functionalities for main.py, the functionalities are
  send message to a specific user, print the list of contacts, remove a user of you list friends, and consults the status of a 
  specific user).
  
  -register.py (This script has the functionality of register a new user into the server).
  
  -room.py (This script has the functionality of creating a new room or join a new room, also has a presence message).
  
  HOW TO RUN:
  
    For run this project just runs the main.py file of the next way:
    python main.py
    
This project was built in Python 3.7.3
