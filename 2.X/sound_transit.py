#
# SoundTransit Interface to handle GTFS data from API.
#
# This provides a pythonic interface to the soundtransit GTFS API, allowing
# pythonic use of API data. This not a complete implementation, but shows
# how to use the python GTFS classes to pull data.
#

import datetime
import os
import pytz
import time
import urllib2
import xml.etree.ElementTree
import stop_schedule
import route


class BaseException(Exception):
  """ Base exception for class."""
  pass


class SoundTransitStop(object):
  """ Models a specific stop using api.pugetsound.onebusaway.org API.

  Attributes:
    API_BASE: String base URL for API.
    CACHE_LOCATION_PREFIX: String file locaiton prefix, if cache
        should be stored outside of working directory.
  """
  API_BASE = 'http://api.pugetsound.onebusaway.org/api/where'
  CACHE_LOCATION_PREFIX = ''

  def __init__(self, agency_id, stop_id, api_key,
               timezone=None, cache_lifetime=86400):
    """ Initialize OneBusAway Interface.

    Args:
      agency_id: Integer agency ID from
          https://www.soundtransit.org/Developer-resources/Data-downloads
        stop_id: Integer stop ID from
          http://developer.onebusaway.org/tmp/sound/gtfs/modified_staged/1_gtfs.zip/stops.txt 
      api_key: String API key to use for querying servers.
      timezone: pytz.timezone object for local timezone. Default UTC.
      cache_lifetime: Integer number of seconds queries are cached locally in
          seconds. Default 86400 (one day).
    """
    self.agency_id = agency_id
    self.stop_id = stop_id
    self.api_key = api_key
    self.timezone = timezone or pytz.utc
    self.cache_lifetime = cache_lifetime
    self._cache_location = '%s%s-%s-schedule.xml' % (self.CACHE_LOCATION_PREFIX,
                                                     self.agency_id,
                                                     self.stop_id)

  def _QueryApi(self, endpoint, cache_location):
    """ Queries a specific API endpoint and store in local cache.

    Args:
      endpoint: String endpoint to query.
      cache_location: String file location to cache data to.
    """
    query = '%s/%s.xml?key=%s' % (self.API_BASE, endpoint, self.api_key)
    query = urllib2.Request(query)
    data = urllib2.urlopen(query)
    with open(cache_location, 'wb') as cache:
      cache.write(data.read())

  def _UpdateStopSchedule(self):
    """ Updates the cached stop schedule for a given stop.

    Cache lifetime applies.

    Args:
      agency_id: Integer agency ID to use. Default 1.
      stop_id: Integer stop ID to use.
    """
    if not os.path.isfile(self._cache_location):
      try:
        file = open(self._cache_location, 'w')
        file.close()
      except OSError:
        raise BaseException('Could not create schedule cache: %s' % e)      
    if ((abs(time.time() - os.path.getmtime(self._cache_location)) >
         self.cache_lifetime) or
        os.path.getsize(self._cache_location) == 0):
      self._QueryApi(
          'schedule-for-stop/%s_%s' % (self.agency_id, self.stop_id),
          self._cache_location)

  def GetStopSchedule(self):
    """ Returns python objects representing a stop schedule.

    Args:
      agency_id: Integer agency ID to use. Default 1.
      stop_id: Integer stop ID to use.

    Returns:
      Tuple of ({route short name: Route()}, {route_id: StopSchedule()}).
    """
    self._UpdateStopSchedule()
    tree = xml.etree.ElementTree.parse(self._cache_location)
    root = tree.getroot()

    loaded_routes = {}
    for routes in root.findall('.//routes'):
      for new_route in routes.getchildren():
        rt = route.Route()
        rt.InitFromElementTree(new_route)
        loaded_routes[rt.short_name] = rt

    stops = {}
    for stop_route_schedules in root.findall('.//stopRouteSchedules'):
      for stop_route_schedule in stop_route_schedules.getchildren():
        route_stop = stop_schedule.StopSchedule()
        route_stop.InitFromElementTree(stop_route_schedule)
        stops[route_stop.route_id] = route_stop

    return (loaded_routes, stops)

  def GetNextStops(self, route_short_name, count=3):
    """ Returns the next (count) number of stops for a given route.

    Args:
      route_short_name: String short route name to lookup.
      count: Integer number of next stops to return. Default 3.
      format: String format string to use for time (strftime). Default: %H:%M.

    Returns:
      List containing datetime TZ aware objects containing the next stops for
      the given route.
    """
    now = datetime.datetime.now(tz=pytz.utc)
    (routes, stops) = self.GetStopSchedule()
    next_stops = []
    for stop in stops[routes[route_short_name].id].stops:
      if stop.departure_datetime > now:
        next_stops.append(stop.departure_datetime)
        if len(next_stops) == count:
          break
    return next_stops
