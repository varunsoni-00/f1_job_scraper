# Importing the required libraries
import re
import json
import requests
import dateparser
from bs4 import BeautifulSoup


# Creating the scrapping functions for all the teams
# Scrapper for mclaren
def mclaren(html):
    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role
    information = list()
    
    # The headers for the mclearn team will  be fixed i.e. [Job Title, Work Model, Location, Department, Link]
    # We will pass this directly in the return statement since its fixed and known to us
    
    # Storing the html code of for the current team
    soup = BeautifulSoup(html, "html.parser")
    
    # All the jobs for the mclaren team can be viewed on a single page
    # It is a static website
    # So reaching the table which has all the required job information
    jobs_table = soup.find_all("div", attrs={"data-testid": "offer-list-table-desktop-display"})
    
    # Next this table will have multiple table rows which will be nothing but our job information
    # So we will iterate through all the tr in jobs_table and then extract the information from them
    job_rows = jobs_table[0].find_all("tr")
    
    # Now we will iterate through all the job rows, we will ignore the first one
    # Since that row will have information of the table headers
    
    # Iterating through all the job rows
    for row in job_rows[1:]:
        # Creating a list to store the current job information
        current_job_information = list()
        
        # Each row will hav 5 td's i.e. 5 table data values, each of them includes the following things
        # First: Job title and job page link
        # Second: Work Modes (Hybrid, On-site, etc.)
        # Third: Work Location
        # Fourth: Job Department
        # Fifth: Job link again
        # We can extract all the required information from the first 4 td's
        table_data = row.find_all("td")
        
        # Iterating through the first 4 td's and extracting the required information
        # Extracting the job title
        job_title = table_data[0].text
        
        # Extracting the work model
        work_model = table_data[1].text
        
        # Extracting the work location
        job_location = table_data[2].text
        
        # Extracting the work department
        job_department = table_data[3].text
        
        # Extracting the job link
        job_link = table_data[0].find_all("a")[0]["href"]
        # Adding the full job link to the extracted link
        job_link = "https://racingcareers.mclaren.com" + job_link
        
        # Adding all the information in the current job information list
        current_job_information.append(job_title)
        current_job_information.append(work_model)
        current_job_information.append(job_location)
        current_job_information.append(job_department)
        current_job_information.append(job_link)
        
        # Once all the information for the current job is extracted we will store it in the main information list
        information.append(current_job_information)
    
    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Job Title", "Work Model", "Location", "Department", "Link"], information


# Scrapper for ferrari
def ferrari(html):
    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role
    information = list()
    
    # The headers for the ferrari team will  be fixed i.e. [Job Title, Location, Job Posting Date, Department, Link]
    # We will pass this directly in the return statement since its fixed and known to us
    
    # Storing the html code of for the current team
    soup = BeautifulSoup(html, "html.parser")
    
    # All the jobs for the ferrari team can be viewed on a single page
    # It is a static website
    # So reaching the page which has all the required job information
    # The jobs on the ferrari page are in list not in table
    # First we will extract the overall list
    jobs_box = soup.find_all("ul", attrs={"id": "job-tile-list"})
    
    # Inside this unordered list we have multiple list items
    # Each list item represents a job and its corresponding details
    job_list = jobs_box[0].find_all("li")
    
    # After getting all the list we will iterate through each list and extract the job information
    # Iteration through all the jobs in the list
    for job in job_list:
        # Creating a list to store the current job information
        current_job_information = list()
        
        # Each element in the job lists will have majorly 3 sections of code for desktop, tablet and mobile
        # First we will locate the div which has a class and has word desktop in it
        # To do this we will use the regular expression in the class attrs
        job = job.find_all("div", attrs={"class": re.compile(r".*desktop.*")})
        
        # Now inside each job there are 2 div with class "oneline" these are the 2 div which have all the information
        # The first div will have the job title and link
        # From the second div we can extract location, posting date & department
        job_details = job[0].find_all("div", attrs={"class": "oneline"})
        
        # Extracting the job title from the first div
        job_title = job_details[0].find_all("a")[0].text
        
        # Extracting the job link from the first div
        job_link = job_details[0].find_all("a")[0]["href"]
        # Adding the complete link in the job link
        job_link = "https://jobs.ferrari.com" + job_link
        
        # Extracting the job location from the second div
        # Inside this every these are 6 div and every alternate div has the information we need
        job_location = job_details[1].find_all("div")[1].text
        
        # Extracting the job posting date from the second div
        job_posting_date = job_details[1].find_all("div")[3].text
        
        # Some job cound be missing department information in that case we will keep them blank
        if len(job_details[1].find_all("div")) == 6:
            # Extracting the job department from the second div
            job_department = job_details[1].find_all("div")[5].text
        else:
            # If department information does not exist we will keep it blank
            job_department = "-"
        
        # Adding all the information in the current job information list
        current_job_information.append(job_title.strip())
        current_job_information.append(job_posting_date.strip())
        current_job_information.append(job_location.strip())
        current_job_information.append(job_department.strip())
        current_job_information.append(job_link.strip())
        
        # Once all the information for the current job is extracted we will store it in the main information list
        information.append(current_job_information)
    
    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Job Title", "Job Posting Date", "Location", "Department", "Link"], information


