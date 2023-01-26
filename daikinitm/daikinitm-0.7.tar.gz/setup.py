import setuptools 


with open('README.md') as f:
      long_description  = f.read()

setuptools.setup(
	name='daikinitm',
    version='0.7',
    description='Daikin ITM Controller',
	long_description = "README.md",
	long_description_content_type="text/markdown",
    url='https://github.com/ancutrs/daikinitm',
    author='Anucha',
    author_email='utrsanc@gmail.com',
    license='AnuchaU',
    keywords='daikin itm ',
    packages=['daikinitm'],
	
)