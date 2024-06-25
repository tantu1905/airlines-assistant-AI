import requests
from bs4 import BeautifulSoup
import re
def build_array():
    # URL of the Wikipedia page
    url = "https://tr.wikipedia.org/wiki/Türk_Hava_Yolları_uçuş_noktaları_listesi"

    # Fetch the page content
    response = requests.get(url)
    page_content = response.content

    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(page_content, 'html.parser')

    # Find all table rows in the destinations table
    rows = soup.find_all('tr')

    # Initialize an empty list to store IATA codes
    iata_codes = []

    # Regular expression to match IATA codes (3 uppercase letters)
    iata_code_pattern = re.compile(r'\b[A-Z]{3}\b')

    # Iterate through each row in the table
    for row in rows:
        # Extract text from each cell
        cells = row.find_all('td')
        for cell in cells:
            cell_text = cell.get_text()
            # Find IATA codes in the cell text
            codes = iata_code_pattern.findall(cell_text)
            iata_codes.extend(codes)

    # Remove duplicates by converting the list to a set and back to a list
    unique_iata_codes = list(set(iata_codes))
    #print (unique_iata_codes)
    return unique_iata_codes

    # Print the extracted IATA codes
#print(build_array())
