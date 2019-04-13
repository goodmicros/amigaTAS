#! /usr/bin/env python3
#
# Example program using irc.bot.
#
# Joel Rosdahl <joel@rosdahl.net>

"""A simple example bot.

This is an example bot that uses the SingleServerIRCBot class from
irc.bot.  The bot enters a channel and listens for commands in
private messages and channel traffic.  Commands in channel messages
are given by prefixing the text by the bot name followed by a colon.
It also responds to DCC CHAT invitations and echos data sent in such
sessions.

The known commands are:

    stats -- Prints some channel information.

    disconnect -- Disconnect the bot.  The bot will try to reconnect
                  after 60 seconds.

    die -- Let the bot cease to exist.

    dcc -- Let the bot invite you to a DCC CHAT connection.
"""

import irc.bot
import irc.strings
from irc.client import ip_numstr_to_quad, ip_quad_to_numstr
import threading
import time
import sys


class tas():
    def __init__(self, port):
        import serial
        self.s = serial.Serial(port, baudrate = 115200)
        self.tickrate = 1/10
        self.holdtime = 0.1
        self.commands = {
        'u':{'release':0,
            'value':bytes.fromhex('3e')
            },
        'd':{'release':0,
            'value':bytes.fromhex('3d')
            },
        'l':{'release':0,
            'value':bytes.fromhex('3b')
            },
        'r':{'release':0,
            'value':bytes.fromhex('37')
            },
        'a':{'release':0,
            'value':bytes.fromhex('2f')
            },
        'b':{'release':0,
            'value':bytes.fromhex('1f')
            }
        }
        self.run = True
        self.tick()

    def stop(self):
        self.run = False

    def set(self, value):
        if value in self.commands:
            print(value)
            self.commands[value]['release'] = time.time()+self.holdtime

    def tick(self):
        t = time.time()
        print(t)
        print(self.commands)
        mapping = bytes.fromhex('ff') 
        #generate current mapping from commands
        for key, button in self.commands.items():
            if button['release'] > t:
                mapping = bytes([mapping[0] & button['value'][0]])
        print(mapping)
        #update
        self.s.write(mapping)
        if self.run:
            threading.Timer(self.tickrate, self.tick).start()
            

class TestBot(irc.bot.SingleServerIRCBot):
    def __init__(self, tas, channel, nickname, server, port=6667):
        irc.bot.SingleServerIRCBot.__init__(
            self, [(server, port)], nickname, nickname)
        self.channel = channel
        self.tas = tas

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)

    def on_privmsg(self, c, e):
        pass

    def on_pubmsg(self, c, e):
        message = e.arguments[0]
        self.tas.set(message)

    def on_dccmsg(self, c, e):
        pass

    def on_dccchat(self, c, e):
        pass

def main():
    import sys

    server = "localhost"
    port = 6667
    channel = "#test"
    nickname = "a600"

    t = tas('/dev/ttyACM0')

    bot = TestBot(t, channel, nickname, server, port)
    bot.start()


if __name__ == "__main__":
    main()
