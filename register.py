import sys
import logging
import getpass
from optparse import OptionParser

import sleekxmpp
from sleekxmpp.exceptions import IqError, IqTimeout

raw_input = input


class RegisterBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        sleekxmpp.ClientXMPP.__init__(self, jid, password)

        # El evento session_start inicializa el bot para 
        # establecer coneccion con el servidor y con el XML
        # stream para confirmar si esta listo para ser usado.
        self.add_event_handler("session_start", self.start)

        # El evento register provee un resultado Iq  stanza 
        # con una registro del servidor. 
        self.add_event_handler("register", self.register)

    def start(self, event):
        """
        Aqui se inicia la sesion.

        Este evento solicita una lista y un broadcasting 
        para una presencia inicial del stanza. .
        """
        self.send_presence()
        self.get_roster()
        self.disconnect()

    def register(self, iq):
        """
        Complete y envíe un formulario de registro.

        El registro esta compuesto por una registracion basica en sus campos,
        en la data del formulario, un out-band-link, o cualquier otra
        combinacion. 
        """
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            resp.send(now=True)
            logging.info("Account created for %s!" % self.boundjid)
        except IqError as e:
            logging.error("Could not register account: %s" % 
                    e.iq['error']['text'])
            self.disconnect()
        except IqTimeout:
            logging.error("No response from server.")
            self.disconnect()
        """
        Aqui se termina el proceso de registro del codigo y se coloca un 
        try si en caso ocurriese un error a la hora del registro, con esto
        me aseguro que si falla el usuario lo sepa.  
        """

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

    opts, args = optp.parse_args()

    logging.basicConfig(level=opts.loglevel,
                        format='%(levelname)-8s %(message)s')

    if opts.jid is None:
        opts.jid = raw_input("Username: ")
        print("Este sera tu usuario -> ", opts.jid)
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")

    xmpp = RegisterBot(opts.jid, opts.password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0004') # Data forms
    xmpp.register_plugin('xep_0066') # Out-of-band Data
    xmpp.register_plugin('xep_0077') # In-band Registration

    if xmpp.connect():
        xmpp.process(block=True)
        print("Done")
    else:
        print("Unable to connect.")

#con = RegisterBot("tru@redes2020.xyz", "alex")
