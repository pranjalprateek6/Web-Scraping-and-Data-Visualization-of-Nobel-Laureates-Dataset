import requests
from bs4 import BeautifulSoup
import csv

url = "https://en.wikipedia.org/wiki/List_of_Nobel_laureates"

#HTTP request to fetch the page
response = requests.get(url)

#Check if the request was successful
if response.status_code == 200:
    #Parsing the HTML content of the page.
    soup = BeautifulSoup(response.text, 'html.parser')

    #Finding the table with the class 'wikitable'.
    table = soup.find('table', class_='wikitable')

    #Initialize a list to store the scraped data.
    laureates_data = []

    for row in table.find_all('tr')[1:]:
        columns = row.find_all('td')
        
        #Making sure that row has enough columns before accessing them
        if len(columns) >= 7:
            year = columns[0].text.strip()
            physics = columns[1].text.strip()
            chemistry = columns[2].text.strip()
            physiology_medicine = columns[3].text.strip()
            literature = columns[4].text.strip()
            peace = columns[5].text.strip()
            economics = columns[6].text.strip()

            #Create a dictionary to store the data
            laureate_entry = {
                'Year': year,
                'Physics': physics,
                'Chemistry': chemistry,
                'Physiology or Medicine': physiology_medicine,
                'Literature': literature,
                'Peace': peace,
                'Economics': economics
            }

            #Appending entres to list of laureates_data.
            laureates_data.append(laureate_entry)
        else:
            print(f"Skipping row with insufficient columns: {row}")

    #CSV file name
    csv_filename = 'nobel_laureates.csv'

    #Open CSV file for writing and writing
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        #CSV fieldnames based on keys in laureate_entry dictionaries
        fieldnames = ['Year', 'Physics', 'Chemistry', 'Physiology or Medicine', 'Literature', 'Peace', 'Economics']

        #CSV writer object.
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #header row.
        writer.writeheader()

        #data rows.
        for entry in laureates_data:
            writer.writerow(entry)

    print(f'Data saved to {csv_filename}')
else:
    print("Failed to retrieve the webpage.")
