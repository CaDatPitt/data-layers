# Overview

## Base Layer Scripts
### data_layers_config.py
  - **Description**: Configuration file containing mappings between base layer fields and BeautifulSoup selectors for EAD, MODS, and RELS-EXT (RDF)
  - **Usage**: Imported in extract_base_layer.py script
### decode_values.py
  - **Description**: Script for decoding encoded values in data layer columns (i.e., 'collection_language', 'language', and 'geographic_coverage')
  - **Usage**: Can be used to modify any data layer CSV/Excel file (requires absolute path); a modified version is included as a function in extract_base_layer.py script
### encoding_schemes.py
  - **Description**: Dictionary of encoding schemes containing mappings between codes and names
  - **Usage**: Imported in by extract_base_layer.py script
### extract_base_layer.py
  - **Description**: Main script for extracting and transforming source data to create base layer files
  - **Usage**: Used to transform source data into base layers

## Extension Layer Scripts
### tf-extension-layers.ipynb
  - **Description**: Analyzes base layers to determine term frequencies
<!-- - **Extension Layer(s)**:
   - [american-left-ephemera/tagged_genres](https://github.com/CaDatPitt/data-layers/tree/master/extension-layers/american-left-ephemera/tagged_genres)
   -->
### Join-Genres-with-BaseLayer.ipynb**
  - **Description**: Joins extension layers (tagged genres) with base layers
 <!-- - **Extension Layer(s)**: -->

## Documentation
- **changelog.md**
- **LICENSE**
- **requirements.txt**
