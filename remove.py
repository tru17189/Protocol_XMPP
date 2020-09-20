from __future__ import absolute_import, unicode_literals

import logging
from optparse import OptionParser
import getpass

from sleekxmpp.stanza import StreamFeatures
from sleekxmpp.basexmpp import BaseXMPP
from sleekxmpp.exceptions import XMPPError
from sleekxmpp.xmlstream import XMLStream
from sleekxmpp.xmlstream.matcher import StanzaPath, MatchXPath
from sleekxmpp.xmlstream.handler import Callback

try:
    import dns.resolver
except ImportError:
    DNSPYTHON = False
else:
    DNSPYTHON = True


log = logging.getLogger(__name__)

raw_input = input 

class RemoveUser(BaseXMPP):
    def __init__(self, jid, password, plugin_config=None,
                 plugin_whitelist=None, escape_quotes=True, sasl_mech=None,
                 lang='en', **kwargs):
        if not plugin_whitelist:
            plugin_whitelist = []
        if not plugin_config:
            plugin_config = {}

        BaseXMPP.__init__(self, jid, 'jabber:client', **kwargs)

        self.escape_quotes = escape_quotes
        self.plugin_config = plugin_config
        self.plugin_whitelist = plugin_whitelist
        self.default_port = 5222
        self.default_lang = lang

        self.credentials = {}

        self.password = password

        self.stream_header = "<stream:stream to='%s' %s %s %s %s>" % (
                self.boundjid.host,
                "xmlns:stream='%s'" % self.stream_ns,
                "xmlns='%s'" % self.default_ns,
                "xml:lang='%s'" % self.default_lang,
                "version='1.0'")
        self.stream_footer = "</stream:stream>"

        self.features = set()
        self._stream_feature_handlers = {}
        self._stream_feature_order = []

        self.dns_service = 'xmpp-client'

        #TODO: Use stream state here
        self.authenticated = False
        self.sessionstarted = False
        self.bound = False
        self.bindfail = False

        self.add_event_handler('connected', self._reset_connection_state)
        self.add_event_handler('session_bind', self._handle_session_bind)
        self.add_event_handler('roster_update', self._handle_roster)

        self.register_stanza(StreamFeatures)

        self.register_handler(
                Callback('Stream Features',
                         MatchXPath('{%s}features' % self.stream_ns),
                         self._handle_stream_features))
        self.register_handler(
                Callback('Roster Update',
                         StanzaPath('iq@type=set/roster'),
                         lambda iq: self.event('roster_update', iq)))

        # Setup default stream features
        self.register_plugin('feature_starttls')
        self.register_plugin('feature_bind')
        self.register_plugin('feature_session')
        self.register_plugin('feature_rosterver')
        self.register_plugin('feature_preapproval')
        self.register_plugin('feature_mechanisms')

        if sasl_mech:
            self['feature_mechanisms'].use_mech = sasl_mech

    def del_roster_item(self, jid):
        print("Se borrara")
        return self.client_roster.remove(jid)

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
        opts.jid = input("Username: ")
        print("Este sera tu usuario -> ", opts.jid)
    if opts.password is None:
        opts.password = getpass.getpass("Password: ")

    xmpp = RemoveUser(opts.jid, opts.password)
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
