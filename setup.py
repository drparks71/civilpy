from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="civilpy",
    version="0.1.12",
    packages=find_packages(
        "src", exclude=["tests", "Notebooks", "secrets", "docs", "res"]
    ),
    description="Civil Engineering Tools in Python",
    url="https://daneparks.com/Dane/civilpy",
    author_email="Dane@daneparks.com",
    author="Dane Parks",
    license='AGPL-V3',
    include_package_data=True,
    package_data= {'civilpy': ['structural/res/*.csv']},
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
        "civilpy.general.software",
        "civilpy.structural.beam_bending",
        "civilpy.structural.search_tools",
        "civilpy.structural.steel",
        "civilpy.structural.midas",
        "civilpy.water_resources.hydraulics",
        "civilpy.CLI",
        "civilpy.kivy",
    ],
    package_dir={"": "src"},
    classifiers=[
        'Development Status :: 4 - Beta',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "numpy>=2.0.2",
        "folium>=0.12.1",
        "pandas>=1.1.5",
        "Pillow>=10.2.0",
        "Pint>=0.12.2",
        "coverage>=7.1.0",
        "webdriver-manager>=3.8.5",
        "msedge-selenium-tools>=3.141.4",
        "Flask>=2.2.2",
        "PyPDF2>=3.0.1",
        "beautifulsoup4>=4.11.1",
        "sympy>=1.10.0",
        "sshtunnel>=0.4.0",
        "termcolor>=1.1.0",
        "icalendar>=4.0.7",
        "html5lib>=1.1",
        "geopandas>=0.6.2",
        "fiona>=1.8.22",
        "tifftools>=1.3.7",
        "natsort>=8.2.0",
        "html5lib>=1.1",
        "requests>=2.28.2",
        "pyntcloud>=0.3.1",
        "openpyxl>=3.1.2",
        "tqdm>=4.65.0",
        "pytesseract>=0.3.10",
        "pytest>=7.4.1",
    ],
    extras_require={
        "full": [  # Holds all the packages that aren't "Pure Python"
            "matplotlib>=3.6.3",
            "selenium>=3.141.0",
            "msedge-selenium-tools>=3.141.4",
            "jupyter>=1.0.0",
            "PyMuPDF>=1.23.7",
            "simplekml>=1.3.6",
            "psycopg2-binary>=2.9.5",
            "sympy>=1.10.0",
            "latex>=0.7.0",
            "laspy>=2.4.1",
            "earthpy>=0.9.4",
            "pymupdf>=1.22.3",
            "pyodbc>=4.0.39",
            "kivymd>=1.1.1",
            "PyQt5>=5.15.9",
            "tox>=4.11.1",
            "markdownify>=0.13.1",
            "pytest-cov>=4.1.0",
        ]
    },
)
