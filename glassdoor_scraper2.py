#Data scraping is a technique where a computer program extracts data from human-readable output coming from another program. This Program Sraps the glassdoor webpage, from where we are going to collect our data
#We obtained the code from this github direction: https://github.com/Doumham-Armah/da_salary_proj/blob/master/glassdoor_scraper.ipynb
#Para que Selenium pueda comunicarse con el navegador se necesita instalar en el mismo directorio un ejecutable (ChromeDriver)
#He intentado solucionar el scraper pero no funciona (Han actualizado el código html de la página). Intentaremos volver a esto más adelante y descargaremos la información directamente.

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException
from selenium import webdriver
import time
import pandas as pd
import numpy as np
import math

exps = (NoSuchElementException, StaleElementReferenceException)

def get_jobs(keyword, pages, verbose=False):
    
 
    
    options = webdriver.ChromeOptions()
    
    #give path to chromedriver
    #exec_path_mac = '/Users/mahmoudhamra/Dropbox/GitHub Projects/da_salary_proj/scraping-glassdoor-selenium-master/chromedriver'
    exec_path_pc = "C:/Users/aleja/OneDrive/Documentos/Programas Python/ds_salary_proj/chromedriver"
    driver = webdriver.Chrome(executable_path=exec_path_pc, options=options)
    

    driver.set_window_size(1120, 1000)
    url = 'https://www.glassdoor.com/Job/' + keyword.split()[0] + '-' + keyword.split()[1] + '-jobs-SRCH_KO0,14.htm'    
    driver.get(url)
    df = []    
    
    #loop through pages
    for i in range(pages):
        
        #if more than one page, load and get the next pages
        if i>=1:
            url2 = 'https://www.glassdoor.com/Job/' + keyword.split()[0] + '-' + keyword.split()[1] + '-jobs-SRCH_KO0,12_IP' + str(i+1) + '.htm?includeNoSalaryJobs=true&sortBy=date_desc'
            #https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14_IP2.htm?includeNoSalaryJobs=true&pgc=AB4AAYEAHgAAAAAAAAAAAAAAAbcabZcARgEBAQYAsBeHDlBWtOee61zjJuQvYNYdYwFymUP%2BU5DVANzdTAIN3m23riKShrX35x7cIFeAxdA9pErhi2%2FekI9Q3ejd7lgAAA%3D%3D
            #https://www.glassdoor.com/Job/data-scientist-jobs-SRCH_KO0,14_IP3.htm?includeNoSalaryJobs=true&pgc=AB4AAoEAPAAAAAAAAAAAAAAAAbcabZcAdgEBARgHViX9n%2BPzckFmV5IYdyq04EngCEA6QXmfjBV6wqL30vB3hpG9vZXvH5R%2BvDe6kyt6UWavKvYybPeuoaXe2Pj3Rcf66iibObzBVLx%2FVrImW8%2Fhg5AaPEY8pqrdIuYgxUID0VAXIyIW5WWeyjPkk4sBuc4AAA%3D%3D
            driver.get(url2)
        else:
            pass
        
        driver.implicitly_wait(1)
        
        #collect job listings in the page (30 jobs/page)
        jobs = driver.find_elements_by_xpath('.//*[@id="MainCol"]/div[1]/ul/li')
        
        for job in jobs:
            
            print("---------------------------")
            
            # click on job 
            job.click()
            print("JOB BUTTON CLICKED")
            
            #if sign up window pops up close it
            try:
                driver.find_element_by_css_selector('[alt="Close"]').click()  #clicking to the X.
                print("clicked the X button")
            except NoSuchElementException:
                pass

            
            #get job_title
            try:
                job_title = job.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[2]').text
            except exps:
                job_title = np.nan
                
            #get rating
            try:
                rating = job.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/span').text
            except exps:
                rating = np.nan
            
            #get salary_estimate  
            try:
                salary_estimate = job.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[4]/span').text
            except exps:
                salary_estimate = np.nan
            
            #get location
            try:
                location = job.find_element_by_xpath('//*[@id="JDCol"]/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[3]').text
            except exps:
                location = np.nan
                                

            #Looping over Company Overview section and appending information to comp_info list
            comp_info = []
            elems = driver.find_elements_by_xpath('.//div[@id="EmpBasicInfo"]//div//div[@class="d-flex flex-wrap"]//div[@class="d-flex justify-content-start css-rmzuhb e1pvx6aw0"]')
            for element in elems:
                try:
                    driver.implicitly_wait(5)
                    #taking key value pairs ex: 'size', 1001 to 5000 Employees etc.
                    comp_info.append(element.find_element_by_xpath('.//span[@class="css-1taruhi e1pvx6aw1"]').text)
                    comp_info.append(element.find_element_by_xpath('.//span[@class="css-i9gxme e1pvx6aw2"]').text)

                except StaleElementReferenceException:
                    print("##################StaleElementReferenceException##################")
                        
                    
            # Convert comp_info list to dictionary
            it = iter(comp_info)
            comp_info = dict(zip(it, it))
            
           
            # take values from comp_info dict
            try:
                size = comp_info['Size']
            except KeyError:
                size = "Unknown"
                
                            
            try:
                founded = comp_info['Founded']
            except KeyError:
                founded = np.nan
                

            try:
                type_of_ownership = comp_info['Type']
            except KeyError:
                type_of_ownership = np.nan
                

            try:
                industry = comp_info['Industry']
            except KeyError:
                industry = np.nan
                

            try:
                sector = comp_info['Sector']
            except KeyError:
                sector = np.nan
                

            try:
                revenue = comp_info['Revenue']
            except KeyError:
                revenue = np.nan
                
            if verbose:
                print('job_title:' , job_title)
                print('salary_estimate:', salary_estimate)
                print('location:', location)
                print('rating:', rating)
                print('size:', size)
                print('founded:', founded)
                print('type_of_ownership:', type_of_ownership)
                print('industry:', industry)
                print('sector:', sector)
                print('revenue:', revenue)
                
                
            print("---------------------------")
            
            #append job details to df
            df.append({
            "job_title": job_title,
            "salary_estimate": salary_estimate,
            "location": location,
            "rating" : rating,
            "size" : size,
            "founded" : founded,
            "type_of_ownership" : type_of_ownership,
            "industry" : industry,
            "sector" : sector,
            "revenue" : revenue})
         
    return pd.DataFrame(df)  #This line converts the dictionary object into a pandas DataFrame