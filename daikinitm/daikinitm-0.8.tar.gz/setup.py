import setuptools 

def readme():
    with open('README.md') as f:
        return f.read()


setuptools.setup(
	name='daikinitm',
    version='0.8',
    description='Daikin ITM Controller',
	long_description = readme(),
	long_description_content_type="text/markdown",
    url='https://github.com/ancutrs/daikinitm',
    author='Anucha',
    author_email='utrsanc@gmail.com',
    license='AnuchaU',
    keywords='daikin itm ',
    packages=['daikinitm'],
	
)