from setuptools import setup

setup(name='cycli',
      version='0.0.1',
      description='A Command Line Interface for Cypher.',
      long_description='Syntax highlighting and autocomplete.',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Neo4j :: Cypher',
      ],
      keywords='neo4j cypher cli syntax autocomplete',
      url='https://github.com/nicolewhite/cycli',
      author='Nicole White',
      author_email='nicole@neotechnology.com',
      license='MIT',
      packages=['cycli'],
      install_requires=[
        'prompt-toolkit==0.43',
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