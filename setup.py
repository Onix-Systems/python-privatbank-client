from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='python_internal_privat',
  version='0.0.3',
  author='ihor.sotnyk',
  author_email='ihor.sotnyk@onix-systems.com',
  description='This module is designed for quick interaction with the privatbank API.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://gitlab.onix.ua/onix-systems/python-internal-privat',
  packages=find_packages(),
  install_requires=[
    'requests>=2.25.1',
    'python-dotenv==1.0.0'
],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  python_requires='>=3.6'
)
