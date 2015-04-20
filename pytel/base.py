# The MIT License (MIT)
#
# Copyright (c) 2015 Leon Jacobs
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from utils import sockets
import socket

class TelegramBase(object):

    '''
        TelegramBase

        A python class to interface with a telegram-cli socket.
        This is the parent class.
    '''

    # Connection specific properties
    connection_type = None
    location = None
    port = None

    # The socket connection
    connection = None

    def __init__(self, location):

        '''
            Prepare a new TG() instance

            --
            @param  location:str    The location of the TCP/Unix socket. Location
                                    is broken up into 3 parts, of which the last
                                    is optional. Examples are:
                                        unix:///var/run/tg.sock
                                        tcp://127.0.0.1:2931
            @return None
        '''

        # Determine the socket type and location
        # for the telegram-cli connection
        if 'unix://' in location.lower():
            self.connection_type = 'unix'

            # strip the unix:// part. We also split by the
            # port delimiter and choose the first key
            # in case the port was accidentally
            # specified.
            self.location = location[7:].split(':')[0]

        elif 'tcp://' in location.lower():
            self.connection_type = 'tcp'

            # Check that we have both a location and a port
            # which will be delimited by a :
            if len(location[6:].split(':')) != 2:
                raise Exception('TCP Sockets should be specified in the format: tcp://host:port')

            # strip the tcp:// part and set the location
            # and port
            self.location = location[6:].split(':')[0]
            self.port = int(location[6:].split(':')[1])

        else:
            raise Exception('Unable to determine socket connection type. Expecting unix:// or tcp://')

        return

    def __del__(self):

        '''
            Desctruct the TG() instance

            Cleans up the TG() instance by closing the socket connection

            --
            @return None
        '''

        if self.connection:
            self.connection.close()

        return

    def _connect(self):

        '''
            Connect

            Setup a socket connection to the specified telegram-cli socket

            --
            @return None
        '''

        if self.connection_type.lower() == 'tcp':
            self.connection = sockets.setup_tcp_socket(self.location, self.port)

        elif self.connection_type.lower() == 'unix':
            self.connection = sockets.setup_domain_socket(self.location)

        return

    def _send(self, payload):

        '''
            Send

            Send a payload to a telegram-cli socket.

            --
            @param  payload:str     The Payload to send over a socket connection.
            @return bool
        '''

        if not self.connection:
            self._connect()

        # Send the payload, adding a newline to the end
        self.connection.send(payload + '\n')

        # Read 256 bytes off the socket and check the
        # status that returned.
        try:
            data = self.connection.recv(256)

        except socket.timeout, e:
            print 'Failed to read response in a timely manner to determine the status.'
            return False

        if data.split('\n')[1] == 'FAIL':
            print 'Failed to send payload: {payload}'.format(payload = payload)
            return False

        return True
