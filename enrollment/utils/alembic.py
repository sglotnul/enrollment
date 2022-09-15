import os
from pathlib import Path
from types import SimpleNamespace
from typing import Union
from alembic.config import Config
from configargparse import Namespace

PROJECT_PATH = Path(__file__).parent.parent.resolve()

def make_alembic_config(cmd_opts: Union[Namespace, SimpleNamespace],
                        base_path: str = PROJECT_PATH) -> Config:
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config)

    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name,
                    cmd_opts=cmd_opts)

    alembic_location = config.get_main_option('script_location')
    if not os.path.isabs(alembic_location):
        config.set_main_option('script_location',
                               os.path.join(base_path, alembic_location))

    
    url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(cmd_opts.user, cmd_opts.password, cmd_opts.host, cmd_opts.port, cmd_opts.database)

    config.set_main_option('sqlalchemy.url', url)

    return config