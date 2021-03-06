## @package PyHoot-Robot.__main__
# Main file
## @file __main__.py Implementation of @ref PyHoot-Robot.__main__

import argparse
import logging

from . import base, constants, robot, util


def parse_args():
    """Parser args"""
    parser = argparse.ArgumentParser()
    LOG_STR_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    parser.add_argument(
        '--bind-address',
        default="0.0.0.0:0",
        help='Bind address, default: %(default)s',
    )

    parser.add_argument(
        "--connect-address",
        default="localhost:8080",
        help="The address we will connect to, default %(default)s",
    )
    parser.add_argument(
        "--buff-size",
        default=constants.BLOCK_SIZE,
        type=int,
        help="Buff size for each time, default %(default)d"
    )

    parser.add_argument(
        '--log-level',
        dest='log_level_str',
        default='INFO',
        choices=LOG_STR_LEVELS.keys(),
        help='Log level',
    )
    parser.add_argument(
        '--log-file',
        dest='log_file',
        metavar='FILE',
        required=False,
        help='Logfile to write to, otherwise will log to console.',
    )
    args = parser.parse_args()
    args.log_level = LOG_STR_LEVELS[args.log_level_str]
    args.bind_address = util.split_address(args.bind_address, "--bind-address")
    args.connect_address = util.split_address(
        args.connect_address, "--connect-address")
    return args


def main():
    """Main"""
    args = parse_args()
    close_file = []
    if args.log_file:
        close_file.append(open(args.log_file, 'a'))
        logger = base.setup_logging(
            stream=close_file[0],
            level=args.log_level,
        )
    else:
        logger = base.setup_logging(
            level=args.log_level,
        )
    logger.info("Parsed args and created logger")
    r = robot.Robot(args.buff_size, args.bind_address, args.connect_address)
    r.play(*r.register())

    for f in close_file:
        f.close()


if __name__ == "__main__":
    main()
