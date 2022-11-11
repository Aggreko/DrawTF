#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['Click>=7.0', 'diagrams==0.22.0']

test_requirements = ['pytest>=3', ]

setup(
    author="Aggreko",
    author_email='michael.law@aggreko.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
    description="Draw diagrams from tf state files",
    entry_points={
        'console_scripts': [
            'drawtf=drawtf.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='drawtf,terraform,ci/cd,design,architecture,diagrams,graphviz',
    name='drawtf',
    packages=find_packages(include=['drawtf', 'drawtf.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/Aggreko/DrawTF',
    version='0.1.0',
    zip_safe=False,
)
