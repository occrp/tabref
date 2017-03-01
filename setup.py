from setuptools import setup, find_packages


setup(
    name='tabref',
    version='0.1',
    description="Cross-referencing tool for tabular data (in databases or CSV)",
    long_description="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7'
    ],
    keywords='files databases matching crossreference ddj',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/occrp/tabref',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'test']),
    namespace_packages=[],
    package_data={},
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[
        'six',
        'click',
        'psycopg2',
        'sqlalchemy',
        'unicodecsv',
        'pyahocorasick',
        'normality',
        'fingerprints'
    ],
    tests_require=[
        'nose',
        'coverage',
    ],
    entry_points={
        'console_scripts': [
            'tabref = tabref.cli:main'
        ]
    }
)
