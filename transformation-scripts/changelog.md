# Changelog

### 2020/12/9 commit
Incorporate decode_values function + command line argument parser ([e0b0cdf](https://github.com/CaDatPitt/data-layers/commit/e0b0cdf77dce9cf28e6b90ae0d4563ac27ae9d52))

### 2020/9/15 commit
- Fix issues + clean up code + add documentation ([85a0dea9](https://github.com/CaDatPitt/data-layers/commit/85a0dea9589bc9717890f412c2c15ce72d1c6dc6#diff-106df2799d3d323a3f500ca1374c87a6))

### 2020/9/14 commit
- Fix malformed selectors + shorten keys + rename maps ([5dce2872](https://github.com/CaDatPitt/data-layers/commit/5dce2872f21c4b01f2b7a192d3720976ecb6d216))

### 2020/9/9 commit
- Update extract_base_layer.py ([d2b0b468](https://github.com/CaDatPitt/data-layers/commit/d2b0b468da737e05d027f8f7f0582a5b8d69e14f))

### 2019/9/13 commit
1. Any helper function that accepts a bs_object has to come during the previous for loop (or inside the function called there) because, at the end of that loop, a concatenated string built from the loop is the result. If we go back to the bs_object, that's the bs for the whole xml file. Meanwhile, the regex functions depend on the concatenated string, so they have to come later.
2. We have two types of mods files. Using 'lxml' as our parser (on my system at least) creates an object with <html><body></body></html> around the xml, and this parsed format won't support namespace queries. Instead, if we use the 'xml' setting, we get some files with namespaces and some without, so we need a redundancy to handle either case. Right now, the code doing this is really inelegant and probably not error proof.
3. To pass a dictionary of parameters to a function, we need to use **dictionary (we were missing the asterisks)
4. Fixed an error in one of the parameter dictionaries
5. Added a mods.xml file to test folder to create an example with a creator field
