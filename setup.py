from setuptools import setup, find_packages

setup(
    name='kira',
    version='0.0',
    description='Analysis of characterization results',
    author='Yael Suarez',
    author_email='yaeldelcarmen.suarezlopez@ki.se',
    url=' ',
    packages=find_packages(where='src'),
    entry_points={  
    'console_scripts': [
            'xrd=kira.xrd.plot:plot_folder',
            'nir=kira.nir.plot:plot_folder',
            'mean_fl=kira.mean_fl.plot:plot_folder',
            'bet=kira.bet.radius:cli_bet_radius',
        ],
    },
    install_requires=[
        "numpy",
        "matplotlib",
        "pyyaml"
    ]
)

