# Geoparsing Pliny the Elder's Natural History

* The **Geoparsing Pliny Natural History** is the first workpackage of my FWO PhD project 'Greek Spaces in Roman Times' that aims at analyzing the geographic description of Greece in Pliny's encyclopedia. The scope of this package is to identify place names in the NH and disambiguate them by stable IDs through an external knowledge base.

## Authors 
* Laura Soffiantini, KU Leuven, [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0003-4932-7912) https://orcid.org/0000-0002-7991-0466

## Installation: Virtual Environment 

The Geoparser is developed for Python 3.12. To install you need a Virtual Environment, which can be set up following these instructions: 
- Make sure you have Python 3.12 installed, it should be available for all users and needs to be added to the system path for ease of use. On managed computers Python should be installed in ```C:\Workdir\MyApps\python``` by a user with local admin-rights.
- Download and deploy this GitHub repository (e.g.: ```C:\Workdir\MyApps\python_venvs\geoparser```).
- Open PowerShell as a Local Administrator and navigate to the folder where you deployed this repository. Type: ```python -m venv . activate``` this environment by going to ```Scripts\activate```.
When activated the name of the virtual environment should be shown in front of the path in your PowerShell Window. Install the required modules: ```pip install -r requirements.txt```

## Usage

The repository contains the code to extract annotations from ToposText (https://topostext.org), an online repository of Classical texts in translation, perform flairNER and merge the annotations. Using VecAlign in combination of LABSE, SimAlign in combination with UGARIT-gr the pipeline allows to trasnfer the annotation from the English translation back to the Latin original text.
