## BEACHFINDER DOCUMENTATION

### HOW TO RUN
After you cd into the `/beachfinder` directory, run the command `flask run`. This command should result in a url
appearing in your terminal that you can click to access BeachFinder on the web.

### FUNCTIONS

##### FIND MY LOCATION VIA USER-ENTERED INFO
The first search bar prompts the user for street address, city, state, ZIP code, and the sorting criteria. The information
will be sorted by that criteria in ascending order. After this information is entered and the "Find Me a Beach!" button is pressed,
the ten beaches closest to that location
will be found. Try only entering one of the fields -- it still works!

##### FIND MY LOCATION BY GPS
Under the "Or Find Me" section, select a sorting criteria (or don't) and click "Find Me a Beach!" Within a few seconds,
you should have the ten beaches closest to you. Make sure to enable your location if your browser asks you to.

### RESULTS

##### MAP

Once results are displayed, you should see a map displaying the ten beaches close to you. The "You" flag marks your
current location or the inputted address, and the black pins mark the beaches. Click on a pin to see the name of the beach. You can drag the
map and zoom in and out. The map, having MapQuest's basic API capabilities, displays basic landmarks and other useful
location information.

##### TABLE

BeachFinder provides you all the relevant beach information there is to know. Look in the table for distance, temperature,
humidity, precipitation, sunrise, sunset, conditions, and directions. The table is sorted in ascending order in all these
categories.

##### DIRECTIONS

In the BeachFinder table, we have a "Get Directions" option under the "Conditions" column. Here, we are able to get
step-by-step directions from our current location or the address, city, state, or zip code we inputted,
to any beach in close proximity. A "Clear Directions" button appears once you set a route, so you can return to the
clean map and see the other beaches on it. Without clicking the "Clear Directions" button, you can also click on "Get
Directions" to another beach and the existing route and directions will be replaced.

### LINK TO DEMONSTRATION VIDEO:
https://youtu.be/R3VpAYjpoA4