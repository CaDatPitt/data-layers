import argparse
import encoding_schemes
import os
import sys
import pandas as pd

def decode_values(file_location):
    """
    Replaces encoded values in the specified dataset column(s) with the corresponding decoded values,
    then writes decoded dataset to a new CSV file if any values were decoded.

    Parameters
    ----------
    file_location: str
        a location or absolute path of the file to be used

    Returns
    -------
    None

    Raises
    ------
    Exception: File location [file_location] not found!
    Exception: File type [extension] not supported!
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
    encoded_columns = {
    'collection_language': ['iso639-2b'],
    'language': ['iso639-2b'],
    'geographic_coverage': ['marccountry', 'marcgac']
    }
    encoding_dict = {}
    total_decoded_value_count = 0

    for column in encoded_columns.keys():
        # build dictionary from appropriate encoding schemes for column
        for encoding_scheme in encoded_columns[column]:
            encoding_dict.update(encoding_schemes.LIST[encoding_scheme])

        # pre-process and decode fields in column and keep count of total and decoded values
        value_count, decoded_value_count = 0, 0
        if column in df.columns:
            for i in df.index:
                field_data = df.at[i, column]
                field_list = []
                decoded_field_list = []
                if isinstance(field_data, str):
                    field_list = (field_data).split('|||')
                    for value in field_list:
                        processed_value = value.strip('-\n\t ').lower()
                        decoded_value = ""
                        if value != "":
                            value_count += 1
                        for code in encoding_dict.keys():
                            if processed_value == code:
                                decoded_value = processed_value.replace(code, encoding_dict[code])
                                decoded_value_count += 1
                                break
                            else:
                                decoded_value = value
                        decoded_field_list.append(decoded_value)
                df.at[i, column] = "|||".join(set(decoded_field_list))
            total_decoded_value_count += decoded_value_count

            # report counts of evaluated values and decoded values in column
            print(str(decoded_value_count) + " out of " + str(value_count) + " values decoded in '" + column + "' column.")

    # write decoded DataFrame to CSV if any values were decoded
    if total_decoded_value_count > 0:
        outfile_location = file_location.replace(extension, '_decoded.csv')
        outfile = open(outfile_location, 'w', encoding="utf-8", newline='')
        outfile.write(df.to_csv(index=False))
        outfile.close()
        print("Output file: " + outfile_location + "\nComplete!")
    else:
        print("No file was created.\nComplete!")

    return

def parse_arguments():
    """
    Parses command line arguments.

    Parameters
    ----------
    None

    Returns
    -------
    args: dict
        dictionary of arguments
    """
    # Create argument parser
    parser = argparse.ArgumentParser(
        prog="decode_values",
        description="Replaces encoded values in the specified dataset column(s) with the corresponding decoded values, then writes decoded dataset to a new CSV file if any values were decoded.",
        epilog="To run the script, your command should be input as follows: python decode_values.py [location]"
        )
    # Positional mandatory arguments
    parser.add_argument("file_location", help="location or absolute path of the file to be used", type=str)

    # Parse arguments
    args = parser.parse_args()

    return args

# call main function
if __name__ == '__main__':
    # parse the arguments
    args = parse_arguments()
    # raw print arguments
    print("You are running the script with the following arguments:")
    for a in args.__dict__:
        print("  *" + str(a) + ": " + str(args.__dict__[a]))
    # run function
    decode_values(args.file_location)