# Scrapper for mercedes
def mercedes(html):
    # Storing the html page foe the mercedes source page
    source_page_html = BeautifulSoup(html, "html.parser")

    # All the jobs for the mercedes team cannot be viewed on a single page
    # It is a static website with multiple job pages
    # So first from the source page we will find out how many job pages are there and store their links
    # Then we will iterate through each page link and get all the jobs

    # First on the source page we will reach the job paginator in the html code which has an unordered list
    # The unordered list has list items and the count of total list items mins 2 will be the total job pages
    # Minus 2 because the list items also has the front and the back navigation buttons at the start and end

    # Going to the job_paginator html coden the page and getting all the list items
    job_pages_list = source_page_html.find_all("li", attrs={"class": re.compile(
        "pagination_pagination__item.*")})

    # So all the job links have a common text in pre i.e. https://www.mercedesamgf1.com/"
    # We will add this to the pre of each extracted link to complete the url
    # Creating a dictionary that will store all the job link pages
    job_pages_link = dict()

    # Iterating through all the list items and extracting the job pages link
    # We will ignore the first and the last list item as they are page navigators
    for page in range(1, len(job_pages_list)-1):
        page_number = job_pages_list[page].find_all("a")[0]["data-page"]
        job_pages_link["Page_" + page_number] = "https://www.mercedesamgf1.com" + job_pages_list[page].find_all("a")[0][
            "href"]


    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role
    information = list()
    
    # The headers for the mercedes team will be fixed i.e. [Job Title, Job ID, Deadline, Department, Link]
    # We will pass this directly in the return statement since its fixed and known to us

    # Iterating though all the job pages
    for link in job_pages_link.values():
        # Getting the current job page's html code
        response = requests.get(link, verify=False)

        # Storing the html code for the current page
        soup = BeautifulSoup(response.text, "html.parser")

        # So reaching the table which has all the required job information
        jobs_table = soup.find_all("table", attrs={"class": re.compile(".*vacancylist.*")})

        # Inside the vacancy table all the table rows will have the jobs details
        # So we will iterate through each table row and extract that respective job information
        jobs_table_body = jobs_table[0].find_all("tbody")
        job_rows = jobs_table_body[0].find_all("tr")

        # Iterating through each row and extracting the information
        for row in job_rows:
            # Creating a list to store the current job information
            current_job_information = list()

            # Each row will hav 3 td's i.e. 3 table data values, each of them includes the following things
            # First: Job title, job link, job id
            # Second: Department
            # Third: Deadline
            row_data = row.find_all("td")

            # Extracting information from the 1st row data
            # It has 6 div, which will consist of 3 required information title, id and link
            job_details = row_data[0].find_all("div")

            # Extracting the job title
            job_title = job_details[1].text

            # Extracting the job id
            job_id = job_details[4].text.split(":")[1].strip()

            # Extracting the job link
            job_link = job_details[5].find_all("a")[0]["href"]
            # Adding the complete link to the job link
            job_link = "https://www.mercedesamgf1.com" + job_link

            # Extracting information from the 2nd row data
            # It has 2 div, which will consist of department information
            job_department = row_data[1].find_all("div")[1].text

            # Extracting information from the 3rd row data
            # It has 1 span, which will consist of deadline
            # This will always be blank as this is updated on the website using javascript in realtime
            # So for beautiful soup's html code that information will always be blank
            job_deadline = row_data[2].find_all("span")[0].text

            # Adding all the information in the current job information list
            current_job_information.append(job_title)
            current_job_information.append(job_id)
            current_job_information.append(job_deadline)
            current_job_information.append(job_department)
            current_job_information.append(job_link)

            # Once all the information for the current job is extracted we will store it in the main information list
            information.append(current_job_information)

    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Job Title", "Job ID", "Deadline", "Department", "Link"], information


