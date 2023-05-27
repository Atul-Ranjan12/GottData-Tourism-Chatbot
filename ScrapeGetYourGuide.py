from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def get_driver(opts):
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=opts)


OPTIONS = Options()
OPTIONS.add_argument('--disable-gpu')
OPTIONS.add_argument('--headless')


class ScrapeGetYourGuide:
    def __init__(self):
        self.driver = get_driver(OPTIONS)

    def get_response(self, url: str) -> list:
        # Got to the webpage
        self.driver.get(url)
        print("Going to url: ", url)

        self.driver.implicitly_wait(10)

        # Find all the trips
        try:
            trips = self.driver.find_elements(By.CSS_SELECTOR, ".vertical-activity-card")
        except Exception as e:
            print("The following exception occured: ", e)
            return [{"message": "Could not find any trips", "status": 400}]

        if len(trips) != 0:
            res = []
            for trip in trips:
                single_trip = {}
                # Get the title of the trip
                try:
                    title = trip.find_element(By.CSS_SELECTOR, 'p[data-test-id="activity-card-title"]')
                    single_trip["title"] = title.text
                except Exception as e:
                    print("The following exception occured: ", e)
                    single_trip["title"] = ""

                # Get the rating of the trip
                try:
                    rating = trip.find_element(By.CSS_SELECTOR, 'span.rating-overall__rating-number')
                    single_trip["rating"] = rating.text
                except Exception as e:
                    print("The following exception occured: ", e)
                    single_trip["rating"] = "Not found"

                # Get the review of the trip
                try:
                    reviews = trip.find_element(By.CSS_SELECTOR, 'div.rating-overall__reviews span')
                    single_trip["num_reviews"] = reviews.text
                except Exception as e:
                    print("The following exception occured: ", e)
                    single_trip["num_reviews"] = "Not found"

                # Get the price of the trip
                try:
                    pricing_container = trip.find_element(By.CSS_SELECTOR, "div.baseline-pricing__container")
                    pricing_value = pricing_container.find_element(By.CSS_SELECTOR, "div.baseline-pricing__value")
                    pricing_category = pricing_container.find_element(By.CSS_SELECTOR, 'p.baseline-pricing__category')

                    single_trip["pricing_value"] = pricing_value.text
                    single_trip["pricing_category"] = pricing_category.text
                except Exception as e:
                    print("The following exception occured: ", e)
                    single_trip["pricing_value"] = "Not found"
                    single_trip["pricing_category"] = "Not found"

                # Add in success message
                single_trip["message"] = "Success!"
                single_trip["status"] = 200

                # Append to result
                res.append(single_trip)
        else:
            print("No trips were found")
            return [{"status": 400, "message": "Could not find any trips"}]

        return res


def get_getyourguide_trips(links: list) -> list:
    """
    Take as an input a list of urls of getyourguide pages and returns all
    the available trips
    :param links: urls of getyourguide pages
    :return: list og trips
    """
    res = []
    scraper = ScrapeGetYourGuide()
    for url in links:
        trips = scraper.get_response(url)
        res.extend(trips)

    return res

