from os import getcwd, path
from setuptools import setup, find_packages

if not path.dirname(__file__):
    _dirname = getcwd()
else:
    _dirname = path.dirname(path.dirname(__file__))


def read(name, default=None, debug=True):
    try:
        filename = path.join(_dirname, name)
        with open(filename) as f:
            return f.read()
    except Exception as e:
        err = "%s: %s" % (type(e), str(e))
        if debug:
            print(err)
        return default


def lines(name):
    txt = read(name)
    return map(
        lambda l: l.lstrip().rstrip(),
        filter(lambda t: not t.startswith('#'), txt.splitlines() if txt else [])
    )


install_requires = [i for i in lines("requirements.txt") if '-e' not in i]

setup(
    name='PyAsync',
    version='1.0.0',
    author='riki mondal',
    author_email='rkmondal41@gmail.com',
    url='https://github.com/riki-nitdgp/PyAsync',
    description='Python Async WebFramework',
    packages=find_packages(exclude=['examples', 'tests', 'docs']),
    install_requires=install_requires
)
