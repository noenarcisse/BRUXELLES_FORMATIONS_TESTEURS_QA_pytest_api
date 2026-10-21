from constants import BASE_URL
from helpers import getAllEvents, getEventsWithAvailability

events = getAllEvents()
eventswith6 = getEventsWithAvailability(BASE_URL, events, 6)

print (events)