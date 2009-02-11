from distutils.core import setup

long_description = open('README.rst').read()

setup(
    name='django-failwhale',
    version="0.1",
    package_dir={'failwhale': 'failwhale'},
    packages=['failwhale'],
    description='Twitter client for Django',
    author='Jeremy Carbaugh',
    author_email='jcarbaugh@sunlightfoundation.com',
    license='BSD License',
    url='http://github.com/sunlightlabs/django-failwhale/',
    long_description=long_description,
    platforms=["any"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Environment :: Web Environment',
    ],
)