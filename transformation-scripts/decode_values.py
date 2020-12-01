import encoding_schemes
import os
import sys
import pandas as pd

def decode(file_location, specified_column):
    """
    Replaces encoded values in the specified dataset column(s) with the corresponding decoded values,
    then writes decoded dataset to a new CSV file if any values were decoded.

    Parameters
    ----------
    file_location: str
        a location or absolute path of the file to be used
    specified_column: str
        a column name, as it appears in the file, containing the encoded values to be decoded

    Returns
    -------
    None

    Raises
    ------
    Exception: File location [file_location] not found!
    Exception: File type [extension] not supported!
    Exception: Column [column] not found in dataset!
    """

    # validate file location
    if not os.path.exists(file_location):
        raise Exception ("File location %s not found!" % (file_location,))

    # store and validate file extension and create DataFrame from file if valid
    extension = os.path.splitext(file_location)[1]
    if extension == '.csv':
        df = pd.read_csv(file_location, encoding="utf-8")
    elif extension in ['.xls', '.xlsx', '.xlsm', '.xlsb', '.odf', '.ods', '.odt']:
        df = pd.read_excel(file_location, encoding="utf-8")
    else:
        raise Exception ("File type '%s' not supported!" % (extension,))

    # pre-process and decode fields in specified column(s)
    if specified_column == 'all':
        # decode all listed encoded columns and keep count of all evaluated and decoded values
        encoded_columns = ['language', 'geographic_coverage']
        total_value_count = 0
        total_decoded_value_count = 0
        for column in encoded_columns:
            [df, value_count, decoded_value_count] = decode_columns(df, column)
            total_value_count += value_count
            total_decoded_value_count += decoded_value_count
        print(str(total_decoded_value_count) + " out of " + str(total_value_count) + " total values decoded in all encoded columns.")
    else:
        # validate column name and decode column if valid
        if specified_column not in df.columns:
            raise Exception ("Column '%s' not found in dataset!" % (specified_column,))
        [df, total_value_count, total_decoded_value_count] = decode_columns(df, specified_column)

    # write decoded DataFrame to CSV if any values were decoded
    if total_decoded_value_count > 0:
        updated_suffix = '_' + specified_column + '_decoded.csv'
        outfile_location = file_location.replace(extension, updated_suffix)
        outfile = open(outfile_location, 'w', encoding="utf-8", newline='')
        outfile.write(df.to_csv())
        outfile.close()
        print("Output file: " + outfile_location + "\nComplete!")
    else:
        print("No file was created.\nComplete!")

    return

def decode_columns(df, specified_column):
    """
    Helper function that pre-processes values in the specified dataset column, then replaces encoded values
    with the corresponding decoded values in an encoding scheme dictionary.

    Parameters
    ----------
    df: pandas.core.frame.DataFrame
        a dataset with one or more columns to be decoded
    specified_column: str
        a column name, as it appears in the file, containing the encoded values to be decoded

    Returns
    -------
    df: pandas.core.frame.DataFrame
        a dataset with columns that have been decoded or, at least, evaluated for decoding
    value_count: int
        number of values in the specified column
    decoded_value_count: int
        number of decoded values in the specified column
    """

    # build dictionary from appropriate encoding schemes for column
    encoded_columns = {
    'language': ['iso639-2b'],
    'geographic_coverage': ['marccountry', 'marcgac']
    }
    encoding_dict = {}

    for column_key in encoded_columns:
        if specified_column == column_key:
            for encoding_scheme in encoded_columns[column_key]:
                encoding_dict.update(encoding_schemes.LIST[encoding_scheme])

    # pre-process specified column in DataFrame and replace encoded field values with decoded values from encoding dictionary
    value_count = 0
    decoded_value_count = 0

    for i in df.index:
        field_data = df.at[i, specified_column]
        field_list = []
        decoded_field_list = []
        if isinstance(field_data, str):
            field_list = (field_data).split('|||')
            for value in field_list:
                processed_value = value.strip('-\n\t ').lower() # remove trailing dashes and white spaces to match values in encoding dictionaries, esp. marcgac and marccountry
                decoded_value = ""
                value_count += 1
                for key in encoding_dict.keys():
                    if processed_value == key:
                        decoded_value = processed_value.replace(key, encoding_dict[key])
                        decoded_value_count += 1
                        break
                    else:
                        decoded_value = value
                decoded_field_list.append(decoded_value)
        df.at[i, specified_column] = "|||".join(set(decoded_field_list))

    print(str(decoded_value_count) + " out of " + str(value_count) + " values decoded in '" + specified_column + "' column.")

    return df, value_count, decoded_value_count

# call main function
if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("When running as a script, you must provide two arguments: file location and specified column.")
    decode(sys.argv[1], sys.argv[2])
