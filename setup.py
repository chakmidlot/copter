from distutils.core import setup

from setuptools import find_packages

setup(name='copter',
      version='0.1.1',
      description='Offline CLI password manager',
      author='Dzmitry Talkach',
      author_email='chakmidlot@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=find_packages(exclude=['contrib', 'docs', 'tests']),
      install_requires=[
          'pyperclip==1.7.0',
          'cryptography==42.0.4',
          'cffi==1.13.1'
      ],
      entry_points={
          'console_scripts': [
              'copter-daemon=copter.daemon.service:start_server',
              'copter=copter.main:main',
          ]
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Password manager',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.8',
      ],
)
