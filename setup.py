from setuptools import setup, find_packages

setup(
    name="test-reader",
    version="1.0.2",
    url="https://github.com/amandaquaglio/test-reader",
    author="Amanda Quaglio",
    author_email="amandacq@yahoo.com.br",
    scripts=['bin/test-reader-start'],
    include_package_data=True,
    description="A Test reader based on yaml config to export test cases and its test types",
    packages=find_packages(),
    install_requires=[
        "google-auth",
	    "google-api-python-client"
    ]
)
