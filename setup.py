from setuptools import setup
from setuptools import find_packages

setup(
    name='auth_page',
    version='1.0.0',
    author='Kristoffer Snabb',
    url='https://github.com/geonition/auth_page',
    packages=find_packages(),
    include_package_data=True,
    package_data = {
        "auth_page": [
            'templates/*',
            'static/css/*.css'
        ],
    },
    zip_safe=False,
    install_requires=['django',
                      'django-social-auth']
)
