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

from utils import strings
from pytel import base

class Telegram(base.TelegramBase):

    '''
        Telegram

        A python class to interface with a telegram-cli socket.
        This SubClass contains the commonly used methods.
    '''

    def raw(self, payload):

        '''
            Raw

            Sends a a raw payload to the telegram-cli socket.

            --
            @param  payload:str     The Payload to send.
            @return None
        '''

        self._send(payload)

        return

    def send_message(self, recipient, message):

        '''
            Send Message

            Sends a message to a Telegram Recipient.
            From telegram-cli:
                msg <peer> <text>       Sends text message to peer

            --
            @param  recipient:str   The telegram recipient the message is intended
                                    for. Can be either a Person or a Group.
            @param  message:str     The message to send.
            @return None
        '''

        payload = 'msg {recipient} {message}'.format(
            recipient = strings.escape_recipient(recipient),
            message = strings.escape_newlines(message.strip())
        )
        self._send(payload)

        return

    def send_image(self, recipient, path):

        '''
            Send Image

            Sends a an image to a Telegram Recipient. The image needs
            to be readable to the telegram-cli instance where the
            socket is created.
            From telegram-cli:
                send_photo <peer> <file>        Sends photo to peer

            --
            @param  recipient:str   The telegram recipient the message is intended
                                    for. Can be either a Person or a Group.
            @param  path:str        The full path to the image to send.
            @return None
        '''

        payload = 'send_photo {recipient} {path}'.format(
            recipient = strings.escape_recipient(recipient),
            path = path
        )
        self._send(payload)

        return
