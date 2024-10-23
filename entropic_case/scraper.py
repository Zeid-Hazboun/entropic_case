import requests
from bs4 import BeautifulSoup
import csv

# URL of the webpage
url = "https://ispt.eu/projects/?theme-tag=heat"

# Send a GET request to fetch the raw HTML content
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find all project elements within the 'article' tag (article was choosen after inspection of webpage elements)
projects = soup.find_all('article')


# Collect the project titles and links
project_data = []
for project in projects:
    title = project.find('h2').text 
    link = project.find('a')['href'] 
    project_data.append([title, link])


# Function to scrape individual projects using the links extracted previously
def scrape_project_details(link):
    response = requests.get(link)
    project_soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize values present in projects
    code = 'N/A'
    status = 'N/A'
    start_date = 'N/A'
    description = 'N/A'

    # Extract code, status, and start date from entry-meta div
    meta_div = project_soup.find('div', class_='entry-meta')
    if meta_div:
        meta_spans = meta_div.find_all('span')
        for i in range(0, len(meta_spans) - 1, 2):
            key = meta_spans[i].text.strip()
            value = meta_spans[i + 1].text.strip()
            if key == 'Code':
                code = value
            elif key == 'Status':
                status = value
            elif key == 'Start date':
                start_date = value

    # Extract the description from the entry-content div
    description_div = project_soup.find('div', class_='entry-content')
    if description_div:
        description = description_div.get_text(separator=" ").strip()

    return code, status, start_date, description


# Collect the details for each project and save them in one file
csv_filename = "data/ispt_projects.csv"
project_details = []

for project in project_data:
    title, link = project
    code, status, start_date, description = scrape_project_details(link)
    project_details.append([title, link, code, status, start_date, description])

# Save all project details to a single CSV file
with open(combined_csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Project Title", "Link", "Code", "Status", "Start Date", "Description"])
    writer.writerows(project_details)

print(f"Combined project details have been saved to {csv_filename}.")


