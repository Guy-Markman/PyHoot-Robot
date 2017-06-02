## @package PyHoot-Robot.constants
# Constants for the program
## @file constants.py Implementation of @ref PyHoot-Robot.constants

## maximum size of block
BLOCK_SIZE = 1024

## Header of Cookie
COOKIE_HEADER = "Cookie: "

## New line
CRLF = '\r\n'

## Encoded new line
CRLF_BIN = CRLF.encode('utf-8')

## DEFAULT HTTP PORT
DEFAULT_HTTP_PORT = 80

## HTTP version
HTTP_SIGNATURE = 'HTTP/1.1'

## Longest Header possible
MAX_HEADER_LENGTH = 4096

## Maximum ambount of headers
MAX_NUMBER_OF_HEADERS = 100
