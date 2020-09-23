from __future__ import absolute_import, unicode_literals

import sys
import os
import logging
import getpass
from optparse import OptionParser

import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout
from sleekxmpp.stanza import StreamFeatures
from sleekxmpp.basexmpp import BaseXMPP
from sleekxmpp.exceptions import XMPPError
from sleekxmpp.xmlstream import XMLStream
from sleekxmpp.xmlstream.matcher import StanzaPath, MatchXPath
from sleekxmpp.xmlstream.handler import Callback
from sleekxmpp.xmlstream.stanzabase import ET, ElementBase

import register 
import login_send_message
import room
# Se configura los dns para evitar problemas. 
try:
    import dns.resolver
except ImportError:
    DNSPYTHON = False
else:
    DNSPYTHON = True

log = logging.getLogger(__name__)

# Esta cclase inica un cliente por si se necesitase sacar
# informacion de aqui. 
class ClientObject(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password,):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start, threaded=True)
        self.add_event_handler('message', self.ReceiveMessage)
        self.add_event_handler("got_online", self.people_online)
        self.add_event_handler("got_offline", self.people_offline)
        self.register_plugin('xep_0030') 
        self.register_plugin('xep_0199')
        self.register_plugin('xep_0045') 
        if self.connect():
            self.process(block=False)
            print("Done")
        else:
            print("Unable to connect.")

    def start(self, event):
        self.send_presence()
        self.get_roster()
        #self.disconnect(wait=True)

    def ReceiveMessage(self, message):
        print(message['from'].user, message['body'])
    
    def people_online(self, notificacion):
        print("Conectados:", notificacion['from'].user)
    
    def people_offline(self, notificacion):
        print("desconectado:", notificacion['from'].user)

    def addUser(self):
        username = input("¿A quien deseas mandar una notificacion?")
        self.send_presence_subscription(pto=username)
    
    def BuildNotification(self, message):
        message = self.Message()
        message['type'] = 'chat'
        message['body'] = message
        message.append(ET.fromstring("<active xmlns='http://jabber.org/protocol/chatstates'/>"))
        y = input("¿Quieres cambiar el mensaje de presencia?[y/n] ")
        lista = self.client_roster.groups()
        print(lista)
        for i in lista:
            message['to'] = i
            try:
                message.send()
            except IqError as e:
                raise Exception("Invalido ", e)
            except IqTimeout:
                raise Exception("El servidor no esta respondiendo")
                
                

