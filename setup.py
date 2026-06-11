from setuptools import setup

setup(
    name="filter203",
    version="0.1.0",
    license="MIT",
    author="Amy Parker <amy@amyip.net>, Adam Hahun Nam <adamhn1@uci.edu>",
    author_email="amy@amyip.net",
    url="https://github.com/amyipdev/203-filter",
    description="Custom network filtering/middleware architecture library",
    packages=["filter203"],
    include_package_data=True,
    setup_requires=["wheel"],
    python_requires=">=3.13"
)
