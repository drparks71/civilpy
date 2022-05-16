# CivilPy

![PyPI - License](https://img.shields.io/pypi/l/civilpy)
<img alt="Project badge" aria-hidden="" class="project-badge" src="https://daneparks.com/Dane/civilpy/badges/master/pipeline.svg">
<img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/civilpy">
<img alt="Project badge" aria-hidden="" class="project-badge" src="https://daneparks.com/Dane/civilpy/badges/master/coverage.svg">
![PyPI - Downloads](https://img.shields.io/pypi/dm/CivilPy)


# [Source Code](https://daneparks.com/Dane/civilpy)

Code snippets for Civil Engineering related tasks

## About (Skip to the "Installation" section to start running code)

Welcome to the CivilPy repository.  This is a simple software package to give civil engineers cleaner access
to some of the packages from the python ecosystem.  The package is focused on civil engineering related tasks such as 
file management, pdf data extraction, image manipulation mapping and unit conversions.  I did my best to make the user 
interface obvious to use and tried to keep the functionality compatible with tools available to the average Civil 
engineer.

## Intro

This repository was created in order for me to gain a better understanding of software development work flows and how they can be
re-purposed for civil engineering related tasks.  This is by no means a comprehensive or even functional repository but 
is more a way for me to track my progress while learning more about another industry.  There may occasionally be how-tos
and other code posted here but this repository is not meant as tutorial or in depth explanation for how coding works. 
For those types of things I highly suggest you instead check <a href=https://www.youtube.com/>Youtube</a> for general 
lessons or <a href=https://stackoverflow.com/>Stack Overflow</a> for specific issues.  I highly recommend the 
<a href=https://www.youtube.com/user/cs50tv>Harvard CS50 YouTube Channel</a> for conceptual level programming lessons or
<a href=https://www.youtube.com/user/schafer5>CoreyMS's Youtube Channel</a> for lessons in practical uses of 
programming. 

For an interesting somewhat working examples see the files `Useful Tricks and Tools.ipynb` and `NBI STandards - Conversion`
files to have a better understanding of what function the DOT/SNBI files are performing. 

## Installation

Run the following code to install the package:

```bash
$ pip install civilpy
```

## Usage

to check the package installed correctly, run:

```python
from civilpy.structural.steel import hello_world

# Test the function imported successfully
hello_world()
```

```python
from civilpy.structural.steel import W

# Load a W steel section as a python object
W40X390 = W("W40X390")
W40X390.A
```

# How to determine where to store functions within the package

Here is the decision tree for function organization within the package, the goal
is to keep importing and running functions as simple as possible for non-programmers,
while maintaining an organizational structure capable of supporting many tools.

i.e., the end user should be able to access any of your functions from a simple import:

```python
from civilpy.state.ohio.dot import help_function
```

<div class="center">

```mermaid
graph TD
    A[Does the function more relate to a particular state<br> requirement/system, or a branch of Civil Engineering?] --> |State| B("Does it apply state wide <br> or a specific department?")
    A --> |Branch| C("Which branch does it most closely fit? ")
    C --> |construction| D(Save under <br> civilpy.construction)
    C --> |structural| E(Save under <br> civilpy.structural)
    C --> |geotechnical| F(Save under <br> civilpy.geotechnical)
    C --> |environmental| G(Save under <br> civilpy.environmental)
    C --> |transportation| H(Save under <br> civilpy.transportation)
    C --> |water_resources| I(Save under <br> civilpy.water_resources)
    A --> |Neither| P
    D --> K("Is it related to a particular standard, (i.e. AASHTO)")
    E --> K
    F --> K
    G --> K
    H --> K
    I --> K
    B --> |Statewide| L("civilpy.[state].__init__.py")
    B --> |Department| M("civilpy.[state].department")
    K --> |Yes| N("Save under a file for the standard<br>i.e. civilpy.structural.aisc")
    K --> |No| O("save to the relevant __init__.py")
    P("Save under civilpy.general.[relevant_file]")
    N --> |Doesn't make sense to put it there| P
    O --> |Doesn't make sense to put it there|P
```
</div>
