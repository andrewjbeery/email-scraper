import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import os

term = 'General contractors'
location = 'Milwaukee, WI'
location_city = input("What city are you looking for?")
location_state = input("What state are you looking for? (Please enter in a state abbreviation)")

with open("data\yelp_results_url_added_Milwaukee.json", 'r') as json_file:
    filtered_results = json.load(json_file)

# Key to check for null values
key_to_check = 'website'

# Count the number of null values for the specified key
null_count = sum(1 for d in filtered_results if d.get(key_to_check) is not None)

print(f"Number of '{key_to_check}' found: {null_count}")


def find_email(website_url):
    try:
        # URL of the website to scrape
        url = 'https://' + website_url

        # Send a GET request to the website
        response = requests.get(url)

        # Raise an exception if the response status code is not 200 (OK)
        response.raise_for_status()

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all text on the website
        all_text = soup.get_text()

        # Regular expression to match email addresses
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{3}\b'

        # Find all email addresses in the text
        email_addresses = re.findall(email_regex, all_text)

        # Check if any email addresses were found
        if email_addresses:
            return email_addresses
        else:
            # print(f"No email addresses found on {url}")
            pass
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

counter = 0
for company in filtered_results:
    counter += 1
    website = company.get("website")
    if website == None:
        print("No Website Found!")
    else:
        emails_found = find_email(website)
        if emails_found != None:
            index = filtered_results.index(company)
            filtered_results[index]["email"] = emails_found
        else:
            emails_found = find_email(website + '/contact/')
            if emails_found != None:
                index = filtered_results.index(company)
                filtered_results[index]["email"] = emails_found
            else: 
                emails_found = find_email(website + "/contact-us/")
                if emails_found != None:
                    index = filtered_results.index(company)
                    filtered_results[index]["email"] = emails_found
                else:
                    print(f"No email found for {website}")


    print("emails searched for" + str(counter) + "/" + str(len(filtered_results)))


# Define the file path
file_path = 'data/yelp_results_email_added_' + location_city + '.json'

# Open the file in write mode
with open(file_path, 'w') as file:
    # Use the json.dump() function to write the data to the file
    json.dump(filtered_results, file)

print(f'Data saved to {file_path}')


key_to_check = 'email'

# Count the number of null values for the specified key
null_count = sum(1 for d in filtered_results if d.get(key_to_check) != "")

print(f"Number of '{key_to_check}' found: {null_count}")

ready_for_csv = []
for company in filtered_results:
    if company['email'] != '':
        ready_for_csv.append(company)
    else:
        pass

for company in ready_for_csv:
    company.pop('yelp_url')
    if len(company['email']) ==1:
        company['email'] = company['email'][0]
    else:
        pass


# Specify the field names (keys of the dictionaries)
fieldnames = ready_for_csv[0].keys()

# Specify the name of the CSV file
filename = 'final_output_' + location_city + '.csv'

# Open the CSV file in write mode
with open(filename, mode='w', newline='') as file:
    # Create a CSV writer object
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    # Write the header row
    writer.writeheader()
    
    # Write each dictionary as a row in the CSV file
    for person in ready_for_csv:
        writer.writerow(person)

print(f'CSV file "{filename}" has been created successfully.')
print(f'{str(len(ready_for_csv))} email addresses have been found!')