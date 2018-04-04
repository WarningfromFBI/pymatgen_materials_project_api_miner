# pymatgen api_miner/feature scraper
This repositories serves two key functionalities:  
One is to use the Materials Project API to pull down the data from the Materials project AND
the Battery Explorer.  
The second is series of functions to mine the pulled data into the training/test data and deployment data
for use in ML models  
the primary output are a csv file of the features and a csv files of the labels used in our paper:

note that to use these scripts, you must have an account on Materials Project (free) so you can generate your own MAPI key
(if you find my MAPI key on my scripts, please let me know.

## requirements
pymatgen 2.0 -- structure miner is completely dependent on this module

## folder structure


## mining the api extracted data
In general, using the api to query the data over an internet connection is slow, so we want to mine everything 
into a local set of folders so we can use efficiently  
there is an additional set of functions which further mines the raw database to generate features and labels
for battery machine learning, which is a separate repository you can check to see state of the art machine learning algorithms

## database_reader_functions
compilation of functions designed to read data from the databases mined by the api-miners
materials_project_reader:  reads .json formatted text files  
NOTE that a structure base reader isn't included. Since the contents of the structure base are just pickled python objects   
simple object, pickle.loads(file) is sufficient

## csv_processed_datasets
csv is important because ONLY csv files  
we include a folder called data-dump where I usually put in all the .csv files which are successfully mined from the data-miner
these files should be transferred to the battery machine learning repo for further analysis. we want to keep things as compartmentalized as possible

## FeatureLabelMining
Idea to have separate scripts for different features is simple. First, we can classify different features
Second, different types of features may be more or less expensive to compute


# scripts
contains two folders, one which focuses on the Materials Project, one which focuses on the Battery Explorer

## Battery API Miner Folder
one script which queries the Battery Explorer and mines them to a text file in a directory that has the default name: Battery_Explorer

## Materials API Miner Folder
two core scripts 
- one which mines materials data and structure data to json format in one file each (Materials_Project_Database)  
- second one mines the structure into a pymatgen structure object, stored as a pickle file (structure_base)

## Data Scraping
performs all feature construction 