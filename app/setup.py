from setuptools import setup

setup(
    name='app',
    packages=['Dashboard'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)