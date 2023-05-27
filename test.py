from ScrapeGoogle import get_getyourguide_link
from ScrapeGetYourGuide import get_getyourguide_trips
import json


getyourguide_links = get_getyourguide_link("getyourguide Barcelona")
getyourguide_trips = get_getyourguide_trips(getyourguide_links)

print(getyourguide_trips)


