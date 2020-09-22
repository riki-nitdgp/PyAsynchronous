import os
from setuptools import setup, find_packages


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

BASE_DIR = os.path.join(os.path.dirname(__file__))

with open(os.path.join(BASE_DIR, 'requirements.txt')) as f:
    REQUIREMENTS = f.read()



URL = 'https://github.com/riki-nitdgp/PyAsync'
README = "For more info, go to: {}".format(URL)
VERSION = "1.1.0.dev"


setup(
    name='PyAsync',
    version=VERSION,
    description='PyAsync is lightweight and simple async web Framework based on python3.6+',
    author='Riki Mondal',
    author_email='rkmondal41@gmail.com',
    long_description=README,
    url=URL,
    packages=find_packages(exclude=['test*']),
    zip_safe=False,
    include_package_data=True,
    install_requires=REQUIREMENTS,
    setup_requires=REQUIREMENTS,
    license='MIT License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)