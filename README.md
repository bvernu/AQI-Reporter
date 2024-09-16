# AQI-Reporter
Air Quality Index Reporter
When given a coordinate or the name of a location, this program will output the x nearest locations that had an AQI higher than y within z miles. I integrated data from multiple APIs to accurately identify locations and retrieve real-time AQI information, providing users with precise and actionable air quality insights. This program can be especially useful for people with chronic respiratory problems; the quality of the air we breathe can have a dramatic impact on our short- and long-term health.

the user provides:
    - their location
    - a mile radius for how far away the locations found should be
    - the maximun number of locations that should be found
    - an AQI threshold, so that the program looks form locations with an AQI higher than the threshold provided

- using geocoding and longitudal and latitudal analysis, this program finds the distance between points to find the area relevant to the users search
- air quality data is provided by PurpleAir's Web API
- forward and reverse geocoding performed using Nominatims's API
- parsed JSON files using python library
