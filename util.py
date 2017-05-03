import constants


def send_all(s, buf):
    while buf:
        buf = buf[s.send(buf):]


def recv_line(
    s,
    buf,
    max_length=constants.MAX_HEADER_LENGTH,
    block_size=constants.BLOCK_SIZE,
):
    while True:
        if len(buf) > max_length:
            raise RuntimeError(
                'Exceeded maximum line length %s' % max_length)

        n = buf.find(constants.CRLF_BIN)
        if n != -1:
            break

        t = s.recv(block_size)
        if not t:
            raise RuntimeError('Disconnect')
        buf += t

    return buf[:n].decode('utf-8'), buf[n + len(constants.CRLF_BIN):]


def parse_header(line):
    SEP = ':'
    n = line.find(SEP)
    if n == -1:
        raise RuntimeError('Invalid header received')
    return line[:n].rstrip(), line[n + len(SEP):].lstrip()


def split_address(address, name):
    a = address.split(":")
    if len(a) != 2:
        raise ValueError(
            """%s need to be in the next format:
                server_address:server_port""" % name
        )
    return a
