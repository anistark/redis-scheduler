from distutils.core import setup
import os, re


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
            filepaths.extend([os.path.join(base, filename)
                              for filename in filenames])
    return {package: filepaths}


setup(
    name = 'redis-scheduler',
    packages = ['redis-scheduler'],
    package_data=get_package_data('redis-scheduler'),
    version = get_version('redis-scheduler'),
    description = 'A redis scheduling lib',
    author = 'Kumar Anirudha',
    author_email = 'anirudhastark@yahoo.com',
    url = 'https://github.com/anistark/redis-scheduler',
    keywords = ['redis-scheduler','scheduler', 'anistark', 'python', 'redis', 'trigger', 'sqs', 'aws', 'boto3',
                'boto'],
    install_requires=[
        'redis',
        'pytz',
        'python-dateutil',
        'boto3',
        'botocore'
    ],
    dependency_links=[],
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
