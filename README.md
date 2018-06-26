# Introduction:
Simple Django project to showcase the library parsing_tools.

# Minimum requirements:
The server responds to two urls:

# Test links
## '/opening-hours/'
This endpoint is managed by DRF (Django Rest Framework). It showcases how easy it is to use the library and how to integrate it with any backend. No authentication required (by design) to make it easier to test. The response for this endpoint is a dictionary with the day name as key and the opening hours string as a value.
```json
{
    "monday": "10 AM - 6 PM",
    "tuesday": "10 AM - 6 PM",
    "wednesday": "Closed",
    "thursday": "Closed",
    "friday": "Closed",
    "saturday": "Closed",
    "sunday": "Closed"
}
```

## 'opening-hours-string/'
This endpoint is plain text response.

# Extra:
TLDR; Caching the parsed responses to improve speed.
Because having views that renders responses is lame, I thought of a twist. In the module
```python
from opening_hours import extra
```
## Assumptions:
The extra module is experimenting the ability of having the parsed responses cached in the memory. The assumptions are:
1. Opening and closing hours are finite combination.
2. Opening and closing hours are probably similar for a lot of business in the same country/region.
3. Python json parsing is expensive.
4. Python dictionaries are comparably faster than parsing json payloads.

## Test method:
To test the assumptions, two function were created:
1. Direct parsing.
2. Trying to fetch from a dict, parse if not found and then save the parsed value in a dictionary. The key for the saved parsed value is the payload itself.

The two function then put into the test with a test sample. The test sample is a json payload for one day that has one opening and one closing. The opening and closing time of the sample is randomly selected from the hours of the day (24). The test sample is restricted to one day only to have more controlled sample.

## Test result:
The dictionary was filled fast with the 576 possible combinations of the opening and closing hours and the speed ramped up drastically compared to the direct parsing that has constant time. Fetching from dictionary is constant time as well, that time thou is less than the parsing time.
result
```
Final results: dict result: 0.08882951736450195second, parse result: 6.097273826599121second, summation of time diffs: -6.008444309234619second, db length: 576 item and db size:153361byte
```
From the small test sample and after 100,000 iterations: The dict caching is working great.

## Where to go from here?
Many suggestions to resume:
1. Think of using memcache to be able to persist results after threads and between servers.
2. Check the size of the actual production sample. the size might balloon fast.
