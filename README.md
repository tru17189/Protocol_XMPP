# XMPP protocol in practice

This repository includes a functional program that manages the XMPP's protocol with too many functionalities
for make differents actions like send a message or register a user into a server. Below in this readme 
You will Read the description of all the scripts and how to execute the project correctly.

# DESCRIPTIONS:

  -main.py (The principal program, this script imports the others also uses them to make a program that has different functionalities
  all these functionalities are describing into the menu of the program, this program also has a client that has some definitions that are other functionalities, for example send a friend request).

  -login_send_message.py (this script has 4 different classes, these classes are functionalities for main.py, the functionalities are
  send message to a specific user, print the list of contacts, remove a user of you list friends, and consults the status of a 
  specific user).
  
  -register.py (This script has the functionality of register a new user into the server).
  
  -room.py (This script has the functionality of creating a new room or join a new room, also has a presence message).

# FUNTIONALITIES:
  
    All the next functionalities that will be described, are the functionalities of you can use when run the project.
    - Send a message to someone specific/Mandar Mensaje a alguien en especifico (Send a personal message to some other
    contact, you need have a destination and a message)  
    - Friends list online/Lista de amigos conectados (Show you a list of your online friends)
    - Remove a contact/Eliminar a un contacto (Write the contact of you want remove of your list friends)
    - See the status of an user/Ver el estado de un usuario (Check if any contact is online or not, the contact you write has to be your friend to see something)
    - Create a room - Join room/Crear una sala - Unirse a una sala ya existente (If you want create a new room just write a new name room or if you want join a room just write a name of a room that already exist)
    - Send friend request/Mandar solicitud de amistad (Do you want a new friend? well just say it with this functionality, remember you need have a destination)
    - Send pressence message/Mandar mensaje de presencia (Say hello of everybody with presence message, and of course if a hello is not enough for you change message here too)
    -  Show all server's user/Mostrar a todos los usuarios del servidor (Show you a list of all the users into the server redes2020.xyz)
    - Close session/Cerrar Sesion (Time for a rest? let's do it here)
  
# HOW TO RUN:
    Follow the commands below (just run the first command in case something goes wrong, because it is an error that does not show up on all computers):

    1. pip uninstall pyasn1 peas-modules sleekxmpp
    2. pip install pyasn1==0.3.6 pyasn1-modules==0.1.5 
    3. pip install sleekxmpp==1.3.3
    4. python main.py
    
This project was built in Python 3.7.3
