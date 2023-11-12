from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re
import pandas as pd

def getSimilarWebData(websiteDomainName):
    
    # Set the path to the WebDriver executable
    driver = webdriver.Chrome()

    # Open Google in the web browser
    driver.get('https://www.similarweb.com/website/' + websiteDomainName + '/#overview')
    wait = WebDriverWait(driver, 10)
    visits = "" 
    aveDuation = ""
    us_traffic = ""
    
    # time.sleep(1000)
    try:
        # Wait for up to 10 seconds for the element to be located
        
        # get all elements with this div name
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.engagement-list__item-value')))
        
        if elements and len(elements) >= 4:
            visits = elements[0].text
            aveDuation = elements[3].text
        else:
            return -1
        
        # Try to locate the US traffic data
        try:
            country_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.wa-geography__country.wa-geography__legend-item')))
            
            if country_elements and len(country_elements) == 6:
                
                for i, country_element in enumerate(country_elements):
                    
                    # find a country_info under current country_element
                    country_info_div = country_element.find_element(By.CSS_SELECTOR, '.wa-geography__country-info')
                    
                    # find the <a> element under div_element
                    country_name_anchor = country_info_div.find_element(By.TAG_NAME, 'a')
                    
                    # grab country name
                    country_name = country_name_anchor.text
                    
                    # get us traffic or just get the least traffic
                    if (country_name == "United States" or i == len(country_elements) - 2):
                        
                        country_traffic_div = country_info_div.find_element(By.CSS_SELECTOR, '.wa-geography__country-traffic')
                        us_traffic = country_traffic_div.find_element(By.CSS_SELECTOR, '.wa-geography__country-traffic-value').text
                        
                        break
            else:
                return -1
            
        except:
            return -1
        
    except Exception as e:
        return -1
    
    finally:
        
        # Close the browser
        driver.quit()
        
        # adjust average duation format
        if aveDuation:
            # split the time string into hours, minutes, and seconds
            hours, minutes, seconds = map(int, aveDuation.split(':'))
            # convert hours, minutes, and seconds to total seconds
            aveDuration_in_seconds = (hours * 3600) + (minutes * 60) + seconds
        else:
            return -1
        
        # adjust visits format
        if visits:
            if visits.endswith('M'):
                visits_in_number = float(visits[:-1]) * 1000000
            elif visits.endswith('K'):
                visits_in_number = float(visits[:-1]) * 1000
            else:
                visits_in_number = float(visits)
        else:
            return -1
        
        # adjust us traffic format
        us_traffic_in_decimal = float(us_traffic.strip('%')) / 100
        
        # calculate output
        total_us_visit_duration = visits_in_number * aveDuration_in_seconds * us_traffic_in_decimal
        return (visits_in_number, aveDuration_in_seconds, us_traffic_in_decimal, total_us_visit_duration)
       
        
def main():
    
    filename = "input_test.txt"
    output_dic = {}
    visits = []
    aveDuration = []
    usTraffic = []
    
    # read piracy websites from file
    with open(filename, 'r') as file:
        # Read the contents of the file into a string
        file_contents = file.read()
    
    # split to a list of websites
    website_links = file_contents.split()
    
    for name in website_links:
        
        # use a regular expression to remove "http://" or "https://" and "www."
        name = re.sub(r"https?://(www\d?\.)?", "", name)

        # save line of data into dictionary
        similarWebData = getSimilarWebData(name)
        
        if (similarWebData != -1):
            # append data to 3 lists
            visits.append(similarWebData[0])
            aveDuration.append(similarWebData[1])
            usTraffic.append(similarWebData[2] * 100)
            
            # append dictionary entry of the output
            output_dic[name] = similarWebData[3]
            
    # create data frame
    df = pd.DataFrame(output_dic.items(), columns=['Piracy Sites', 'Total Visit Duration from US'])
    
    # add three more columns of original data
    df['Total Visits'] = visits
    df['Average Visit Duration (in seconds)'] = aveDuration
    df['US Traffic (in percentage)'] = usTraffic
    
    # set the float format to display numbers without scientific notation
    pd.options.display.float_format = '{:.1f}'.format

    print(df)
    
        
if __name__ == "__main__":
    main()