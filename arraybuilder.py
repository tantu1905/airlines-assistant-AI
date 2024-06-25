import re


def build_array():
# Function to extract IATA codes from a line
    def extract_iata_codes(line):
        # Regular expression to match IATA codes (3 uppercase letters)
        return re.findall(r'\b[A-Z]{3}\b', line)

    # Path to the text file
    file_path = 'yaz.txt'

    # Initialize an empty list to store IATA codes
    iata_codes = []

    # Open the file and read lines
    with open(file_path, 'r') as file:
        for line in file:
            codes = extract_iata_codes(line)
            iata_codes.extend(codes)

    # Remove duplicates by converting the list to a set and back to a list
    unique_iata_codes = list(set(iata_codes))

    # Function to return IATA codes as an array
    def get_iata_codes():
        return unique_iata_codes

    # Example usage
    iata_codes_array = get_iata_codes()
    return iata_codes_array
    print(iata_codes_array)
    
#print(build_array())
