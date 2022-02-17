# -*- coding: utf-8 -*-
"""
Created on Mon Jan  3 18:38:06 2022

@author: Daniel Eduardo López (delope)

Contact: daniel-eduardo-lopez@outlook.com
"""

### Project: Data Jobs Salaries in Mexico in January 2022

#### DATA COLLECTION: WEB SCRAPING

# Libraries importation
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import pandas as pd

# Entry of the Data Jobs in both English and Spanish (avoid empty words)
jobs_list = ["analista datos",
           "data analyst",
           "cientifico datos",
           "data scientist",
           "ingeniero datos",
           "data engineer",
           "arquitecto datos",
           "data arquitect",
           "analista negocio",
           "business analyst"]
# This list was based on: 
    # Axistalent (2020). The Ecosystem of Data Jobs - Making sense of the Data Job Market. https://www.axistalent.io/blog/the-ecosystem-of-data-jobs-making-sense-of-the-data-job-market 

# Setting of the base url of the OCC searcher
base_url = "https://www.occ.com.mx/empleos/de-"
base_page_url = "?page="

# Creation of the corresponding url for each job from the jobs list
jobs_url_list = list(jobs_list)
length = len(jobs_url_list)

for i in range(0,length):
    jobs_url_list[i] = jobs_url_list[i].strip()
    jobs_url_list[i] = jobs_url_list[i].lower()
    jobs_url_list[i] = jobs_url_list[i].replace(' ','-')
    jobs_url_list[i] = base_url + jobs_url_list[i]
    jobs_url_list[i] = jobs_url_list[i] + '/'
    #print(jobs_url_list[i])

# Number of pages to scrap
number_pages = 10

# Setting of the executable path in a new service instance for 
service = Service(executable_path=GeckoDriverManager().install())

# Creation of a new instance of the Firefox driver
driver = webdriver.Firefox(service = service)

# Retrieval of the class identifiers from the OCC Website
#driver.get(jobs_url_list[0])
#html_test = driver.page_source

# Entry of the OCC Website class identifiers
"""
IMPORTANT NOTE: OCC Website dynamically sets the class identifiers for its 
page elements. So, surely the following class identifiers will not produce 
results when running the present code in a different moment than the one
when this code was written and run. 
Thus, to RE-RUN the code, first, it is necessary to the load the page source 
into the variable html_test as shown before and then INSPECT what are the 
CURRENT class identifiers to produce NEW results.
"""
vacancy_class = 'c0132 c011010' # Done
jobname_class = 'c01584 c01588 c01604 c01990 c011016' # Done
salary_class = 'c01584 c01591 c01604 c01993' # Done
company_class = 'c011000' # Done
location_class = 'c011005 c011006' # Done


# Creation of the list to store the data
data = []

# Iterations over the different jobs
for job_url in jobs_url_list:
    
    # Start of the loop
    print('Fetching data for:', jobs_list[jobs_url_list.index(job_url)].title(), 
          ' ({} out of {})'.format(jobs_url_list.index(job_url)+1, length))
    
    # Creation of the different pages for the job
    pages_url_list = []
    for j in range(1, number_pages + 1):
        if j == 1:
            pages_url_list.append(job_url)
        else:
            pages_url_list.append(job_url + base_page_url + str(j))
        
    # Web scrapping over the different pages
    for url in pages_url_list:
        
        # Adding try tag in case urls might have a problem
        try:
            # Soup creation
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Data extraction
            vacancies = soup.find_all('div', attrs = {'class': vacancy_class})
            
            for vacancy in vacancies:
                job = []
                
                try:
                    job.append(vacancy.find('h2', attrs = {'class': jobname_class}).text)
                except:
                    job.append(None) # In case there is no job name available
                
                try:
                    job.append(vacancy.find('span', attrs = {'class': salary_class}).text)
                except:
                    job.append(None) # In case there is no salary available
                
                try:
                    job.append(vacancy.find('a', attrs = {'class': company_class}).text)
                except:
                    job.append(None) # In case there is no company name available

                try:
                    job.append(vacancy.find('a', attrs = {'class': location_class}).text)
                except:
                    job.append(None) # In case there is no location available

                data.append(job)
        
        except:
            continue
    
    # End of the urls loop
    print('Successfully retrieved data for:', jobs_list[jobs_url_list.index(job_url)].title(),
          ' ({} out of {})'.format(jobs_url_list.index(job_url) + 1, length) +'\n')

# End of the main loop
print('Job done!')

# Closure of the Driver
driver.quit()

# Data storation as a data frame
df = pd.DataFrame(data, columns = ['Job','Salary','Company','Location'])

# Data exportation as a csv
df.to_csv('DataJobsMexicoJan2022.csv', index=False, encoding='utf-8')