# Aqui iniciamos el menu principal el cual te da dos opciones 
# registrarse o inicar sesion, sino se inicia sesion no se tiene 
# a acceso a diferentes herramientas como mandar mensaje o ver 
# la lista de amigos. 
while True:
    print("1. Registrar una nueva cuenta en el servidor.")
    print("2. Iniciar Sesión (Hasta hacer esto no podras realizar\n algunas acciones como mandar mensajes)")
    number = int(input("Escribe el numero de la opcion que deseas: "))
    if number == 1:
        raw_input = input
        if __name__ == '__main__':
            optp = OptionParser()

            optp.add_option('-q', '--quiet', help='set logging to ERROR',
                            action='store_const', dest='loglevel',
                            const=logging.ERROR, default=logging.INFO)
            optp.add_option('-d', '--debug', help='set logging to DEBUG',
                            action='store_const', dest='loglevel',
                            const=logging.DEBUG, default=logging.INFO)
            optp.add_option('-v', '--verbose', help='set logging to COMM',
                            action='store_const', dest='loglevel',
                            const=5, default=logging.INFO)
            
            optp.add_option("-j", "--jid", dest="jid",
                            help="JID to use")
            optp.add_option("-p", "--password", dest="password",
                            help="password to use")

            opts, args = optp.parse_args()

            logging.basicConfig(level=opts.loglevel,
                                format='%(levelname)-8s %(message)s')

            if opts.jid is None:
                opts.jid = raw_input("Username: ")
                print("Este sera tu usuario -> ", opts.jid)
            if opts.password is None:
                opts.password = getpass.getpass("Password: ")
                print("Este sera tu contraseña -> ", opts.password)

            xmpp = register.RegisterBot(opts.jid, opts.password)
            xmpp.register_plugin('xep_0030') # Service Discovery
            xmpp.register_plugin('xep_0004') # Data forms
            xmpp.register_plugin('xep_0066') # Out-of-band Data
            xmpp.register_plugin('xep_0077') # In-band Registration

            if xmpp.connect():
                xmpp.process(block=True)
                print("Done")
            else:
                print("Unable to connect.")
    elif number == 2:
        raw_input = input
        if __name__ == '__main__':
            optp = OptionParser()

            optp.add_option('-q', '--quiet', help='set logging to ERROR',
                            action='store_const', dest='loglevel',
                            const=logging.ERROR, default=logging.INFO)
            optp.add_option('-d', '--debug', help='set logging to DEBUG',
                            action='store_const', dest='loglevel',
                            const=logging.DEBUG, default=logging.INFO)
            optp.add_option('-v', '--verbose', help='set logging to COMM',
                            action='store_const', dest='loglevel',
                            const=5, default=logging.INFO)

            optp.add_option("-j", "--jid", dest="jid",
                            help="JID to use")
            optp.add_option("-p", "--password", dest="password",
                            help="password to use")
            optp.add_option("-t", "--to", dest="to",
                            help="JID to send the message to")
            optp.add_option("-m", "--message", dest="message",
                            help="message to send")

            opts, args = optp.parse_args()

            logging.basicConfig(level=opts.loglevel,
                                format='%(levelname)-8s %(message)s')

            if opts.jid is None:
                opts.jid = raw_input("Username: ")
            if opts.password is None:
                opts.password = getpass.getpass("Contraseña: ")
            print(f"\nQue deseas hacer {opts.jid}")
            while True:
                print("1. Mandar Mensaje a alguien en especifico.")
                print("2. Lista de amigos conectados.")
                print("3. Eliminar a un contacto.")
                print("4. Ver el estado de un usuario.")
                print("5. Crear una sala / Unirse a una sala ya existente. (Editar mensaje de presencia de grupos tambien)")
                print("6. Mandar solicitud de amistad")
                print("7. Mandar mensaje de presencia (Editar tambien)")
                print("8. Cerrar Sesion.")
                ClientObject(opts.jid, opts.password)
                number = int(input("Escribe el numero de la opcion que deseas: \n\n"))
                if number == 1:
                    opts.to = raw_input("\nPara: ")
                    opts.message = raw_input("Mensaje: ")

                    xmpp = login_send_message.SendMsgBot(opts.jid, opts.password, opts.to, opts.message)
                    xmpp.register_plugin('xep_0030') # Service Discovery
                    xmpp.register_plugin('xep_0199') # XMPP Ping

                    if xmpp.connect():
                        xmpp.process(block=True)
                        print("Done")
                    else:
                        print("Unable to connect.")
                elif number == 2:
                    print("\nLa siguiente es tu lista de amigos: ")
                    xmpp = login_send_message.ContactBot(opts.jid, opts.password)
                    xmpp.register_plugin('xep_0030') 
                    xmpp.register_plugin('xep_0199') 

                    if xmpp.connect():
                        xmpp.process(block=True)
                    else:
                        pass
                elif number == 3:
                    confirmation = input("\n¿Estas seguro que quieres borrar un contacto? [y/n]")
                    if confirmation == "y":
                        user = input("¿A quien deseas eliminar?: ")
                        xmpp = login_send_message.RemoveUserBot(opts.jid, opts.password, user)
                        xmpp.register_plugin('xep_0030') 
                        xmpp.register_plugin('xep_0199') 

                        if xmpp.connect():
                            xmpp.process(block=True)
                            print("Done")
                        else:
                            print("Unable to connect.")
                    else:
                        pass
                elif number == 4:
                    user = input("\nEscribe el nombre del usuario que deseas saber su status: ")
                    xmpp = login_send_message.StatusBot(opts.jid, opts.password, user)
                    xmpp.register_plugin('xep_0030') 
                    xmpp.register_plugin('xep_0199') 

                    if xmpp.connect():
                        xmpp.process(block=True)
                        print("Done")
                    else:
                        print("Unable to connect.")
                elif number == 5:
                    print("\nA continuacion se te presentara dos opciones: ")
                    print("-Para unirse a una sala ya existente solo escribe el nombre exacto de la sala que deseas entrar.")
                    print("-Para crear una nueva sala escribir el nombre de una sala no existente.")
                    opts.roomr = raw_input("\nEscriba el nombre de la sala: ")
                    opts.roomnickname = raw_input("Escribe el apodo de la sala: ")
                    xmpp = room.MUCBot(opts.jid, opts.password, opts.roomr, opts.roomnickname)
                    xmpp.register_plugin('xep_0030') # Service Discovery
                    xmpp.register_plugin('xep_0045') # Multi-User Chat
                    xmpp.register_plugin('xep_0199') # XMPP Ping

                    if xmpp.connect():
                        xmpp.process(block=False)
                        print("Done")
                    else:
                        print("Unable to connect.")
                elif number == 6:
                    ClientObject(opts.jid, opts.password).addUser()
                elif number == 7:
                    mensaje = "respeto tu privacidad tocando la puerta pero reafirmo mi autoridad entrando de todos modos, tru"
                    ClientObject(opts.jid, opts.password).BuildNotification(mensaje)
                elif number == 8:
                    restart = input("\n¿Quieres cerrar sesión? [y/n] ")
                    if restart == "y":
                        #xmpp.disconnect(wait=True)
                        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
                    else:
                        pass

                    #paraBorrar@redes2020.xyz
                    #yo
                    '''
                    y = input("¿Quieres cambiar el mensaje de presencia?[y/n] ")
                    if (y == 'y'):
                        mensaje = input("Escribe el nuevo mensaje de presencia: ")
                    else:
                        pass
                    '''