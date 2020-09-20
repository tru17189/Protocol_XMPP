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

import register 
import login_send_message
import room

try:
    import dns.resolver
except ImportError:
    DNSPYTHON = False
else:
    DNSPYTHON = True

log = logging.getLogger(__name__)

class ClientObject(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password,):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start, threaded=True)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.client_roster()
        self.disconnect(wait=True)

while True:
    print("1. Registrar una nueva cuenta en el servidor.")
    print("2. Iniciar Sesión (Hasta hacer esto podras mandar mensajes)")
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
            print(f"Que deseas hacer {opts.jid}")
            while True:
                print("1. Mandar Mensaje a alguien en especifico.")
                print("2. Lista de amigos.")
                print("3. Eliminar a un contacto.")
                print("4. Ver el estado de un usuario.")
                print("5. Crear un chat compartido / Unirse a un chat compartido.")
                print("6. Cerrar Sesion.")
                number = int(input("Escribe el numero de la opcion que deseas: "))
                if number == 1:
                    if opts.to is None:
                        opts.to = raw_input("Para: ")
                    if opts.message is None:
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
                    print("La siguiente es tu lista de amigos: ")
                    xmpp = login_send_message.ContactBot(opts.jid, opts.password)
                    xmpp.register_plugin('xep_0030') 
                    xmpp.register_plugin('xep_0199') 

                    if xmpp.connect():
                        xmpp.process(block=True)
                    else:
                        pass
                elif number == 3:
                    confirmation = input("¿Estas seguro que quieres borrar un contacto? [y/n]")
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
                    user = input("Escribe el nombre del usuario que deseas saber su status: ")
                    xmpp = login_send_message.StatusBot(opts.jid, opts.password, user)
                    xmpp.register_plugin('xep_0030') 
                    xmpp.register_plugin('xep_0199') 

                    if xmpp.connect():
                        xmpp.process(block=True)
                        print("Done")
                    else:
                        print("Unable to connect.")
                elif number == 5:
                    restart = input("¿Quieres cerrar sesión? [y/n] ")
                    if restart == "y":
                        os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
                    else:
                        pass

                    #paraBorrar@redes2020.xyz
                    #yo