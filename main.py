import pandas
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def scrape_business_tech():
    chrome_options = Options()
    chrome_options.add_experimental_option(
        # this will disable image loading
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )
    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=chrome_options)
    driver.get("https://businesstech.co.za/news/")
    driver.maximize_window()

    search_button = driver.find_element(by=By.CLASS_NAME, value="search-menu")
    search_button.click()

    search = driver.find_element(by=By.ID, value="s")
    search.send_keys("IT")
    search.send_keys(Keys.RETURN)

    try:
        heading = []
        links = []
        main = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "main"))
        )
        articles = main.find_elements(by=By.TAG_NAME, value="article")
        for article in articles:
            header = article.find_element(
                by=By.CLASS_NAME, value="entry-title > a")
            heading.append(header.text)
            link = header.get_attribute('href')
            links.append(link)

        data = {'Heading': heading, 'Link': links}
        df = pandas.DataFrame(data=data)
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.axis('tight')
        ax.axis('off')
        the_table = ax.table(cellText=df.values,
                             colLabels=df.columns, loc='center')

        pp = PdfPages("business_tech.pdf")
        pp.savefig(fig, bbox_inches='tight')
        pp.close()

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_business_tech()
