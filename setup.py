from setuptools import setup, find_packages

setup(
    name="adaptive-dbscan",
    version="0.3.1",
    description="A python package for density adaptive DBSCAN clustering",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Sina Sabermahani",
    author_email="sina.sabermahani@gmail.com",
    url="https://github.com/Sinamahani/AdaptiveDBSCAN",
    license=open('LICENSE').read(),
    packages=find_packages(),
    install_requires=[
        'numpy>=1.26.0',
        'geopandas>=0.14.0',
        'pandas>=2.1.1',
        'matplotlib>=2.2.0',
        'pyproj>=3.6.1',
        'scipy>=1.11.3']
    
    
)
