from setuptools import setup

setup(
  name='bowerbird',
  packages=['bowerbird'],
  version='0.4.0',
  description=(
      'A collection of stdlib logging.Formatter classes using Pygments'),
  author='Bartek Brak',
  install_requires=['sqlparse==0.1.18', 'Pygments'],
  author_email='bartek0brak@gmail.com',
  url='https://github.com/bartekbrak/bowerbird',
  download_url='https://github.com/bartekbrak/bowerbird/archive/0.4.0.tar.gz',
)
