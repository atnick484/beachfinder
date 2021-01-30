## BEACHFINDER Design Document

In order to implement our app BeachFinder, we needed to address several things. First, we needed to figure out how to query a database of beaches based off a location. Next, we
knew we wanted to implement some sort of way to query the weather data for each beach location. Another step would be to present this data nicely so that the user could see
the list of beach locations. We will cover each part below:

### FINDING BEACHES
We began by looking for a way to query data based off a user's location. After implementing SQL databases in CS50 in the past, we decided a SQL table could serve as our database
of beaches. We searched the Internet for beach information data and found several databases that would allow us to download their data and import it into our own SQL database.
By running our python script `importBeaches.py`, we were many beaches from across the United States into our SQL ready to be queried.

### QUERYING THE DATABASE
We implemented the front-end of our site on `index.html` with several forms for the user to either get their location via Geocoding or enter their address. Then, we got these
inputs in the back-end in `application.py` and implemented code to query the database using SQLite3, getting all of the beaches that were within plus/minus 1 degree latitude and longitude.
Once we had a list of beaches near the user's entered location, we ran a haversine algorithm that determined the proximity of each beach to the user, sorted the list of
beaches by proximity, and then truncated the list at 10 beaches in order to not overwhelm the APIs (that we will discuss in the next section).

### FINDING WEATHER
We originally planned to webscrape the weather data from websites like weather.com and surfline.com, but we found several free weather APIs like ClimaCell and WeatherStack
that offered the data we needed easily. We implemented those next in `application.py` and ran through each beach in our SQL query, querying weather information for that beach and
adding it to the query `dict`. Once finished iterating through each beach and finding weather information, we now had the right things to pass onto our next page, `display.html`
in order to display the beaches.

### DISPLAYING BEACHES
We wanted to present our beach data in two ways: a table and a map.

##### TABLE
In our table, we basically gave each key/value pair from each dictionary (representing a beach) in our list of
beaches a new column and gave each beach a new row.

##### MAP
Mapping was one of the most challenging aspects of our project. While it greatly improved the front-end of our application, it was a lengthy process of trial and error to find
an API to suit our needs. We first tried TomTom, but later realized that MapQuest was easier to use and had a greater variety of more accurate functions. Our mapping process can
be split into geocoding, display, and directions.

###### GEOCODING
Geocoding was the most time-consuming part of the mapping process. It required us to learn how to utilize the MapQuest's Geocoding API to translate text fields into latitude and longitude
coordinates for the the SQL query and the weather APIs. The other challenge of Geocoding was figuring out how to POST the information to `application.py`,
as a standard HTML form would no longer work, since the info first had to be translated to coordinates. The alternative to geocoding was to access current location, which was not
too challenging through JavaScript's navigation object.

###### DISPLAY
MapQuest's Map API made displaying maps easy, so there wasn't much else that we had to do other than create maps and markers.

###### DIRECTIONS
MapQuest's Directions API also made directions easy, and a quick call to the MapQuest API provided step-by-step directions to the user. However, the challenge was creating the "Clear Directions"
button, which only appeared after getting directions and required more knowledge of MapQuest's directions API functions. Overall, mapping required a lot of JavaScript to integrate APIs, but really
contributed to the functionality and visual representation of our app.

### OTHER MISC. DESIGN
To make our website more presentable, we added a few extra things. We added a Bootstrap, which let us include a favicon, navbar, and special fonts to our site.
We also implemented an about page under `about.html` that gave a little more information about our application and introduced the creators (us!). Lastly, we added
a background color for our beaches table and a background image for the site.