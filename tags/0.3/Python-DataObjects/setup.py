from distutils.core import setup

setup(name='python-dataobjects',
      version='0.3',
      package_dir = {'': 'dataobjects'},
      packages=['domain'],
      url='http://code.google.com/p/python-dataobjects',
      description='Library to help creation of Entities and ValueObjects with easy validation.',
      long_description='Library with a lot of unit test to help creation of Entities and ValueObjects in Python with easy validation, inspired by sintax of GORM of Groovy.',
      platforms='python platforms',
      author='Paulo Cheque',
      author_email='paulocheque@agilbits.com.br',
      license='MIT',
      )

