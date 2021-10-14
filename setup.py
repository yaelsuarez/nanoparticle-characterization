from setuptools import setup, find_packages

setup(name='kira',
      version='0.1',
      description='Analysis of characterization results',
      author='Yael Suarez',
      author_email='yaeldelcarmen.suarezlopez@ki.se',
      url=' ',
      packages=["bet", "model"],
      package_dir={
          "": ".",
          "bet": "./kira/bet",
          "model": "./kira/model",
      },
      entry_points={
          'console_scripts': [
              'bet=bet.radius:cli_bet_radius',
          ],
      },
      install_requires=["numpy", "matplotlib", "pyyaml"])
