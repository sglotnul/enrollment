import argparse
import logging
import os

from alembic.config import CommandLine

from enrollment.utils.alembic import make_alembic_config
from enrollment.utils.argparse import positive_int

def main():
    logging.basicConfig(level=logging.DEBUG)

    alembic_cl = CommandLine()
    alembic_cl.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter

    alembic_cl.parser.add_argument('--host', default='localhost', help='PostgreSQL server name')
    alembic_cl.parser.add_argument('--port', default='5432', type=positive_int, help='PostgreSQL server port')
    alembic_cl.parser.add_argument('--user', required=True, help='PostgreSQL user name')
    alembic_cl.parser.add_argument('--password', required=True, help='PostgreSQL user password')
    alembic_cl.parser.add_argument('--database', required=True, help='PostgreSQL database name')

    options = alembic_cl.parser.parse_args()
    if 'cmd' not in options:
        alembic_cl.parser.error('too few arguments')
        exit(128)
    else:
        config = make_alembic_config(options)
        exit(alembic_cl.run_cmd(config, options))

if __name__ == '__main__':
    main()