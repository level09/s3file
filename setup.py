from setuptools import setup

setup(name='s3file',
      version='0.1',
      description='S3 file uploads made easy',
      url='http://github.com/level09/s3file',
      author='Nidal Alhariri',
      author_email='nidal@level09.com',
      license='MIT',
      packages=['s3file'],
      install_requires=['boto','requests'
      ],
      zip_safe=False)
