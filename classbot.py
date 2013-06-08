#!/usr/bin/env python
# coding: utf-8
"""
    ClassBot

    A simple IRCBot to manage Q&A sessions on IRC

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Tarashish Mishra <sunu0000@gmail.com>"
__version__ = "1.0"
__date__ = "8 June 2013"
__copyright__ = "Copyright (c) Tarashish Mishra"
__license__ = "GPL3"

from ircbot import SingleServerIRCBot
from irclib import nm_to_n

from datetime import datetime

# IRC Server Configuration
SERVER = "irc.freenode.net"
PORT = 6667
SERVER_PASS = None
CHANNELS = ["#sunu"]
OPERATORS = ["sunu", "SunuTheNinja"]
NICK = "wfs-classbot"
NICK_PASS = ""

# Time gap in between questions in seconds. Asker can't ask more than 1 question
# within this timegap.
TIME_GAP = 30


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
        self.question_queue = []
        self.timestamps = {}

        print "ClassBot %s" % __version__
        print "Connecting to %s:%i..." % (server, port)
        print "Press Ctrl-C to quit"

    def quit(self):
        self.connection.disconnect("Quitting...")

    def on_welcome(self, c, e):
        for chan in self.chans:
            c.join(chan)
            print "Joined channel {0}".format(chan)

    def on_nicknameinuse(self, c, e):
        """Nickname in use"""
        c.nick(c.get_nickname() + "_")

    def on_privmsg(self, c, e):
        asker = nm_to_n(e.source())
        now = datetime.now()
        last_time = self.timestamps.get(asker)
        if last_time:
            timedelta = now - last_time
            timegap = timedelta.total_seconds()
        else:
            timegap = None
        if not timegap or timegap > TIME_GAP:
            questions = e.arguments()
            print asker, questions
            self.question_queue.append((asker, questions[0]))
            self.timestamps[asker] = datetime.now()
            success_msg = "Your question is in queue to be asked. Thank you!"
            c.privmsg(asker, success_msg)
        else:
            error_msg = "You can ask only one question every 30 seconds. Please be patient and wait a \
while before asking another question. Thank you."
            c.privmsg(asker, error_msg)

    def on_pubmsg(self, c, e):
        if e.arguments()[0].startswith(NICK):
            msg = e.arguments()[0]
            user = e.source().split("!")[0]
            cmd = msg.split()[1].lower()
            if cmd == "next" and user in self.operators:
                if self.question_queue:
                    asker, question = self.question_queue.pop(0)
                    m = "{0}, {1} asks: {2}".format(user, asker, question)
                    c.privmsg(e.target(), m)
                else:
                    m = "{0}, The question queue is empty now.".format(user)
                    c.privmsg(e.target(), m)


def main():
    bot = ClassBot(SERVER, PORT, SERVER_PASS, CHANNELS, NICK, NICK_PASS, OPERATORS)

    try:
        bot.start()
    except KeyboardInterrupt:
        bot.quit()

if __name__ == '__main__':
    main()
