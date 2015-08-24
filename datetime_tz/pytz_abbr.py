#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set ts=2 sw=2 et sts=2 ai:
#
# Copyright 2010 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Common time zone acronyms/abbreviations for use with the datetime_tz module.

*WARNING*: There are lots of caveats when using this module which are listed
below.

CAVEAT 1: The acronyms/abbreviations are not globally unique, they are not even
unique within a region. For example, EST can mean any of,
  Eastern Standard Time in Australia (which is 10 hour ahead of UTC)
  Eastern Standard Time in North America (which is 5 hours behind UTC)

Where there are two abbreviations the more popular one will appear in the all
dictionary, while the less common one will only appear in that countries region
dictionary. IE If using all, EST will be mapped to Eastern Standard Time in
North America.

CAVEAT 2: Many of the acronyms don't map to a neat Oslon timezones. For example,
Eastern European Summer Time (EEDT) is used by many different countries in
Europe *at different times*! If the acronym does not map neatly to one zone it
is mapped to the Etc/GMT+-XX Oslon zone. This means that any date manipulations
can end up with idiot things like summer time in the middle of winter.

CAVEAT 3: The Summer/Standard time difference is really important! For an hour
each year it is needed to determine which time you are actually talking about.
    2002-10-27 01:20:00 EST != 2002-10-27 01:20:00 EDT
