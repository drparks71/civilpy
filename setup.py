from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='civilpy',
    version='0.0.30',
    packages=find_packages('src', exclude=['test', 'secrets', 'docs', 'res']),
    description='Civil Engineering Tools in Python',
    url="https://daneparks.com/Dane/civilpy",
    author_email="Dane@daneparks.com",
    author="Dane Parks",
    py_modules=[
        "civilpy.state.ohio.dot",
        "civilpy.state.ohio.snbi",
        "civilpy.general.database_tools",
        "civilpy.general.gis",
        "civilpy.general.kml_tools",
        "civilpy.general.math",
        "civilpy.general.microstation",
        "civilpy.general.pdf",
        "civilpy.general.photos",
        "civilpy.general.physics",
        "civilpy.general.plan_development",
        "civilpy.general.pointclouds",
        "civilpy.structural.beam_bending",
        "civilpy.structural.search_tools",
        "civilpy.structural.steel",
        "civilpy.water_resources.hydraulics",
        "civilpy.CLI"
    ],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console :: Curses",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy>=1.14.5",
        "folium>=0.12.1",
        "pandas>=1.1.5",
        "Pillow>=9.4.0",
        "Pint>=0.18.2",
        "coverage>=7.1.0",
        "matplotlib>=3.6.3",
        "webdriver-manager>=3.8.5",
        "selenium>=3.141.0",
        "msedge-selenium-tools>=3.141.4",
        "jupyter>=1.0.0",
        "Flask>=2.2.2",
        "PyPDF2>=3.0.1",
        "simplekml>=1.3.6",
        "beautifulsoup4>=4.11.1",
        "psycopg2-binary>=2.9.5",
        "sympy>=1.10.0",
        "sshtunnel>=0.4.0",
        "icalendar>=4.0.7",
        "latex>=0.7.0",
        "html5lib>=1.1",
        "geopandas>=0.6.2",
        "fiona>=1.8.22",
        "tifftools>=1.3.7",
        "natsort>=8.2.0",
        "html5lib>=1.1",
        "requests>=2.28.2",
        "pyntcloud>=0.3.1",
        "laspy>=2.4.1"
    ],

    extras_require={
        "dev": [
            "pytest>=3.7",
            "pytest-cov>=4.0.0",
            "jupyter>=1.0.0",
        ]
    }
)
