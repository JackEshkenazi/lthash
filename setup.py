from setuptools import setup, find_packages

setup(
    name='lthash',  # Package name
    version='0.1.0',  # Package version
    author='Jack Eshkenazi',
    author_email='noreply@example.com',
    description='A lightweight homomorphic, commutative hash implementation',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JackEshkenazi/lthash',
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
