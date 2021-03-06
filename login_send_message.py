import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp

if sys.version_info < (3, 0):
    from sleekxmpp.util.misc_ops import setdefaultencoding
    setdefaultencoding('utf8')
else:
    raw_input = input


class SendMsgBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password, recipient, message):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # variable la cual recibe el usuario destino del mensaje.
        self.recipient = recipient
        # variable la cual sirve para recupilar el mensaje que se enviara. 
        self.msg = message

        # El evento session_start inicializa el bot para 
        # establecer coneccion con el servidor y con el XML
        # stream para confirmar si esta listo para ser usado.
        self.add_event_handler("session_start", self.start, threaded=True)

    """
    Se inicia el evento de mandar mensaje y se construye
    el objeto, el cual recibe los parametros necesarios para 
    poder mandar el mensaje como la presencia del usuario origen
    y el usuario destino en donde acabara el mensaje. 
    """
    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.client_roster

        self.send_message(mto=self.recipient,
                          mbody=self.msg,
                          mtype='chat')

        self.disconnect(wait=True)


# Clase que sirve para imprimir a los usuarios amigos del usuario 
# que este usando el programa. 
class ContactBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.start, threaded=True)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.client_roster
        print("clientes: ", self.client_roster.groups())

        self.disconnect(wait=True)

# Clase que sirve para borrar un usuario de la lista de amigos
# del usuario que este usando el programa. 
class RemoveUserBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, next_user):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.next_user = next_user

        self.add_event_handler("session_start", self.start, threaded=True)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        # Funcion provista por el sleekxmpp.ClientXMPP que sirve para 
        # cambiar el status de un usuario amigo a "removed"
        self.del_roster_item(self.next_user)

        self.disconnect(wait=True)

# Clase que sive para buscar el status de un usuario en especifico.
class StatusBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, next_user):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start, threaded=True)
        self.next_user = next_user

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.client_roster
        # Aqui se busca dentro el cliente roster el status del usuario ingresado
        print("Este es: ", self.client_roster.presence(self.next_user))
        self.disconnect(wait=True)

# A partir de este punto hasta el final es codigo que no se usa en el 
# programa principal que se evaluara en el proyecto, este codigo solo me sirve 
# por si quisiese probar especificamente las funcionalidades de este script.
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
        opts.password = getpass.getpass("Password: ")
    if opts.to is None:
        opts.to = raw_input("Send To: ")
    if opts.message is None:
        opts.message = raw_input("Message: ")

    xmpp = SendMsgBot(opts.jid, opts.password, opts.to, opts.message)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping

    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")

