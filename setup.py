from distutils.core import setup

setup(
    name = 'redis-scheduler',
    packages = ['redis-scheduler'], # this must be the same as the name above
    version = '0.0.2',
    description = 'A redis scheduling lib',
    author = 'Kumar Anirudha',
    author_email = 'anirudhastark@yahoo.com',
    url = 'https://github.com/anistark/redis-scheduler', # use the URL to the github repo
    # download_url = 'https://github.com/anistark/redis-scheduler/tarball/0.1', # I'll explain this in a second
    keywords = ['redis-scheduler','scheduler', 'anistark', 'python', 'redis', 'trigger'], # arbitrary keywords
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
