from setuptools import find_packages, setup
from typing import List
from pkg_resources import parse_requirements

requirements_file_path = 'requirements.txt'

scripts = [
    'enrollment = enrollment.api.__main__:main'
]

def load_requirements(fname: str) -> List[str]:
    requirements = []
    with open(fname, 'r') as fp:
        for req in parse_requirements(fp.read()):
            extras = '[{}]'.format(','.join(req.extras)) if req.extras else ''
            requirements.append(req.name + extras + str(req.specifier))
    return requirements

setup(
    name='enrollment',
    version='1.0.0',
    author='sglotnul',
    platforms='all',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: Russian',
        'Operating System :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
    python_requires='>=3.8',
    packages=find_packages(),
    install_requires=load_requirements(requirements_file_path),
    entry_points={
        'console_scripts': scripts
    },
    include_package_data=True
)