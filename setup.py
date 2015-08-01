from setuptools import setup

setup(name='cycli',
      version='0.0.1',
      description='A Command Line Interface for Cypher.',
      long_description='Syntax highlighting and autocomplete.',
      keywords='neo4j cypher cli syntax autocomplete',
      url='https://github.com/nicolewhite/cycli',
      author='Nicole White',
      author_email='nicole@neotechnology.com',
      license='MIT',
      packages=['cycli'],
      install_requires=[
        'click==4.1',
        'prompt-toolkit==0.43',
        'Pygments==2.0.2',
        'py2neo==2.0.7',
        'requests==2.7.0',
      ],
      include_package_data=True,
      zip_safe=False,
      entry_points={
        'console_scripts': [
            'cycli = cycli.main:run'
        ]
    })