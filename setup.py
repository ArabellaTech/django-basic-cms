# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pkg_resources import require, DistributionNotFound
import basic_cms
import os
package_name = 'django-basic-cms'


def local_open(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))

requirements = local_open('requirements/external_apps.txt')
test_requirements = local_open('requirements/extra_apps.txt')

# Build the list of dependency to install
required_to_install = []
for dist in requirements.readlines():
    dist = dist.strip()
    try:
        require(dist)
    except DistributionNotFound:
        required_to_install.append(dist)

test_required_to_install = []
for dist in test_requirements.readlines():
    dist = dist.strip()
    try:
        require(dist)
    except DistributionNotFound:
        test_required_to_install.append(dist)

data_dirs = []
for directory in os.walk('basic_cms/templates'):
    data_dirs.append(directory[0][10:] + '/*.*')

for directory in os.walk('basic_cms/media'):
    data_dirs.append(directory[0][10:] + '/*.*')

for directory in os.walk('basic_cms/static'):
    data_dirs.append(directory[0][10:] + '/*.*')

for directory in os.walk('basic_cms/locale'):
    data_dirs.append(directory[0][10:] + '/*.*')

url_schema = 'http://pypi.python.org/packages/source/d/%s/%s-%s.tar.gz'
download_url = url_schema % (package_name, package_name, basic_cms.__version__)


setup(
    name=package_name,
    test_suite='basic_cms.test_runner.build_suite',
    version=basic_cms.__version__,
    description=basic_cms.__doc__,
    author=basic_cms.__author__,
    author_email=basic_cms.__contact__,
    url=basic_cms.__homepage__,
    license=basic_cms.__license__,
    long_description=local_open('README.rst').read(),
    download_url=download_url,
    install_requires=required_to_install,
    tests_require=test_required_to_install,
    packages=find_packages(exclude=['example', 'example.*']),
    # very important for the binary distribution to include the templates.
    package_data={'basic_cms': data_dirs},
    #include_package_data=True, # include package data under svn source control
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: JavaScript',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
)
