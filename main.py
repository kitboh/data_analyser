from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import sys
import time
from selenium.common.exceptions import NoSuchElementException

# Create a new instance of Firefox driver
driver = webdriver.Firefox()
job_name = sys.argv[1] if len(sys.argv) > 1 else ""
if job_name == "":
    job_name = "Data Analyst"  # Fix: Replace '==' with '=' to assign the value
print(job_name)
formatted_name = job_name.replace(" ", "+")
url = f"https://uk.indeed.com/jobs?q={formatted_name}&l=St.+Asaph%2C+Denbighshire&sc=0kf%3Ajt%28permanent%29%3B&vjk=60c6296b5f85300e"
driver.get(url)
means = []
medians = []

# Rest of the code...
def average_salary(input):
    try:
        # Find numerical values beginning with £
        pattern = r"£[\d,]+"
        matches = re.findall(pattern, input)
        match_ints = []
        # Process the matches
        for match in matches:
            # Remove the £ symbol and commas from the string
            value = match.replace("£", "").replace(",", "")
            # Convert the string to a float or int
            value = int(value)
            # Do something with the numerical value
            match_ints.append(value)
        mean_value = sum(match_ints) / len(match_ints)
        median_value = sorted(match_ints)[len(match_ints) // 2]
        return mean_value, median_value
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 0, 0


job_data = []

# Run the loop 3 times
for _ in range(3):
    # Find elements by data-testid "slider_container"
    time.sleep(1)
    button_present = driver.find_elements(By.CLASS_NAME, 'css-yi9ndv.e8ju0x51')
    if button_present:
        button_present[0].click()
    time.sleep(1)
    jobs = driver.find_elements(By.CSS_SELECTOR, '[data-testid="slider_item"]')
    for job in jobs:
        job_title = job.find_element(By.CLASS_NAME, 'jobTitle')
        try:
            job_salary = job.find_element(By.CLASS_NAME, 'salary-snippet-container')
            mean_sal, median_sal = average_salary(job_salary.text)
        except NoSuchElementException:
            mean_sal, median_sal = 0, 0
        if all(word.lower() in job_title.text.lower() for word in job_name.split()) and "Junior" not in job_title.text:
            # Do something if job title contains all words in job_name and does not contain "Junior"
            if mean_sal != 0:
                means.append(mean_sal)
            if median_sal != 0:
                medians.append(median_sal)
            job_data.append({
                "title": job_title.text,
                "av_salary": str(mean_sal) + " " + str(median_sal)
            })
    # Check if the button with id "onetrust-accept-btn-handler" is present
    try:
        if driver.find_elements(By.ID, "onetrust-accept-btn-handler"):
            # Click the button
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    except Exception as e:
        print(f"An error occurred while accepting cookies: {str(e)}")
    max_retry = 3
    retry_count = 0
    while retry_count < max_retry:
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="pagination-page-next"]')
            time.sleep(1)
            next_button.click()
            break
        except Exception as e:
            print(f"An error occurred while clicking the next button: {str(e)}")
            retry_count += 1
    else:
        print("Failed to click the next button after multiple retries")


# Close the driver
driver.quit()

# new_driver = webdriver.Firefox()
# new_url = "https://www.totaljobs.com/jobs/permanent/data-analyst/in-st-asaph?radius=20"
# new_driver.get(new_url)

# # Find elements with data-at attribute and id "job-item"
# job_items = new_driver.find_elements(By.CSS_SELECTOR, '[data-at="job-item"]')

# # Process the job items
# # Wait for the popup to show
# popup = WebDriverWait(new_driver, 10).until(EC.presence_of_element_located((By.ID, 'ccmgt_explicit_accept')))
# # Press the button
# popup.click()
# for job_item in job_items:
#     # Extract the job details job-item-salary-info
#     job_title = job_item.find_element(By.CSS_SELECTOR, '[data-at="job-item-title"]')
#     job_salary = job_item.find_element(By.CSS_SELECTOR, '[data-at="job-item-salary-info"]')
#     mean_sal, median_sal = average_salary(job_salary.text)

#     if "Data" in job_title.text and "Analyst" in job_title.text and "Junior" not in job_title.text:
#         # Do something if job title contains "Data Analyst"
#         if mean_sal != 0:
#             means.append(mean_sal)
#         if median_sal != 0:
#             medians.append(median_sal)
#         job_data.append({
#             "title": job_title.text,
#             "av_salary": str(mean_sal) + " " + str(median_sal)
#         })
# new_driver.quit()


# Write job data to a text file
with open("job_data.txt", "w") as file:
    for job in job_data:
        print(job)
        file.write(f"Title: {job['title']}\nSalary: {job['av_salary']}\n")



mean_of_means = sum(means) / len(means)
median_of_medians = sorted(medians)[len(medians) // 2]
print("Mean of means:", mean_of_means)
print("Median of medians:", median_of_medians)
# Append mean of means and median of medians to the end of the job_data.txt file
with open("job_data.txt", "a") as file:
    file.write(f"Mean of means: {mean_of_means}\n")
    file.write(f"Median of medians: {median_of_medians}\n")