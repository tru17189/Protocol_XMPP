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

# Clase para salas o unirte a una sala compartida. aparte en esta clase
# se define el mensaje de presencia que se tiene cuando te conectas en 
# alguna sala. 
class MUCBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password, room, nick):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # Variable que se usa para definir el nombre el nombre de la sala
        # Ejemplo: Example@confenrence.redes2020.xyz
        self.room = room
        # Variabe que se usa para definir el apodo de la sala. 
        # Ejemplo: Example 
        self.nick = nick
        # Varianle que sirve para recibir el mensjae de presencia, aunque 
        # ya tiene uno por default. 
        self.presence = "Imponiendo su presencia"

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.muc_message)
        self.add_event_handler("muc::%s::got_online" % self.room,
                               self.muc_online)

        n = input("\n¿Deseas cambiar el mensaje de presencia?[y/n] ")
        if n == "y":
            new = input("Escribe el nuevo mensaje de presencia: ")
            self.presence = new
        else:
            pass
    """
    Se inicia el evento para crear un objeto sala que recibe los parametros
    que antes de describieron. 
    """
    def start(self, event):
        self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].joinMUC(self.room,
                                        self.nick,
                                        # If a room password is needed, use:
                                        # password=the_room_password,
                                        wait=True)

        """
        Aqui se configura la sala anteriormente creada para que la opcion 
        'persistent' de mantega en True, asi aunque la consola no este corriendo
        la sala seguira existiendo y siendo util para cualquiera que se 
        quiera meter. 
        """
        roomform = self.plugin['xep_0045'].getRoomConfig(self.room)
        roomform.set_values({
            'muc#roomconfig_persistentroom': 1,
        })
        self.plugin['xep_0045'].configureRoom(self.room, form=roomform)

    """
    Se verifica que se estan escuchando los mensajes. 
    """    
    def muc_message(self, msg):
        if msg['mucnick'] != self.nick and self.nick in msg['body']:
            self.send_message(mto=msg['from'].bare,
                              mbody="I heard that, %s." % msg['mucnick'],
                              mtype='groupchat')

    """
    Se devuelve el mensaje de presencia anteriormente definido para cuando 
    el usuario inicia a la sala. 
    """
    def muc_online(self, presence):
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                              mbody="{}, %s %s".format(self.presence) % (presence['muc']['role'],
                                                      presence['muc']['nick']),
                              mtype='groupchat')

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
    optp.add_option("-r", "--room", dest="room",
                    help="MUC room to join")
    optp.add_option("-n", "--nick", dest="nick",
                    help="MUC nickname")

    opts, args = optp.parse_args()

    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")
    if opts.room is None:
        opts.room = raw_input("MUC room: ")
    if opts.nick is None:
        opts.nick = raw_input("MUC nickname: ")

    xmpp = MUCBot(opts.jid, opts.password, opts.room, opts.nick)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0045') # Multi-User Chat
    xmpp.register_plugin('xep_0199') # XMPP Ping

    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")
