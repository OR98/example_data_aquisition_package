import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "example_data_aquisition_package",
    version = "0.0.1",
    author = "OR98",
    author_email = "r.ouhmiz@gmail.com",
    description = "Package containing data aquisition modules.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(),
    url = "https://test.pypi.org/project/_example_data_aquisition_package/",
    project_urls = {
        "Bug Tracker": "https://github.com/OR98/example_data_aquisition_package/issues",
        "repository": "https://github.com/OR98/data_aquisition_package"
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)