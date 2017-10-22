# gtfs
Python [GTFS](https://developers.google.com/transit/gtfs/) Skeleton
Implementation.

This is a skeleton library that provides Python classes for use with the
General Transit Feed Specification (GTFS). This is not a complete
implementation, and only features which are used have been implemented.

Classes follow the [General Transit Feed Specification (GTFS)](https://developers.google.com/transit/gtfs/)
unless otherwise noted.

# Python 2.X and 3.X Support
Compatible libraries for both 2.X and 3.X python are in respective directories
Import/use the right directory for the respective version of Python you are
using.

# Requirements
This library requires the use of the ```pytz``` library. Install the library
with

```bash
pip install pytz
```

Then ensure this library is in your project or Python path.

# Usage

```python
import pytz
from gtfs import sound_transit
transit = sound_transit.SoundTransitStop('agency', 'stop', 'api key')
transit.GetNextStops('A Line')
```
