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

import socket

'''
    Sockets

    Contains methods used to connect to Unix Domain or TCP sockets.
'''

timeout = 5

def setup_domain_socket(location):

    '''
        Setup Domain Socket

        Setup a connection to a Unix Domain Socket

        --
        @param  location:str    The path to the Unix Domain Socket to connect to.
        @return <class 'socket._socketobject'>
    '''

    clientsocket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    clientsocket.settimeout(timeout)
    clientsocket.connect(location)

    return clientsocket

def setup_tcp_socket(location, port):

    '''
        Setup TCP Socket

        Setup a connection to a TCP Socket

        --
        @param  location:str    The Hostname / IP Address of the remote TCP Socket.
        @param  port:int        The TCP Port the remote Socket is listening on.
        @return <class 'socket._socketobject'>
    '''

    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.settimeout(timeout)
    clientsocket.connect((location, port))

    return clientsocket