# Scrapper for red bull
def red_bull_racing(html):
    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role
    information = list()
    
    # The headers for the red bull racing team will  be fixed i.e. [Job Title, Work Model, Location, Category, Link]
    # We will pass this directly in the return statement since its fixed and known to us
    
    # Storing the html code of for the current team
    soup = BeautifulSoup(html, "html.parser")
    
    # All the jobs for the red bull team can be viewed on a single page
    # It is a static website
    # So reaching the div class which has all the required job information
    # There is only 1 class with this name
    jobs_class = soup.find_all("div", attrs={"class": re.compile(r"jobs_positions.*")})
    
    # Inside first job_class there are multiple <a> tags which withholds the individual job information
    # So we will iterate through all the <a> and get all the jobs and its information
    job_rows = jobs_class[0].find_all("a")
    
    # Now iterating through each job in the job row and extracting the required information
    for job in job_rows:
        # Creating a list to store the current job information
        current_job_information = list()
        
        # Job is the <a> tag the href part in this has out job link
        # Further inside each job the information which we need is spilt into different cosmos tags
        # There are 3 <cosmos-text> inside the <a>
        # The 1st has the job_category/department
        # The 2nd has the work model information
        # The 3rd has the job location
        # Then there is 1 cosmos-title which has the job title information
        
        # Extracting the job link
        job_link = job["href"]
        
        # Extracting the job_category
        job_category = job.find_all("cosmos-text")[0].text
        
        # Extracting the work_model
        work_model = job.find_all("cosmos-text")[1].text
        
        # Extracting the job_location
        job_location = job.find_all("cosmos-text")[2].text
        
        # Extracting the job_title
        job_title = job.find_all("cosmos-title")[0].text
        
        # Adding all the information in the current job information list
        current_job_information.append(job_title)
        current_job_information.append(work_model)
        current_job_information.append(job_location)
        current_job_information.append(job_category)
        current_job_information.append(job_link)
        
        # Once all the information for the current job is extracted we will store it in the main information list
        information.append(current_job_information)
    
    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Job Title", "Work Model", "Location", "Category", "Link"], information


# Scrapper for williams
def williams(html):
    # Storing the html code of for the cadillac source page
    source_page_html = BeautifulSoup(html, "html.parser")

    # All the jobs for the williams team cannot be viewed on a single page
    # It is a static website with multiple job pages
    # So first from the source page we will find out how many job pages are there and store all their links
    # Then we will iterate through each page link and get all the jobs
    # On the source page there is a <ul> with aria-label: "Pagination Navigation"
    # Inside this there is 1 span class which has the text as number of pages on the portal

    # Locating the paginator
    job_paginator = source_page_html.find_all("ul", attrs={"aria-label": "Pagination Navigation"})


    # Locating the 1 span class inside the paginator and extracting the count of pages
    job_page_count = job_paginator[0].find_all("span")[0].text

    # Now we can create the link for all the pages since its common and only the last number changes
    # The common link "https://careers.williamsf1.com/jobs?page="

    # Once we have the count we will create a dictionary to store the page number and its link
    job_pages_link = dict()

    # Creating all the job links
    for pages in range(1, len(job_page_count)+1):
        job_pages_link["Page_" + str(pages)] = "https://careers.williamsf1.com/jobs?page=" + str(pages)

    # Once we have all the job pages we will iterate through all of them and extract the required information
    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role

    information = list()

    # The headers for the williams team will be fixed i.e. [Job Title, Location, Department, Link]
    # We will pass this directly in the return statement since its fixed and known to us

    # Iterating through all the job pages
    for link in job_pages_link.values():
        # Getting the current job page's html code
        response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"}, verify=False)

        # Storing the html code for the current page
        soup = BeautifulSoup(response.text, "html.parser")

        # In the job portal page there is 1 <div> with class: "attrax-list-widget__lists"
        # Inside this div there are multiple div which represents our job rows
        # Reaching the main div
        job_section = soup.find_all("div", attrs={"class": "attrax-list-widget__lists"})

        # Inside the job_section there are multiple <div> with attr data-jobid="<number>" which represent job rows
        job_rows = job_section[0].find_all("div", attrs={"data-jobid": re.compile(r"\d+")})


        # Iterating through all the job_rows
        # Iterating through the second one
        for row in job_rows:

            # Creating a list to store the current job information
            current_job_information = list()

            # Inside the job_details code
            # The first <a> has the job link and the job title
            # Then there is a <div> further ahead with the word location in its class name
            # The second <p> inside that div has the job_location
            # The last <p> in the row will hae the job_department

            # Extracting the job_link
            job_link = row.find_all("a")[0]["href"]
            # Adding the full job link to the extracted link
            job_link = "https://careers.williamsf1.com" + job_link

            # Extracting the job_title
            job_title = row.find_all("a")[0].text

            # Extracting the job_location
            # Reaching the location div
            job_location_div = row.find_all("div", attrs={"class": re.compile(r".*location.*")})[0]
            # Inside this <div> the second <p> has the job_location
            job_location = job_location_div.find_all("p")[1].text

            # Extracting the job department
            # There is javascript involved in the web page's code
            # There are more <p> in the code, compared to what can be seen in the code on devtools
            # In each row the 6th <p> has the job_department
            job_department = row.find_all("p")[5].text

            # Adding all the information in the current job information list
            current_job_information.append(job_title)
            current_job_information.append(job_location.strip())
            current_job_information.append(job_department.strip())
            current_job_information.append(job_link)

            # Once all the information for the current job is extracted we will store it in the main information list
            information.append(current_job_information)

    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Job Title", "Location", "Department", "Link"], information


