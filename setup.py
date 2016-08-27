from setuptools import setup
from cycli import __version__

setup(name='cycli',
      version=__version__,
      description='A Command Line Interface for Cypher.',
      long_description='Syntax highlighting and autocomplete.',
      keywords='neo4j cypher cli syntax autocomplete',
      url='https://github.com/nicolewhite/cycli',
      author='Nicole White',
      author_email='nmwhite0131@gmail.com',
      license='MIT',
      packages=['cycli'],
      install_requires=[
        'click==4.1',
        'prompt-toolkit==0.57',
        'Pygments==2.0.2',
        'py2neo==3.1.2'
      ],
      include_package_data=True,
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'cycli = cycli.main:run'
        ]
    })
