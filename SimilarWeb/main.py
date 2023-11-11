from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import re

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
            us_traffic_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.wa-geography__country.wa-geography__legend-item .wa-geography__country-traffic-value')))
            us_traffic = us_traffic_element.text
        except:
            us_traffic = "N/A"
        
    except Exception as e:
        return -1
    
    finally:
        
        # Close the browser
        driver.quit()
        
        """
        # adjust average duation format
        if aveDuation:
            # Split the time string into hours, minutes, and seconds
            hours, minutes, seconds = map(int, aveDuation.split(':'))
            # Convert hours and minutes to total minutes
            aveDuation_in_minutes = (hours * 60) + minutes
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
        """
        
    return (visits, aveDuation, us_traffic)
        
def main():
    
    filename = "input.txt"
    
    # read piracy websites from file
    with open(filename, 'r') as file:
        # Read the contents of the file into a string
        file_contents = file.read()
    
    # split to a list of websites
    website_links = file_contents.split()
    
    for name in website_links:
        
        # use a regular expression to remove "http://" or "https://" and "www."
        name = re.sub(r"https?://(www\d?\.)?", "", name)

        print(getSimilarWebData(name))
        
if __name__ == "__main__":
    main()