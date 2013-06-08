__author__ = "Tarashish Mishra <sunu0000@gmail.com>"
__version__ = "1.0"
__date__ = "8 June 2013"
__copyright__ = "Copyright (c) Tarashish Mishra"
__license__ = "GPL3"

from ircbot import SingleServerIRCBot

# IRC Server Configuration
SERVER = "irc.freenode.net"
PORT = 6667
SERVER_PASS = None
CHANNELS = ["#sunu"]
OPERATORS = ["sunu", "SunuTheNinja"]
NICK = "wfs-classbot"
NICK_PASS = ""

HELP_MSG = "WFS-India - Women in Free Software and Culture in India - www.wfs-india.org. \
Some useful commands - 'logs', 'website', 'events'. Usage: {0}: <command>"


class ClassBot(SingleServerIRCBot):
    """The Bot."""
    def __init__(self, server, port, server_pass=None, channels=[],
                 nick="timber", nick_pass=None, operators=OPERATORS):
        SingleServerIRCBot.__init__(self,
                                    [(server, port, server_pass)],
                                    nick,
                                    nick)

        self.chans = [x.lower() for x in channels]
        self.operators = operators
        self.count = 0
        self.nick_pass = nick_pass

        print "Logbot %s" % __version__
        print "Connecting to %s:%i..." % (server, port)
        print "Press Ctrl-C to quit"

    def quit(self):
        self.connection.disconnect("Quitting...")

    def on_welcome(self, c, e):
        for chan in self.chans:
            c.join(chan)


def main():
    bot = ClassBot(SERVER, PORT, SERVER_PASS, CHANNELS, NICK, NICK_PASS, OPERATORS)

    try:
        bot.start()
    except KeyboardInterrupt:
        bot.quit()

if __name__ == '__main__':
    main()
