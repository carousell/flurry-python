import re

from setuptools import setup, find_packages


__version__ = '0.4.0'


egg = re.compile("\#egg\=(.*?)$")
requirements = open('requirements.txt').read().splitlines()
print(requirements)
REQUIREMENTS = [req for req in requirements if (not req.startswith('-e') and not req.startswith('#') and req != '')]
DEPENDENCY_LINKS = [
    req.replace('-e ', '') for req in requirements if req.startswith('-e')
]
REQUIREMENTS.extend(
    [egg.findall(req)[0] for req in requirements if req.startswith('-e')]
)


setup(
    name='flurry',
    version=__version__,
    zip_safe=False,
    packages=find_packages(exclude=["test*"]),
    dependency_links=DEPENDENCY_LINKS,
    install_requires=REQUIREMENTS
)
