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


class Route(object):
  """ Manages a given route using GTFS specification.

  https://developers.google.com/transit/gtfs/reference/routes-file

  This is an incomplete implementation of a GTFS route, only enough to make it
  work with soundtransit.org.

  Attributes:
    id: String route ID.
    short_name: String short route name (e.g. 1, 13, D, 234x).
    long_name: String long route name (e.g. 1 Express).
    description: String description of the route.
    type: Integer route type. Default 3.
    url: String URL for the webpage of route.
    agency_id: Integer: agency ID for the route. Default 1.
  """
  def _InitManual(self, id, short_name, long_name=None, description=None,
                  type=None, url=None, agency_id=None):
    """ Initialize Route.

    As this is parsed from an xml object, we don't override the base init.

    Args:
      id: String route ID.
      short_name: String short route name (e.g. 1, 13, D, 234x).
      long_name: String long route name (e.g. 1 Express).
      description: String description of the route.
      type: Integer route type. Default 3.
      url: String URL for the webpage of route.
      agency_id: Integer: agency ID for the route. Default 1.
    """
    self.id = id
    self.short_name = short_name
    self.long_name = long_name
    self.description = description
    self.type = type or 3
    self.url = url
    self.agency_id = agency_id or 1

  def _InitUsingCamelCase(self, id, shortName, longName=None, description=None,
                          type=None, url=None, agencyId=None):
    """ Maps initialize to camelcase usage.

    Camelcase is used for attribute names, map to pythonic variable names.

    Args:
        id: String route ID.
        shortName: String short route name (e.g. 1, 13, D, 234x).
        long_name: String long route name (e.g. 1 Express).
        description: String description of the route.
        type: Integer route type. Default 3.
        url: String URL for the webpage of route.
        agencyId: Integer: agency ID for the route. Default 1.
    """
    self._InitManual(id, shortName, longName, description, type, url, agencyId)

  def InitFromElementTree(self, route):
    """ Initalize Route using an xml.etree.ElementTree object.

    Args:
      route: xml.etree.ElementTree object containing route data (<route>).
    """
    kwargs = {}
    for attrib in route.getchildren():
      kwargs[attrib.tag] = attrib.text
    self._InitUsingCamelCase(**kwargs)
