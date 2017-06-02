## @package PyHoot-Robot.util
# Util file
## @file util.py Implementation of @ref PyHoot-Robot.util


import urlparse
from xml.etree import ElementTree

import constants


def send_all(s, buf):
    """Send all the buff"""
    while buf:
        buf = buf[s.send(buf):]


def recv_line(
    s,
    buf,
    max_length=constants.MAX_HEADER_LENGTH,
    block_size=constants.BLOCK_SIZE,
):
    """Receive a single line
    @return a single line"""
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
    """Parse a header
    @return The header"""
    SEP = ':'
    n = line.find(SEP)
    if n == -1:
        raise RuntimeError('Invalid header received')
    return line[:n].rstrip(), line[n + len(SEP):].lstrip()


def split_address(address, name):
    """Split address
    @return The address"""
    a = address.split(":")
    if len(a) != 2:
        raise ValueError(
            """%s need to be in the next format:
                server_address:server_port""" % name
        )
    a[1] = int(a[1])
    return a


def parse_xml_from_string(xmlstring):
    """Turn xml string to ElementTree object
    @return XML file from the string"""
    return ElementTree.fromstring(xmlstring.decode("utf-8"))


def xmlstring_to_boolean(xmlstring):
    """Turn xml to boolean
    @reutrn boolean"""
    return parse_xml_from_string(str(xmlstring)).attrib["answer"] == "True"


def build_url(path, querry={}):
    """Build url from path and querry
    @param path - the path we want
    @param querry - The querry that we want to add to the url
    @return url
    """
    return urlparse.urlunsplit(urlparse.SplitResult(
        "",
        "",
        "/%s" % path,
        "&".join(["%s=%s" % (key, value) for (key, value) in querry.items()]),
        ""
    ))
