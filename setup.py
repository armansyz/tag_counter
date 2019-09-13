import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tag_counter_armansyz",
    version="0.0.5",
    author="Arman Syzdykov",
    author_email="syzdykov.arman@gmail.com",
    description="Package for the python beginners course",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/armansyz/python_task",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
          'app_launcher': [
              'tag_counter = tag_counter.tag_counter:main'
          ]
      },
    test_suite='tests',
)
