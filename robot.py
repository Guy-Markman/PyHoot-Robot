import Cookie
import socket

from . import base, constants, util


class Robot(base):
    def __init__(self, buff_size, bind_address):
        super(Robot, self).__init__()
        self._buff_size = buff_size
        self._socket = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
        )
        self._socket.bind((bind_address[0], bind_address[1]))
        self._bind_address = bind_address.join(":")
        self._cookie = Cookie.SimpleCookie()

    def xmlhttprequest(self, url, method="GET"):
        request = (
            '%s %s %s%s'
            'Host: %s%s'
        ) % (
            method,
            url,
            constants.HTTP_SIGNATURE,
            constants.CRLF,
            self._bind_address,
            constants.CRLF
        )
        cookie_output = self._cookie.output(header=constants.COOKIE_HEADER)
        if cookie_output != "":
            request += "%s %s" % (cookie_output, constants.CRLF)
        request += constants.CRLF

        util.send_all(
            self._socket,
            (request).encode('utf-8')
        )

        rest = bytearray()
        #
        # Parse status line
        #
        status, rest = util.recv_line(self._socket, rest)
        status_comps = status.split(' ', 2)
        if status_comps[0] != constants.HTTP_SIGNATURE:
            raise RuntimeError('Not HTTP protocol')
        if len(status_comps) != 3:
            raise RuntimeError('Incomplete HTTP protocol')

        signature, code, message = status_comps
        if code != '200':
            raise RuntimeError('HTTP failure %s: %s' % (code, message))

        #
        # Parse headers
        #
        content_length = None
        for i in range(constants.MAX_NUMBER_OF_HEADERS):
            line, rest = util.recv_line(self._socket, rest)
            if not line:
                break

            name, value = util.parse_header(line)
            if name == 'Content-Length':
                content_length = int(value)
            if name == 'Set-Cookie':
                self._cookie.load(value)
        else:
            raise RuntimeError('Too many headers')

        file = ""
        if content_length is None:
            # Fast track, no content length
            # Recv until disconnect
            file = rest
            while True:
                buf = self._socket.recv(constants.BLOCK_SIZE)
                if not buf:
                    break
                file += buf
        else:
            # Safe track, we have content length
            # Recv excacly what requested.
            left_to_read = content_length
            while left_to_read > 0:
                if not rest:
                    t = self._socket.recv(constants.BLOCK_SIZE)
                    if not t:
                        raise RuntimeError(
                            'Disconnected while waiting for content'
                        )
                    rest += t
                buf, rest = rest[:left_to_read], rest[left_to_read:]
                file += buf
                left_to_read -= len(buf)
        return file

    def connect(self, address):
        self._socket.connect(address)

    #  Taught robot to love
    def love(self):
        return "<3"