# Scrapper for aston martin
def aston_martin(html):
    # Storing the html code of for the aston martin source page
    source_page_html = BeautifulSoup(html, "html.parser")
    
    # All the jobs for the aston martin team cannot be viewed on a single page
    # It is a static website with multiple job pages
    # So first from the source page we will find out how many job pages are there and store all their links
    # Then we will iterate through each page link and get all the jobs
    
    # Going to the job section html code on the page
    job_section = source_page_html.find_all("section", attrs={"class": re.compile(".*job-listing.*"),
                                                              "audience": "public"})
    
    # Extracting all the job pages and link
    # The count of pages are a part of ordered list within the job posting section
    # So the number of list items will be the count of pages on the portal
    # Getting the ordered list from the job section
    job_pages_list = job_section[0].find_all("ol")
    
    # So all the pages have common link "https://www.astonmartinf1.com/en-GB/careers?page=" just the page number changes
    # So if we have the len of list items in the ordered list we can create links for all the pages
    # Storing each page number and its link in a dictionary
    job_pages_link = dict()
    
    # Getting all the list items from the ordered list
    job_pages_list = job_pages_list[0].find_all("li")
    
    # Creating all the links
    for page in range(1, len(job_pages_list) + 1):
        job_pages_link["Page_" + str(page)] = "https://www.astonmartinf1.com/en-GB/careers?page=" + str(page)
    
    # Once we have all the job pages we will iterate through all of them and extract the required information
    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role
    information = list()
    
    # The headers for the aston martin team will be fixed i.e. [Job Title, Team, Deadline, Location, Link]
    # We will pass this directly in the return statement since its fixed and known to us
    
    # Iterating though all the job pages
    for link in job_pages_link.values():
        # Getting the current job page's html code
        response = requests.get(link, verify=False)
        
        # Storing the html code of for the current page
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Going to the job section html code on the page
        job_section = soup.find_all("section", attrs={"class": re.compile(".*job-listing.*"),
                                                      "audience": "public"})
        
        # Inside the job section there is 1 unordered list which has list items as all the job rows
        job_unordered_list = job_section[0].find_all("ul")
        
        # Now we will extract all the list items which will be nothing but out job rows
        job_rows = job_unordered_list[0].find_all("li")
        
        # Next we will iterate through all the job rows and extract the required information's
        for row in job_rows:
            # Creating a list to store the current job information
            current_job_information = list()
            
            # Each <li> has 1 <h3> tag which has the job title
            # 1 <a> which has the job link
            # 1st <span> which has the location
            # 2nd <span> which has the team name
            # 3rd <span> which has the deadline
            
            # Extracting the job title
            job_title = row.find_all("h3")[0].text
            
            # Extracting the job link
            job_link = row.find_all("a")[0]["href"]
            
            # Extracting the work location
            job_location = row.find_all("span")[0].text
            
            # Extracting the job_team_name
            job_team_name = row.find_all("span")[1].text
            
            # Extracting the job_deadline
            job_deadline = row.find_all("span")[2].text
            # Converting it into date format
            try:
                job_deadline = dateparser.parse(job_deadline.split(":")[1])
                job_deadline = job_deadline.date()
            except:
                job_deadline = row.find_all("span")[2].text
            
            # Adding all the information in the current job information list
            current_job_information.append(job_title)
            current_job_information.append(job_team_name)
            current_job_information.append(job_deadline)
            current_job_information.append(job_location)
            current_job_information.append(job_link)
            
            # Once all the information for the current job is extracted we will store it in the main information list
            information.append(current_job_information)
    
    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Job Title", "Team", "Deadline", "Location", "Link"], information


