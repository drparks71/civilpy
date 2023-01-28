from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='civilpy',
    version='0.0.17',
    description='Civil Engineering Tools in Python',
    url="https://daneparks.com/Dane/civilpy",
    author_email="Dane@daneparks.com",
    author="Dane Parks",
    py_modules=[
        "civilpy",
        "civilpy.state.ohio",
        "civilpy.structural",
        "civilpy.construction",
        "civilpy.environmental",
        "civilpy.general",
        "civilpy.geotechnical",
        "civilpy.state",
        "civilpy.transportation",
        "civilpy.water_resources"
    ],
    package_dir={'civilpy': 'civilpy'},
    packages=[
        "civilpy.structural",
        "civilpy.construction",
        "civilpy.environmental",
        "civilpy.general",
        "civilpy.geotechnical",
        "civilpy.state",
        "civilpy.state.ohio",
        "civilpy.transportation",
        "civilpy.water_resources"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console :: Curses",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy>=1.22.3",
        "folium>=0.12.1",
        "pandas>=1.4.2",
        "Pillow>=9.4.0",
        "Pint>=0.19.2",
        "matplotlib>=3.6.3",
        "jupyter>=1.0.0",
        "Flask>=2.2.2",
        "PyPDF2>=3.0.1",
        "simplekml>=1.3.6",
        "beautifulsoup4>=4.11.1",
        "psycopg2-binary>=2.9.5",
        "sshtunnel>=0.4.0",
        "icalendar>=4.0.7",
        "html5lib>=1.1",
        "geopandas>=0.12.2",
        "fiona>=1.8.22",
        "tifftools>=1.3.7",
        "natsort>=8.2.0",
        "html5lib>=1.1",
        "requests>=2.28.2"
    ],

    extras_require={
        "dev": [
            "pytest>=3.7",
            "jupyter>=1.0.0",
        ]
    }
)
