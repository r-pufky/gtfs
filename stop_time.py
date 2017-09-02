#
# opentransit.org python library.
#
# This provides skeleton classes required to turn given XML data from
# opentransit.org API into a pythonic object ready for easy use.
#
# This is an incomplete implementation - only what is currently needed is
# actually implemented.
#
# Classes follow the General Transit Feed Specification (GTFS) specification.
#   https://developers.google.com/transit/gtfs/
#

import datetime
import pytz


class StopTime(object):
  """ Manages a given stop time using GTFS specification.

  https://developers.google.com/transit/gtfs/reference/stop_times-file

  This is an incomplete implementation of GTFS stop times, only enough to make
  it work with soundtransit.org.

  Attributes:
    trip_id: String ID of the trip.
    arrival_time: Long unixtimestamp with MS for arrival time.
    departure_time: Long unixtimestamp with MS for departure time.
    arrival_enabled: Boolean True if arrival is enabled.
    departure_enabled: Boolean True if departure is enabled.
    service_id: String service ID.
  """
  def _InitManual(self, trip_id, arrival_time, departure_time,
                  arrival_enabled=True, departure_enabled=True,
                  service_id=None):
    """ Initialize Stop Time.

    As this is parsed from an xml object, we don't override the base init.

    As time data is returned with MS postpended with no separator, strip MS
    timing information when storing time data. Time is stored in UTC and will
    require applying timezone information to return the correct time, this
    can be done using .astimezone() with the datetime objects.

    Args:
      trip_id: String ID of the trip.
      arrival_time: Long unixtimestamp with MS for arrival time.
      arrival_datetime: datetime object containing UTC arrival time.
      departure_time: Long unixtimestamp with MS for departure time.
      departure_datetime: datetime object containing UTC departure time.
      arrival_enabled: Boolean True if arrival is enabled.
      departure_enabled: Boolean True if departure is enabled.
      service_id: String service ID.
    """
    self.trip_id = trip_id
    self.arrival_time = int(arrival_time[:-3])
    self.arrival_datetime = datetime.datetime.fromtimestamp(self.arrival_time, tz=pytz.utc)
    self.departure_time = int(departure_time[:-3])
    self.departure_datetime = datetime.datetime.fromtimestamp(self.departure_time, tz=pytz.utc)
    self.arrival_enabled = arrival_enabled
    self.departure_enabled = departure_enabled
    self.service_id = service_id

  def _InitUsingCamelCase(self, tripId, arrivalTime, departureTime,
                          arrivalEnabled, departureEnabled, serviceId):
    """ Maps initialize to camelcase usage.

    Camelcase is used for attribute names, map to pythonic variable names.

    Args:
      tripId: String ID of the trip.
      arrivalTime: Long unixtimestamp with MS for arrival time.
      departureTime: Long unixtimestamp with MS for departure time.
    """
    self._InitManual(tripId, arrivalTime, departureTime, arrivalEnabled,
                     departureEnabled, serviceId)

  def InitFromElementTree(self, stop_time):
    """ Initalize Route using an xml.etree.ElementTree object.

    Args:
      stop_time: xml.etree.ElementTree object containing stop time data
          (<scheduleStopTime>).
    """
    kwargs = {}
    for attrib in stop_time.getchildren():
      kwargs[attrib.tag] = attrib.text
    self._InitUsingCamelCase(**kwargs)
