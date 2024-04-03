from setuptools import setup, find_packages

setup(
    name='TCG_collector',
    version='1.0.0',
    author='K.Womack',
    author_email='womack5706@gmail.com',
    description='A program for creating a list of your own Yu-Gi-Oh! TCG Card Collection.',
    url='https://github.com/womack5706/TCG_collector',
    packages=find_packages(),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'tkinter',
        'csv',
        'pathlib',
        'yugioh_database',
        'about-time',
        'alive-progress',
        'bs4',
        'charset-normalizer',
        'importlib',
        'langdetect',
        'packaging',
        'pillow',
        'pyinstaller',
        'pyinstaller-hooks-contrib',
        'setuptools',
        'tk',
        # Add any other dependencies here
    ],
)
