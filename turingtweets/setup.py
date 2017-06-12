import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_jinja2',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'ipython',
    'pyramid_ipython',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'redis',
    'psycopg2',
    'markovify',
]

tests_require = [
    'WebTest >= 1.3.1',
    'pytest',
    'pytest-cov',
    'tox',
]

setup(
    name='turingtweets',
    version='0.0',
    description='Turing Tweets',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='David Lim, Miguel Pena, James Feore, Elyanil Castro',
    author_email='turingtrump@gmail.com',
    url='https://github.com/jjfeore/turingtweets',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = turingtweets:main',
        ],
        'console_scripts': [
            'initialize_turingtweets_db = turingtweets.scripts.initializedb:main',
        ],
    },
)
