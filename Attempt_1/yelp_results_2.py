import requests
from bs4 import BeautifulSoup
import re
import json
import csv
import os
# from dotenv import load_dotenv
API_KEY = 'sUz0MAX3HClTUZ96lOJBvHkTNwex_TgrNrP8HUaWl9YMhYrmZSldGy-CqzIxKvLQENLZG8351RWiLVjBCUHb2AA0fUx615lOwGFNB68q3WZkLRP9FFP3NOMTLNjfZXYx'

def find_url(yelp_url):

    # Send a GET request to the website
    response = requests.get(yelp_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML response
        soup = BeautifulSoup(response.content, 'html.parser')
    
        # Find all elements with the specified class
        elements = soup.find_all(class_='css-1idmmu3')
    
        # Extract the link from the first element
        if elements:
            for element in elements:
                # print(element.text)
                site = re.search(r'\b[a-zA-Z0-9-]+\.[a-zA-Z]{3}\b', element.text)
                if site:
                    return(site.group())
                else:
                    pass
        else:
            print('No elements found with the specified class')
    else:
        print(f'Error: {response.status_code}')


# load_dotenv()

# Retrieve API key
# API_KEY = os.getenv("API_KEY")

# Define the search parameters
# term = 'General contractors'
# location = 'Madison, WI'
term = input("What kind of company are you looking for?")
location_city = input("What city are you looking for?")
location_state = input("What state are you looking for? (Please enter in a state abbreviation)")
location = location_city + ", " + location_state


# Define the number of results per page
limit = 50
results = []
# Define the total number of results to retrieve
total_results_to_retrieve = 1000

# Calculate the number of pages needed to retrieve all the results
num_pages = total_results_to_retrieve // limit
if total_results_to_retrieve % limit != 0:
    num_pages += 1

# Make a GET request for each page of results
for page in range(num_pages):
    # Calculate the offset for the current page
    offset = page * limit

    # Define the API endpoint for the current page
    url = f'https://api.yelp.com/v3/businesses/search?term={term}&location={location}&limit={limit}&offset={offset}'

    # Define the headers with the API key
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    # Make a GET request to the API endpoint
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Extract the businesses
        businesses = data.get('businesses', [])

        # Print the business names and addresses
        for business in businesses:
            name = business.get('name')
            address = ', '.join(business.get('location', {}).get('display_address', []))
            print(f'Name: {name}')
            print(f'Address: {address}')
            print()
            results.append(business)
    else:
        print(f'Error: {response.status_code}')


# Define the file path
file_path = 'data/yelp_results_' + location_city + '.json'

# Open the file in write mode
with open(file_path, 'w') as file:
    # Use the json.dump() function to write the data to the file
    json.dump(results, file)

print(f'Data saved to {file_path}')


filtered_results = []
for result in results:
    # print(result)
    location_dict = {}
    try:
        location_dict["name"] = result["name"]
    except KeyError as e:
        print(f'KeyError: {e}')
        pass
    try:
        location_dict["yelp_url"] = result["url"]
    except KeyError as e:
        print(f'KeyError: {e}')
        pass   
    try:
        location_dict["city"] = result["location"]['city']
    except KeyError as e:
        print(f'KeyError: {e}')
        pass
    try:
        location_dict["phone"] = result["phone"]
    except KeyError as e:
        print(f'KeyError: {e}')
        pass
    location_dict["website"] = find_url(result["url"])
    location_dict["email"] = ""
    if len(filtered_results) % 50 == 0:
        with open(file_path, 'w') as file:
        # Use the json.dump() function to write the data to the file
            json.dump(filtered_results, file)
        print("Results Saved!")
    else:
        pass

    filtered_results.append(location_dict)
    print(str(len(filtered_results)) + "/" + str(len(results)))


    # Define the file path
file_path = 'data/yelp_results_url_added_' + location_city + '.json'

# Open the file in write mode
with open(file_path, 'w') as file:
    # Use the json.dump() function to write the data to the file
    json.dump(filtered_results, file)

print(f'Data saved to {file_path}')

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