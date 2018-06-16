from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='binance-db',
    version='0.0.1',
    description='Binance data cache',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/StoicPerlman/binance-db',
    author='Sam Kleiner',
    author_email='sam@skleiner.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='binance data cache',
    packages=['binance_db'],
    install_requires=['sqlalchemy', 'psycopg2-binary', 'python-binance']
)
