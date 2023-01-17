## About these datasets

Base layers are curated datasets (CSV files) derived and simplified from the source data layers, as defined and described by the [data dictionary](https://cadatpitt.github.io/documentation/04-data-dictionary) and the [application profiles](https://cadatpitt.github.io/documentation/data-dictionary/application-profiles.html).

Each subfolder represents either a University of Pittsburgh Library System (ULS) [digital collection](https://digital.library.pitt.edu/) or a scholar-created subcollection deriving from ULS collections or the Library catalog. In each location, you will find two csvs, ```collection-base-layer.csv``` for collection-level metadata, and ```item-base-layer.csv``` for item-level metadata.  

### Known Issues
- Some records are missing the identifier (```'id'```) in the CSV. The identifier can be found in the source data's filename. Use other data to locate the appropriate file in its collection directory.
- The date fields will often have two years, separated with a forward-slash, like this: ```"1949/1984"```. In these cases, the start year is typically the earliest date for the entire collection, and the second date is the latest date for the entire collection. In other words, ```"year/year"``` is effectively a placeholder for ```"unknown"```.
