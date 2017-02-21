from setuptools import setup

setup(name='giroptic_osc',
      version='0.1',
      description='Python package to connect to Giroptic 360cam (and other non-tested OSC capable cameras)',
      url='http://github.com/ariksidney/giroptic_osc',
      author='Arik Sidney Guggenheim, Matthias Haeni (Swiss Federal Research Institute WSL)',
      author_email='arik.guggenheim@wsl.ch',
      license='MIT',
      packages=['giroptic_osc'],
      install_requires=['requests'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Programming Language :: Python :: 3.x',
      ],
      zip_safe=False)