"""
from __future__ import division
from past.utils import old_div

import datetime
import pytz
import pytz.tzfile


class tzabbr(datetime.tzinfo):
  """A timezone abbreviation.

  *WARNING*: This is not a tzinfo implementation! Trying to use this as tzinfo
  object will result in failure.  We inherit from datetime.tzinfo so we can get
  through the dateutil checks.
  """
  pass


# A "marker" tzinfo object which is used to signify an unknown timezone.
unknown = datetime.tzinfo()


regions = {"all": {}, "military": {}}
# Create a special alias for the all and military regions
all = regions["all"]
military = regions["military"]


def tzabbr_register(abbr, name, region, zone, dst):
  """Register a new timezone abbreviation in the global registry.

  If another abbreviation with the same name has already been registered it new
  abbreviation will only be registered in region specific dictionary.
  """
  newabbr = tzabbr()
  newabbr.abbr = abbr
  newabbr.name = name
  newabbr.region = region
  newabbr.zone = zone
  newabbr.dst = dst

  if abbr not in all:
    all[abbr] = newabbr

  if not region in regions:
    regions[region] = {}

  assert abbr not in regions[region]
  regions[region][abbr] = newabbr


def tzinfos_create(use_region):
  abbrs = regions[use_region]

  def tzinfos(abbr, offset):
    if abbr:
      if abbr in abbrs:
        result = abbrs[abbr]
        if offset:
          # FIXME: Check the offset matches the abbreviation we just selected.
          pass
        return result
      else:
        raise ValueError("Unknown timezone found %s" % abbr)
    if offset == 0:
      return pytz.utc
    if offset:
      return pytz.FixedOffset(old_div(offset,60))
    return unknown

  return tzinfos


# Create a special alias for the all tzinfos
tzinfos = tzinfos_create("all")


# Create the abbreviations.
# *WARNING*: Order matters!
tzabbr_register("A", "Alpha Time Zone", "Military", "Etc/GMT-1", False)
tzabbr_register("ACDT", "Australian Central Daylight Time", "Australia",
                "Australia/Adelaide", True)
tzabbr_register("ACST", "Australian Central Standard Time", "Australia",
                "Australia/Adelaide", False)
tzabbr_register("ADT", "Atlantic Daylight Time", "North America",
                "America/Halifax", True)
tzabbr_register("AEDT", "Australian Eastern Daylight Time", "Australia",
                "Australia/Sydney", True)
tzabbr_register("AEST", "Australian Eastern Standard Time", "Australia",
                "Australia/Sydney", False)
tzabbr_register("AKDT", "Alaska Daylight Time", "North America",
                "US/Alaska", True)
tzabbr_register("AKST", "Alaska Standard Time", "North America",
                "US/Alaska", False)
tzabbr_register("AST", "Atlantic Standard Time", "North America",
                "America/Halifax", False)
tzabbr_register("AWDT", "Australian Western Daylight Time", "Australia",
                "Australia/West", True)
tzabbr_register("AWST", "Australian Western Standard Time", "Australia",
                "Australia/West", False)
tzabbr_register("B", "Bravo Time Zone", "Military", "Etc/GMT-2", False)
tzabbr_register("BST", "British Summer Time", "Europe", "Europe/London", True)
tzabbr_register("C", "Charlie Time Zone", "Military", "Etc/GMT-2", False)
tzabbr_register("CDT", "Central Daylight Time", "North America",
                "US/Central", True)
tzabbr_register("CEDT", "Central European Daylight Time", "Europe",
                "Etc/GMT+2", True)
tzabbr_register("CEST", "Central European Summer Time", "Europe",
                "Etc/GMT+2", True)
tzabbr_register("CET", "Central European Time", "Europe", "Etc/GMT+1", False)
tzabbr_register("CST", "Central Standard Time", "North America",
                "US/Central", False)
tzabbr_register("CXT", "Christmas Island Time", "Australia",
                "Indian/Christmas", False)
tzabbr_register("D", "Delta Time Zone", "Military", "Etc/GMT-2", False)
tzabbr_register("E", "Echo Time Zone", "Military", "Etc/GMT-2", False)
tzabbr_register("EDT", "Eastern Daylight Time", "North America",
                "US/Eastern", True)
tzabbr_register("EEDT", "Eastern European Daylight Time", "Europe",
                "Etc/GMT+3", True)
tzabbr_register("EEST", "Eastern European Summer Time", "Europe",
                "Etc/GMT+3", True)
tzabbr_register("EET", "Eastern European Time", "Europe", "Etc/GMT+2", False)
tzabbr_register("EST", "Eastern Standard Time", "North America",
                "US/Eastern", False)
tzabbr_register("F", "Foxtrot Time Zone", "Military", "Etc/GMT-6", False)
tzabbr_register("G", "Golf Time Zone", "Military", "Etc/GMT-7", False)
tzabbr_register("GMT", "Greenwich Mean Time", "Europe", pytz.utc, False)
tzabbr_register("H", "Hotel Time Zone", "Military", "Etc/GMT-8", False)
#tzabbr_register("HAA", "Heure Avancée de l'Atlantique", "North America", "UTC - 3 hours")
#tzabbr_register("HAC", "Heure Avancée du Centre", "North America", "UTC - 5 hours")
tzabbr_register("HADT", "Hawaii-Aleutian Daylight Time", "North America",
                "Pacific/Honolulu", True)
#tzabbr_register("HAE", "Heure Avancée de l'Est", "North America", "UTC - 4 hours")
#tzabbr_register("HAP", "Heure Avancée du Pacifique", "North America", "UTC - 7 hours")
#tzabbr_register("HAR", "Heure Avancée des Rocheuses", "North America", "UTC - 6 hours")
tzabbr_register("HAST", "Hawaii-Aleutian Standard Time", "North America",
                "Pacific/Honolulu", False)
#tzabbr_register("HAT", "Heure Avancée de Terre-Neuve", "North America", "UTC - 2:30 hours")
#tzabbr_register("HAY", "Heure Avancée du Yukon", "North America", "UTC - 8 hours")
tzabbr_register("HDT", "Hawaii Daylight Time", "North America",
                "Pacific/Honolulu", True)
#tzabbr_register("HNA", "Heure Normale de l'Atlantique", "North America", "UTC - 4 hours")
#tzabbr_register("HNC", "Heure Normale du Centre", "North America", "UTC - 6 hours")
#tzabbr_register("HNE", "Heure Normale de l'Est", "North America", "UTC - 5 hours")
#tzabbr_register("HNP", "Heure Normale du Pacifique", "North America", "UTC - 8 hours")
#tzabbr_register("HNR", "Heure Normale des Rocheuses", "North America", "UTC - 7 hours")
#tzabbr_register("HNT", "Heure Normale de Terre-Neuve", "North America", "UTC - 3:30 hours")
#tzabbr_register("HNY", "Heure Normale du Yukon", "North America", "UTC - 9 hours")
tzabbr_register("HST", "Hawaii Standard Time", "North America",
                "Pacific/Honolulu", False)
tzabbr_register("I", "India Time Zone", "Military", "Etc/GMT-9", False)
tzabbr_register("IST", "Irish Summer Time", "Europe", "Europe/Dublin", True)
tzabbr_register("K", "Kilo Time Zone", "Military", "Etc/GMT-10", False)
tzabbr_register("L", "Lima Time Zone", "Military", "Etc/GMT-11", False)
tzabbr_register("M", "Mike Time Zone", "Military", "Etc/GMT-12", False)
tzabbr_register("MDT", "Mountain Daylight Time", "North America",
                "US/Mountain", True)
#tzabbr_register("MESZ", "Mitteleuroäische Sommerzeit", "Europe", "UTC + 2 hours")
#tzabbr_register("MEZ", "Mitteleuropäische Zeit", "Europe", "UTC + 1 hour")
tzabbr_register("MSD", "Moscow Daylight Time", "Europe",
                "Europe/Moscow", True)
tzabbr_register("MSK", "Moscow Standard Time", "Europe",
                "Europe/Moscow", False)
tzabbr_register("MST", "Mountain Standard Time", "North America",
                "US/Mountain", False)
tzabbr_register("N", "November Time Zone", "Military", "Etc/GMT+1", False)
tzabbr_register("NDT", "Newfoundland Daylight Time", "North America",
                "America/St_Johns", True)
tzabbr_register("NFT", "Norfolk (Island) Time", "Australia",
                "Pacific/Norfolk", False)
tzabbr_register("NST", "Newfoundland Standard Time", "North America",
                "America/St_Johns", False)
tzabbr_register("O", "Oscar Time Zone", "Military", "Etc/GMT+2", False)
tzabbr_register("P", "Papa Time Zone", "Military", "Etc/GMT+3", False)
tzabbr_register("PDT", "Pacific Daylight Time", "North America",
                "US/Pacific", True)
tzabbr_register("PST", "Pacific Standard Time", "North America",
                "US/Pacific", False)
tzabbr_register("Q", "Quebec Time Zone", "Military", "Etc/GMT+4", False)
tzabbr_register("R", "Romeo Time Zone", "Military", "Etc/GMT+5", False)
tzabbr_register("S", "Sierra Time Zone", "Military", "Etc/GMT+6", False)
tzabbr_register("T", "Tango Time Zone", "Military", "Etc/GMT+7", False)
tzabbr_register("U", "Uniform Time Zone", "Military", "Etc/GMT+8", False)
tzabbr_register("UTC", "Coordinated Universal Time", "Europe",
                pytz.utc, False)
tzabbr_register("V", "Victor Time Zone", "Military", "Etc/GMT+9", False)
tzabbr_register("W", "Whiskey Time Zone", "Military", "Etc/GMT+10", False)
tzabbr_register("WDT", "Western Daylight Time", "Australia",
                "Australia/West", True)
tzabbr_register("WEDT", "Western European Daylight Time", "Europe",
                "Etc/GMT+1", True)
tzabbr_register("WEST", "Western European Summer Time", "Europe",
                "Etc/GMT+1", True)
tzabbr_register("WET", "Western European Time", "Europe", pytz.utc, False)
tzabbr_register("WST", "Western Standard Time", "Australia",
                "Australia/West", False)
tzabbr_register("X", "X-ray Time Zone", "Military", "Etc/GMT+11", False)
tzabbr_register("Y", "Yankee Time Zone", "Military", "Etc/GMT+12", False)
tzabbr_register("Z", "Zulu Time Zone", "Military", pytz.utc, False)
