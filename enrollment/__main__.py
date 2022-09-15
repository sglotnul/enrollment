from configargparse import ArgumentParser, ArgumentDefaultsHelpFormatter

from .utils.argparse import clear_environ, positive_int
from .api.core import start_application

ENV_VAR_PREFIX = 'ENROLLMENT_'

parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX,
    description="yandex backend-school enrollment project 2022",
    formatter_class=ArgumentDefaultsHelpFormatter,
    allow_abbrev=True
)

group = parser.add_argument_group('API Options')
group.add_argument('--host', default='0.0.0.0', help='IPv4/IPv6 address API server would listen on')
group.add_argument('--port', required=True, type=positive_int, help='TCP port API server would listen on')

group = parser.add_argument_group('PostgreSQL options')
group.add_argument('--pg_host', default='localhost', help='PostgreSQL server name')
group.add_argument('--pg_port', default='5432', type=positive_int, help='PostgreSQL server port')
group.add_argument('--pg_user', required=True, help='PostgreSQL user name')
group.add_argument('--pg_password', required=True, help='PostgreSQL user password')
group.add_argument('--pg_database', required=True, help='PostgreSQL database name')

group = parser.add_argument_group('Logging options')
group.add_argument('--log-level', default='info', choices=('debug', 'info', 'warning', 'error', 'fatal'))

def main():
    args = parser.parse_args()

    clear_environ(lambda i: i.startswith(ENV_VAR_PREFIX))

    start_application(
        args.host, 
        args.port,
        args.pg_host,
        args.pg_port,
        args.pg_user,
        args.pg_password,
        args.pg_database
    )

if __name__ == "__main__":
    main()