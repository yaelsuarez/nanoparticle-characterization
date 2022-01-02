from setuptools import setup, find_packages

setup(name='kira',
      version='0.1',
      description='Analysis of characterization results',
      author='Yael Suarez',
      author_email='yael.suarez@ki.se',
      url=' ',
      packages=["bet", "model", "ftir"],
      package_dir={
          "": ".",
          "bet": "./kira/bet",
          "model": "./kira/model",
          "ftir": "./kira/ftir"
      },
      entry_points={
          'console_scripts': [
              'bet=bet.radius:cli_bet_radius',
              'ftir=ftir.cli:main'
          ],
      },
      install_requires=["numpy", "matplotlib", "pyyaml"])
