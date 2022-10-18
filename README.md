# Pre-Processing of Data from the PhenoSys Touchscreen chamber 🐁

### Overview

__PhenoSys Touchscreen Chamber__

The [Touchscreen Chambers](https://www.phenosys.com/wp-content/uploads/2019/12/PhenoSys_Touchscreen_-Paradigms_1911.pdf) from [PhenoSys](https://www.phenosys.com/) contain a pellet dispenser and images/touch screens. 
These screens light up and need to be pressed in the correct order to receive a pellet as a reward. 
This apparatus has enabled the measurement of learning over time in novel models of disease in rodents.

<img src="https://user-images.githubusercontent.com/101311642/196097060-99574bb8-9cf9-4a9c-9c21-edfba42db3a5.png" width="300">

__Purpose__

The raw CSV output from the Touchscreen Chambers is large (~5 MB) and is highly time-consuming to process and obtain statistics of interest. This repository:
* Analyses the data from the paradigms GTPT2-5, 2VDLR, 5CSRTT and TUNL.
* Creates a colour-coded list of all key events in order of time.
* For each animal, these codes creates statistics about:
  * Individual sessions
  * Indvidual sessions split by stimulus durations and inter-trial intervals
  * Time bins over time
  * Snips videos for each experiment into many session clips

__Preview of the graphical user interfaces__

![image](https://user-images.githubusercontent.com/101311642/196102050-8d7635e5-393e-477e-942c-7ce0e00156b4.png)

__Input and output data__

![image](https://user-images.githubusercontent.com/101311642/161454721-6b105f0d-89f3-465c-80c1-d6dc3addc63b.png)

![image](https://user-images.githubusercontent.com/101311642/161454729-8e956896-f9ca-403c-8f6d-c402f6ada5b6.png)

### Installation

Install [Anaconda Navigator](https://www.anaconda.com/products/distribution). <br>
Open Anaconda Prompt (on Mac open terminal and install X-Code when prompted). <br>
Download this repository to your home directory by typing in the line below.
```
git clone https://github.com/Foldi-Lab/PhenoSys-codes.git
```
If you receive an error about git, install git using the line below, type "Y" when prompted and then re-run the line above.
```
conda install -c anaconda git
```
Change the directory to the place where the downloaded folder is. <br>
```
cd PhenoSys-codes
```

Create a conda environment and install the dependencies.
```
conda env create -n PSC -f Dependencies.yaml
```

### Usage
Open Anaconda Prompt (on Mac open terminal). <br>
Change the directory to the place where the git clone was made.
```
cd PhenoSys-codes
```

Activate the conda environment.
```
conda activate PSC
```

Run the codes.
```
python PhenoSys.py
```

### Guide

View the guide about [how to analyse your PhenoSys data](How_to_use_PhenoSys_codes.pdf).

<br>

### Acknowledgements

__Author:__ <br>
[Harry Dempsey](https://github.com/H-Dempsey) (Andrews lab and Foldi lab) <br>

__Credits:__ <br>
Laura Milton, Stephen Power, Claire Foldi, Zane Andrews, Kaixin Huang, Kyna Conn, Sarah Lockie, Karsten Krepinsky <br>

__About the labs:__ <br>
The [Foldi lab](https://www.monash.edu/discovery-institute/foldi-lab) investigates the biological underpinnings of anorexia nervosa and feeding disorders. <br>
The [Andrews lab](https://www.monash.edu/discovery-institute/andrews-lab) investigates how the brain senses and responds to hunger. <br>
