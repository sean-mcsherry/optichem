from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='optichem',
    version='1.0.0',
    description='Optical properties from ATR measurements',
    long_description=readme,
    long_description_content_type='text/markdown',
    install_requires=[
        "numpy>=1.20.1",
        "scipy>=1.6.0",
        "pandas>=1.2.1",
        "matplotlib>=3.3.3",
        ,
        ],
    author='Sean McSherry',
    author_email='mcsherry@umich.edu',
    url='https://github.com/sean-mcsherry/optichem',
    license="MIT",
    packages=find_packages(exclude=('tests', 'docs', 'tutorials')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Topic :: Scientific/Engineering",
    ],
    python_requires='>=3.6',
    project_urls={
        'Documentation': 'https://github.com/sean-mcsherry/optichem.wiki.git',
        'Research group': 'https://lenert.engin.umich.edu/',
        'Source': 'https://github.com/sean-mcsherry/optichem',
    },
    
)