# Scrapper for kick sauber
def kick_sauber(html):
    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role
    information = list()
    
    # The headers for the kick sauber team will  be fixed i.e. [Job Title, Link]
    # We will pass this directly in the return statement since its fixed and known to us
    
    # Storing the html code of for the current team
    soup = BeautifulSoup(html, "html.parser")
    
    # All the jobs for the kick sauber team can be viewed on a single page
    # It is a static website
    # The page is divided into multiple container classed which have all the page information
    # The jobs we are looking for is also in one of this container class
    jobs_container = soup.find_all("div", attrs={"class": "grid-container-default-col"})
    
    # Now inside our job container there are 2 div classes
    # The first has all the quick link buttons to type of jobs in the team
    # The second one contains all the job rows
    jobs_sections = jobs_container[2].find_all("div")
    
    # Now getting all the job rows from the second section
    job_rows = jobs_sections[1].find_all("div")
    
    # Now we will iterate through all the job rows and extract the required information
    # Iterating through all the job rows
    for row in job_rows:
        # Creating a list to store the current job information
        current_job_information = list()
        
        # Kick sauber's job page have minimum information at display
        # You need to dig deep into links to get to detailed information
        # So there are only 2 things that we will extract from each job row
        # First: Job row (part of <h3> tag)
        # Second: Job link (part of <a> tag)
        
        # Extracting the job title
        job_title = row.find_all("h3")[0].text
        
        # Extracting the job link
        job_link = row.find_all("a")[0]["href"]
        # Adding the full job link to the extracted link
        job_link = "https://www.sauber-group.com" + job_link
        
        # Adding all the information in the current job information list
        current_job_information.append(job_title)
        current_job_information.append(job_link)
        
        # Once all the information for the current job is extracted we will store it in the main information list
        information.append(current_job_information)
    
    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Job Title", "Link"], information


