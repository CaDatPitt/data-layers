# Changelog

### 9/13/2019 commit 

1. Any helper function that accepts a bs_object has to come during the previous for loop (or inside the function called there) because, at the end of that loop, a concatenated string built from the loop is the result. If we go back to the bs_object, that's the bs for the whole xml file. Meanwhile, the regex functions depend on the concatenated string, so they have to come later.
2. We have two types of mods files. Using 'lxml' as our parser (on my system at least) creates an object with <html><body></body></html> around the xml, and this parsed format won't support namespace queries. Instead, if we use the 'xml' setting, we get some files with namespaces and some without, so we need a redundancy to handle either case. Right now, the code doing this is really inelegant and probably not error proof. 
3. To pass a dictionary of parameters to a function, we need to use **dictionary (we were missing the asterisks)
4. Fixed an error in one of the parameter dictionaries
5. Added a mods.xml file to test folder to create an example with a creator field
