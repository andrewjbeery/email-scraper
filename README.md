# Email Web Scraper for companies in area

Side project diving with the goal of learning more about web scraping, apis, and search results.


### How it works

    - api connects to yelp fusion api.

    - searches for up to 1000 general contractors in the madison wisconsin area

    - these results get written to yelp_results.json so the api doesn't go over the polling limit if the code needs to get ran more than once

    - each result gets moved to a different dictionary with simplified data.

    - name, yelp url, city, phone are kept
    
    - website is found using the find_url function
    
        - yelp website is loaded 
        
        - the class of the button that may have the website is found
        
        - of the list of the buttons, if the button has the text that ends in .xxx, the url is returned as the "website"
        
    - plan to find email using the url that is found from yelp by going to website, website/contact/, and website/contact-us/
    
        - check if each exist
        
        - if they do exist, look for someting on screen that follows the email format
        
        - if not, continue to next page
        
    - if most contractors websites are not found using this method, might try using google search api to find the contractors website.