# Scrapper for racing bulls
def racing_bulls(json_code):
    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role
    information = list()

    # We will not use the html code to extract information since it is a dynamic page not a static one
    # Each time the page is loaded through a js script code the job information is passed to the website
    # The information that is passed is a json file which has by default 10 job information
    # It also has the maximum count of jobs in racing_bulls, so we will extract the maximum count
    # Take that number and modify the default link to give all the jobs
    # That we can extract all the jobs from the jso file
    # The default link is: "https://jobs.redbull.com/api/search?pageSize=10&locale=en&country=int"
    # The pageSize term in this is "10"
    # We will pass the maximum count here and extract all jobs json file
    # So first we will load the default json

    # IMPORTANT NOTE
    # The Racing bulls company is a sub-company of red bull, this is redbull website we are working with
    # Redbull F1 is completely different entity in terms of website
    # But apart from that all many other red bull sports venture are a part of this website
    # So you have to filter f1 to get the f1 jobs
    # But what we can do is extract all the jobs from all the sub companies under redbull on this webpage
    # Add a column in our excel that will tell us if its F1 or other category job
    # That way we can have more jobs for us to look and apply within the red bull parent company

    # Taking the extracted json code and converting it into a dictionary
    json_dictionary = json.loads(json_code)

    # Getting the maximum jobs on the portal
    # In the json_dictionary count of maximum jobs in redbull parent company is stored in resultSize key
    red_bull_job_count = json_dictionary["resultSize"]
    
    # Creating the new link to extract the information of all the jobs in redbull
    link = ("https://jobs.redbull.com/api/search?pageSize={0}&locale=en&country=int").format(red_bull_job_count)
    
    # Extracting the json dictionary with all job information
    response = requests.get(link, verify=False)
    json_code = response.text

    # Taking the extracted json code and converting it into a dictionary
    json_dictionary = json.loads(json_code)

    # Now we have the dictionary with all the jobs
    # The headers for the racing_bulls team will be fixed i.e.
    # [Category, Job Title, Location, Department, Work Model, Link]
    # We will pass this directly in the return statement since its fixed and known to us

    # Inside the json dictionary there is a jobs key which has a list as value
    # The list elements are dictionary representing all individual job information
    # Its like each element in the list is a job row
    job_rows = json_dictionary["jobs"]

    # Iterating through all the job rows and extracting the required information
    for row in job_rows:

        # Creating a list to store the current job information
        current_job_information = list()

        # In each row there are key elements which are out df headers
        # The value to those keys will be the information that we need
        # Some values are even nested dictionary, we will work on them accordingly

        # Extracting the job title
        job_title = row["title"]

        # Extracting the job category
        # If there is f1 in the job_title then it mean it is a f1 job
        # Else it is some other business job
        if "F1" in job_title:
            job_category = "F1"
        else:
            job_category = "Others"

        # Extracting the job link
        # So there is no link to be precise in this dict, but we can make it using the value of "slug" key in the dict
        job_link = row["slug"]
        # Adding the full job link to the extracted job id
        job_link = "https://jobs.redbull.com/int-en/" + job_link

        # Extracting the work location
        # It is in formation city,state, country, region
        job_location = row["locationText"]

        # Extracting the work department
        # It is a nested dictionary
        # Eg: "function": {"name": "Operations"}
        # For some jobs department can be missing so we will output "-"
        if row["function"]:
            job_department = row["function"]["name"]
        else:
            job_department = "-"

        # Extracting the work model information
        work_model = row["employmentType"]

        # Adding all the information in the current job information list
        current_job_information.append(job_category)
        current_job_information.append(job_title)
        current_job_information.append(job_location)
        current_job_information.append(job_department)
        current_job_information.append(work_model)
        current_job_information.append(job_link)

        # Once all the information for the current job is extracted we will store it in the main information list
        information.append(current_job_information)

    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Category", "Job Title", "Location", "Department", "Work Model", "Link"], information


