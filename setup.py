from setuptools import setup, find_packages

setup(
  name="Global-F1-Battle-2024",
  version="0.1.0",
  description="Library for the interactive F1 Fantasy Dashboard",
  include_package_data=True,
  package_data={"": ["gitignore.txt"]},
  install_requires=[
    "numpy",
    "pandas",
  ],
)
