from setuptools import find_packages, setup

setup(
    name='py-zammad-cti',
    version='0.0.1',
    license="MIT",
    description='Zammad CTI interface',
    author='hmohammad',
    author_email='hmohammad2520@gmail.com',
    url='https://github.com/hmohammad2520-org/py-zammad-cti',
    install_requires=[
        'requests==2.32.4',
        'classmods==1.2.1'
    ],
    packages=find_packages(exclude=['test', 'test.*']),
    include_package_data=True,
    zip_safe=False,
)