# Scrapper for hass
def hass(json_code):
    # If it was a static html page below is the code we would follow
    ####################################################################################################################
    # # Creating a list to store each job information
    # # This will be a nested list
    # # Where the multiple list inside the main list will represent information pertaining to each job role
    # information = list()
    #
    # # The headers for the hass team will  be fixed i.e. [Job Title, Work Model, Location, Department, Link]
    # # We will pass this directly in the return statement since its fixed and known to us
    #
    # # Storing the html code of for the current team
    # soup = BeautifulSoup(html, "html.parser")
    #
    # print(soup.prettify())
    #
    # # All the jobs for the hass team can be viewed on a single page
    # # It is a static website
    # # The jobs information in all in the code within the <main> tag on the page, there is only 1 main tag
    # jobs_section = soup.find_all("main")
    #
    # # Inside the main section there is an unordered list which has all the job rows
    # job_unordered_list = jobs_section[0].find_all("ul")
    #
    # # Inside the unordered list there are list items which represent each job rows
    # # Inside the <li> there is all the information which we need to extract
    # job_rows = job_unordered_list[0].find_all("li")
    #
    # # Iterating through all the job rows
    # for row in job_rows:
    # 	# Creating a list to store the current job information
    # 	current_job_information = list()
    #
    # 	# We will extract the information from the li in the following way
    # 	# The first <a> inside the <li> has the job title and job link
    # 	# Then there are 4 <p> inside each <li>
    # 	# The first 2 <p> combined maked up the location its like city, state
    # 	# The 3rd <p> includes the job department
    # 	# The 4th <p> has the work model
    #
    #
    # 	# Extracting the job title
    # 	job_title = row.find_all("a")[0].text
    #
    # 	# Extracting the job link
    # 	job_link = row.find_all("a")[0]["href"]
    # 	# Adding the full job link to the extracted link
    # 	job_link = "https://haasf1team.bamboohr.com" + job_link
    #
    # 	# Extracting the work location
    # 	job_location = row.find_all("p")[0].text + "," + row.find_all("p")[1].text
    #
    # 	# Extracting the work department
    # 	job_department = row.find_all("p")[2].text
    #
    #
    # 	# Extracting the work model information
    # 	work_model = row.find_all("p")[3].text
    #
    # 	# Adding all the information in the current job information list
    # 	current_job_information.append(job_title)
    # 	current_job_information.append(work_model)
    # 	current_job_information.append(job_location)
    # 	current_job_information.append(job_department)
    # 	current_job_information.append(job_link)
    #
    # 	# Once all the information for the current job is extracted we will store it in the main information list
    # 	information.append(current_job_information)
    #
    # # Returning back the job headers for mclaren along with all the extracted job information
    # return ["Job Title", "Work Model", "Location", "Department", "Link"], information
    ####################################################################################################################
    
    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role
    information = list()
    
    # We will not use the html code to extract information since it is a dynamic page not a static one
    # Each time the page is loaded through a js script code the job information is passed to the website
    # The information that is passed is a json file which has all the job details
    # So for the hass f1 team we will extract all the information from that json file
    
    # Taking the extracted json code and converting it into a dictionary
    json_dictionary = json.loads(json_code)
    
    # Inside the json dictionary there is a result key which has a list as value
    # The list elements are dictionary representing all individual job information
    # Its like each element in the list is a job row
    job_rows = json_dictionary["result"]
    
    # Iterating through all the job rows and extracting the required information
    for row in job_rows:
        # Creating a list to store the current job information
        current_job_information = list()
        
        # In each row there are key elements which are out df headers
        # The value to those keys will be the information that we need
        # Some values are even nested dictionary, we will work on them accordingly
        
        # Extracting the job title
        job_title = row["jobOpeningName"]
        
        # Extracting the job link
        # So there is no link to be precise in this dict, but we can make it using the job id
        job_link = row["id"]
        # Adding the full job link to the extracted job id
        job_link = "https://haasf1team.bamboohr.com/careers/" + job_link
        
        # Extracting the work location
        # The value of this key is a nested dict which has city and state
        # We will combine both and stor in job location
        job_location = row["location"]["city"] + ", " + row["location"]["state"]
        
        # Extracting the work department
        job_department = row["departmentLabel"]
        
        # Extracting the work model information
        work_model = row["employmentStatusLabel"]
        
        # Adding all the information in the current job information list
        current_job_information.append(job_title)
        current_job_information.append(work_model)
        current_job_information.append(job_location)
        current_job_information.append(job_department)
        current_job_information.append(job_link)
        
        # Once all the information for the current job is extracted we will store it in the main information list
        information.append(current_job_information)
    
    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Job Title", "Work Model", "Location", "Department", "Link"], information


# Scrapper for alpine
def alpine(json_code):
    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role
    information = list()
    
    # We will not use the html code to extract information since it is a dynamic page not a static one
    # Each time the page is loaded through a js script code the job information is passed to the website
    # The information that is passed is a json file which has all the job details
    # So for the alpine f1 team we will extract all the information from that json file
    
    # Taking the extracted json code and converting it into a dictionary
    json_dictionary = json.loads(json_code)
    
    # Inside the json dictionary there is a job_posting key which has a list as value
    # The list elements are dictionary representing all individual job information
    # Its like each element in the list is a job row
    job_rows = json_dictionary["jobPostings"]
    
    # Iterating through all the job rows and extracting the required information
    for row in job_rows:
        # Creating a list to store the current job information
        current_job_information = list()
        
        # In each row there are key elements which are out df headers
        # The value to those keys will be the information that we need
        # Some values are even nested dictionary, we will work on them accordingly
        
        # Extracting the job title
        job_title = row["title"]
        
        # Extracting the job link
        job_link = row["externalPath"]
        # Adding the full job link to the extracted job link
        job_link = "https://alliancewd.wd3.myworkdayjobs.com/en-GB/alpine-racing-careers" + job_link
        
        # Extracting the work location
        job_location = row["bulletFields"][0]
        
        # Extracting the work department
        job_department = row["bulletFields"][1]
        
        # Extracting the work model information
        job_post_date = row["postedOn"]
        
        # Adding all the information in the current job information list
        current_job_information.append(job_title)
        current_job_information.append(job_post_date)
        current_job_information.append(job_location)
        current_job_information.append(job_department)
        current_job_information.append(job_link)
        
        # Once all the information for the current job is extracted we will store it in the main information list
        information.append(current_job_information)
    
    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Job Title", "Job Post Date", "Location", "Department", "Link"], information


