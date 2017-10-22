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

import stop_time


class StopSchedule(object):
  """ Manages a given stop route schedule using GTFS specifications.

  This is a meta-class using definitions from:
  https://developers.google.com/transit/gtfs/reference/stop_times-file
  https://developers.google.com/transit/gtfs/reference/trips-file

  to define all the stops a given route has at a specified stop. This is a
  generated class, and does not appear in GTFS. This does not currently
  make a distinction between stop directions as directionality is not
  currently needed for my purposes :)

  Attributes:
    route_id: String route ID. 
    stops: List containing StopTimes for given route.
  """
  def __init__(self):
    """ Initialize Stop Time. """
    self.route_id = None
    self.stops = []

  def InitFromElementTree(self, stop_route_schedule):
    """ Initalize Route using an xml.etree.ElementTree object.

    Args:
      stop_route_schedule: xml.etree.ElementTree object containing stop time
          data (<stopRouteSchedule>).
    """
    kwargs = {}
    for attrib in stop_route_schedule.getchildren():
      if attrib.tag == 'routeId':
        self.route_id = attrib.text
      else:
        for schedule in attrib.findall('.//scheduleStopTimes'):
          for stop in schedule.getchildren():
            time = stop_time.StopTime()
            time.InitFromElementTree(stop)
            self.stops.append(time)
