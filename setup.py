#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read()

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
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points='''
        [console_scripts]
        drawtf=drawtf:main
    ''',
    install_requires=requirements,
    license="MIT license",
    include_package_data=True,
    keywords='drawtf,terraform,ci/cd,design,architecture,diagrams,graphviz',
    name='drawtf',
    packages=find_packages(),
    py_modules=['drawtf', 'app'],
    test_suite='tests',
    url='https://github.com/Aggreko/DrawTF',
    version='0.10.0',
    zip_safe=False,
)
