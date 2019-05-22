from setuptools import find_packages, setup

import meetup

setup(
    name="meetup",
    version=meetup.__version__,
    packages=find_packages(exclude=['docs*', 'tests*']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "core4 @ git+https://github.com/plan-net/core4.git"
    ]
)