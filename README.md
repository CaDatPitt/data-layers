# Using the CaD@Pitt Data Layers Repository

Welcome to the CaD@Pitt Data Layers Repository! This repository hosts primarily collections data, datasets and data extraction/transformation scripts.

## Directories
This repository comprises the following directories:
* **base-layers**: curated datasets derived from library metadata records
* **extension-layers**: datasets that extend/enrich base layers
* **source-data**: snapshots of library metadata records
* **transformation-scripts**: Python scripts for extracting and transforming data from library metadata records

The “base-layers,” “extension-layers” and “source-data” directories each contain subdirectories, organized by collection. Subdirectories under “source-data” contain third-level directories, organized by metadata schema. Subdirectories under “extension-layers” contain third-level  directories organized by project.

## Data Dictionary
The [CaD@Pitt Data Dictionary](data-dictionary/04-data-dictionary.md) defines and describes the data layers in this repository, including the project’s related controlled vocabularies and encoding schemes, metadata element sets, and application profiles.

## Download or Clone the Repository
Because the Data Layers Repository is published on GitHub, you have different options for accessing its content. Determining which method will likely depend on how you plan to use the data and scripts.

### **Download the Repository Contents**
If you are most interested in working with the base layers and/or extension layers that are published in the repository, *downloading* the repository is the easiest way to do so. From the [Data Layers Repository](https://github.com/CaDatPitt/data-layers) main page, look for the green button, just above the file list, labeled "Code." Click on this button and then look for the link that reads "Download Zip." This option will give you a bundled Zip file that will decompress into an exact copy of the directories and files in the GitHub repository. You'll find base layers in the "base-layers" directory, extension layers in the "extension-layers" directory, and so on.

One detail to note about the download option: it gives you a snapshot of the repository contents at that moment in time. If you are interested in working with any updates or additions to the content in the repository, you will have to repeat the download process again later, and manually merge the new files into your workspace, if necessary.

### **Clone the Repository**
If you are interested in keeping your copy of the repository synced to the source, and/or plan on creating your own version of the entire Data Layers publishing framework within git or GitHub, you may wish to clone the repository.

If you are new to git or GitHub, the term "clone" may sound (understandably) strange. In git and GitHub, a [*clone*](https://docs.github.com/en/github/getting-started-with-github/github-glossary#clone) is a special copy of a repository. Like a download, it obtains a complete copy of the repository for your local computer. However, unlike a simple download, which is disconnected from the source repository, a clone maintains the connection back to its source. It is then possible to [*pull*](https://docs.github.com/en/github/getting-started-with-github/github-glossary#pull) down changes from the remote repository and merge them into your local copy, or [*push*](https://docs.github.com/en/github/getting-started-with-github/github-glossary#push) changes that you have made locally back to a repository on GitHub.

If you plan to develop your own custom version of the Data Layers framework, rather than only syncing with the CaD@Pitt repository, you may wish to [*fork*](https://docs.github.com/en/github/getting-started-with-github/github-glossary#fork) the repository, which is similar to a clone but makes a separate personal copy for you to modify.

To clone the repository requires having git or GitHub Desktop installed on your local computer. That configuration is beyond the scope of this documentation, but there is plenty of guidance [elsewhere](https://docs.github.com/en/github/getting-started-with-github/set-up-git). Once this is configured, you will look for the green "Code" button on the Data Layers Repository, and then choose "Clone" via SSH or GitHub Desktop.

## Creating Base Layers
If you would like to extract data from source data (XML files) and transform them into base layers (CSV files), see the [Data Extraction and Transformation Workflow](https://github.com/CaDatPitt/documentation/blob/master/05-data-extraction-and-transformation-workflow.md) documentation for instructions.
