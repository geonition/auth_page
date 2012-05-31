from setuptools import setup
from setuptools import find_packages

setup(
    name='auth_page',
    version='4.0.4',
    author='Kristoffer Snabb',
    url='https://github.com/geonition/auth_page',
    packages=find_packages(),
    include_package_data=True,
    package_data = {
        "auth_page": [
            'templates/*',
            'static/css/*.css',
            "locale/*/LC_MESSAGES/*.mo",
            "locale/*/LC_MESSAGES/*.po"
        ],
    },
    zip_safe=False,
    install_requires=['django']
)
