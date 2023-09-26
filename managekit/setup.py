from setuptools import setup, find_packages

setup(
    name='django-autoseeder',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Django>=3.0',
    ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)

# autoseed/setup.py