# Scrapper for cadillac
def cadillac(html):
    # Storing the html code of for the cadillac source page
    source_page_html = BeautifulSoup(html, "html.parser")
    
    # All the jobs for the cadillac team cannot be viewed on a single page
    # It is a static website with multiple job pages
    # So first from the source page we will find out how many job pages are there and store all their links
    # Then we will iterate through each page link and get all the jobs
    # On the source page there is a <app-paginator> tag which has multiple <a> depending on no of job pages
    # So we will reach the app-paginator and then get the links for all the pages
    
    # Locating the paginator
    job_paginator = source_page_html.find_all("app-paginator")
    
    # Now the second div in the paginator has the count of pages
    job_page_div = job_paginator[0].find_all("div")
    
    # Now there are multiple <a> within the job_page_div and each <a> basically holds the link to the respective page
    # So counting the number of <a> in this div will tell us how many job pages there are
    # Then we can create the link for all the pages since its common and only the last number changes
    # The common link "https://opportunities.cadillacf1team.com/?pageIndex="
    # In cadillac the link for pages starts from 0 not 1
    # So it will be,
    # "https://opportunities.cadillacf1team.com/?pageIndex=0",
    # "https://opportunities.cadillacf1team.com/?pageIndex=1"
    # And so on
    
    # Getting the all the <a> inside the second div of the paginator
    job_page_list = job_page_div[1].find_all("a")
    
    # Once we have the count we will create a dictionary to store the page number and its link
    job_pages_link = dict()
    
    # Creating all the job links
    for pages in range(len(job_page_list)):
        job_pages_link["Page_" + str(pages + 1)] = "https://opportunities.cadillacf1team.com/?pageIndex=" + str(pages)


    # Once we have all the job pages we will iterate through all of them and extract the required information
    # Creating a list to store each job information
    # This will be a nested list
    # Where the multiple list inside the main list will represent information pertaining to each job role

    information = list()
    
    # The headers for the cadillac team will be fixed i.e. [Job Title, Location, Department, Link]
    # We will pass this directly in the return statement since its fixed and known to us
    
    # Iterating through all the job pages
    for link in job_pages_link.values():
        # Getting the current job page's html code
        response = requests.get(link, verify=False)
        
        # Storing the html code for the current page
        soup = BeautifulSoup(response.text, "html.parser")

        # In the job portal page there is 1 <app-typographical-jobs-list> tag
        # This tag has all the jobs information on the current page
        # Reaching the job_list
        job_list = soup.find_all("app-typographical-jobs-list")

        # Inside the job_list there are multiple <app-typographical-job-card>
        # These cards are nothing but individual job rows
        # We will reach the all the cards and then iterate through all the job rows
        job_rows = job_list[0].find_all("app-typographical-job-card")

        # Iterating through all the job_rows
        for row in job_rows:
            # Creating a list to store the current job information
            current_job_information = list()

            # Inside each row there are multiple <div>
            # The second <div> has all the information needed by us for the current job
            # Reaching the second <div>
            job_details = row.find_all("div")[1]

            # Inside the job_details code
            # There is 1 <a> which has the job link and the job title
            # First <div> inside job_details has the department name
            # The second <span> inside it has the job_location
            # Extracting all the required information

            # Extracting the job_link
            job_link = job_details.find_all("a")[0]["href"]
            # Adding the full job link to the extracted link
            job_link = "https://opportunities.cadillacf1team.com" + job_link

            # Extracting the job_title
            job_title = job_details.find_all("a")[0].text

            # Extracting the department name
            job_department = job_details.find_all("div")[0].text

            # Extracting the job_location
            job_location = job_details.find_all("span")[1].text

            # Adding all the information in the current job information list
            current_job_information.append(job_title)
            current_job_information.append(job_location)
            current_job_information.append(job_department)
            current_job_information.append(job_link)

            # Once all the information for the current job is extracted we will store it in the main information list
            information.append(current_job_information)

    # Returning back the job headers for mclaren along with all the extracted job information
    return ["Job Title", "Location", "Department", "Link"], information


