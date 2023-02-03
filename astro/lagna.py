

from __future__ import division
from math import ceil
from collections import namedtuple as struct
import datetime
import swisseph as swe

Date = struct('Date', ['year', 'month', 'day'])
Place = struct('Place', ['latitude', 'longitude', 'timezone'])

sidereal_year = 365.256360417   # From WolframAlpha

planets = ['MERCURY', 'VENUS', 'SUN', 'MOON', 'MARS', 'JUPITER', 'SATURN', 'MEAN_NODE']
rasi = ['Mesha', 'Vrishaba', 'Mithuna', 'Karka', 'Simha', 'Kanya', 'Tula', 'Vrisch', 'Dhanu', 'Makara', 'Kumbha', 'Meena']

# namah suryaya chandraya mangalaya ... rahuve ketuve namah
swe.KETU = swe.PLUTO  # I've mapped Pluto to Ketu
planet_list = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER,
               swe.VENUS, swe.SATURN, swe.MEAN_NODE, # Rahu = MEAN_NODE
               swe.KETU, swe.URANUS, swe.NEPTUNE ]

# Convert 23d 30' 30" to 23.508333 degrees
from_dms = lambda degs, mins, secs: degs + mins/60 + secs/3600

# the inverse
def to_dms_prec(deg):
  d = int(deg)
  mins = (deg - d) * 60
  m = int(mins)
  s = round((mins - m) * 60, 6)
  return [d, m, s]

def to_dms(deg):
  d, m, s = to_dms_prec(deg)
  return [d, m, int(s)]


# Ketu is always 180° after Rahu, so same coordinates but different constellations
# i.e if Rahu is in Pisces, Ketu is in Virgo etc
ketu = lambda rahu: (rahu + 180) % 360

# Julian Day number as on (year, month, day) at 00:00 UTC
gregorian_to_jd = lambda date: swe.julday(date.year, date.month, date.day, 0.0)
jd_to_gregorian = lambda jd: swe.revjul(jd, swe.GREG_CAL)   # returns (y, m, d, h, min, s)

set_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_LAHIRI)
#set_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_TRUE_CITRA)
#set_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_TRUE_PUSHYA)
reset_ayanamsa_mode = lambda: swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)


def sidereal_longitude(jd, place, planet):
  """Computes nirayana (sidereal) longitude of given planet on jd"""
  lat, lon, tz  = place
  jd_utc = jd - (tz / 24.)
  set_ayanamsa_mode()
  longi = swe.calc_ut(jd_utc, planet, flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
  reset_ayanamsa_mode()
  longi_norm =  norm360(longi[0][0]) # degrees
  constellation = int(longi_norm / 30) 
  current = rasi[constellation]
  coordinates = to_dms(longi_norm % 30)

  return [current, coordinates]


solar_longitude = lambda jd, place: sidereal_longitude(jd, place, swe.SUN)
lunar_longitude = lambda jd, place: sidereal_longitude(jd, place, swe.MOON)

def local_time_to_jdut1(year, month, day, hour = 0, minutes = 0, seconds = 0, timezone = 0.0):
  """Converts local time to JD(UT1)"""
  y, m, d, h, mnt, s = swe.utc_time_zone(year, month, day, hour, minutes, seconds, timezone)
  # BUG in pyswisseph: replace 0 by s
  jd_et, jd_ut1 = swe.utc_to_jd(y, m, d, h, mnt, 0)
  return jd_ut1


def ascendant(jd, place):
    lat, lon, tz  = place
    jd_utc = jd - (tz / 24.)
    
    set_ayanamsa_mode()
    data = swe.houses_ex(jd_utc, lat, lon, flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL )
    nirayana_lagna = data[1][0]
    print(nirayana_lagna)
    rasi = int(nirayana_lagna/30)

    return rasi

def ascendant(jd, place):
  """Lagna (=ascendant) calculation at any given time & place"""
  lat, lon, tz = place
  jd_utc = jd - (tz / 24.)
  set_ayanamsa_mode() # needed for swe.houses_ex()

  # returns two arrays, cusps and ascmc, where ascmc[0] = Ascendant
  nirayana_lagna = swe.houses_ex(jd_utc, lat, lon, flags = swe.FLG_SIDEREAL)[1][0]
  # 12 zodiac signs span 360°, so each one takes 30°
  # 0 = Mesha, 1 = Vrishabha, ..., 11 = Meena
  constellation = int(nirayana_lagna / 30) 
  coordinates = to_dms(nirayana_lagna % 30)
  current = rasi[constellation]

  reset_ayanamsa_mode()
  return [current, coordinates]


def ascendant_tests():
  print(sys._getframe().f_code.co_name)
  jd = swe.julday(2015, 9, 24, 23 + 38/60.)
  assert(ascendant(jd, bangalore) == [2, [4, 37, 10]])
  jd = swe.julday(2015, 9, 25, 13 + 29/60. + 13/3600.)
  assert(ascendant(jd, bangalore) == [8, [20, 23, 31]])

# Make angle lie between [-180, 180) instead of [0, 360)
norm180 = lambda angle: (angle - 360) if angle >= 180 else angle;

# Make angle lie between [0, 360)
norm360 = lambda angle: angle % 360



def print_chart(jd, city):
    print("Lagna")
    print(ascendant(jd, city))
    for planet in planets:
        print(planet)
        code = getattr(swe, planet, False)
        print(sidereal_longitude(jd, city, code))



if __name__ == '__main__':
    now = datetime.datetime.now()
    #jd2 = local_time_to_jdut1(now.year, now.month, now.day, hour = now.hour, minutes = now.minute, seconds = now.second, timezone = -6.0)
    import sys
    bangalore = Place(12.972, 77.594, +5.5)
    visakhapatnam = Place(17.6868, 83.2185, +5.5)
    shillong = Place(25.569, 91.883, +5.5)
    helsinki = Place(60.17, 24.935, +2.0)
    austin = Place(30.2672, -97.7431, -6)
    #ascendant_tests()

    jd2 = swe.julday(now.year, now.month, now.day, now.hour + now.minute/60. + now.second/3600.)
    ganavika = swe.julday(2020, 8, 31, 18 + 0/60. + 0/3600.)
    sujeeth = swe.julday(2010, 2, 15, 14 + 35/60. + 0/3600.)
    sudeep = swe.julday(2010, 2, 15, 14 + 38/60. + 0/3600.)
    madhuri = swe.julday(1983, 10, 25, 7 + 40/60. + 0/3600.)
    date_2018_03_25 = swe.julday(2017, 11, 25, 7 + 40/60. + 0/3600.)
    #eswar = swe.julday(1985, 4, 10, 11 + 45/60. + 0/3600.)
    #print_chart(ganavika, visakhapatnam)
    #print_chart(sujeeth, visakhapatnam)
    #print_chart(sudeep, visakhapatnam)
    #print_chart(madhuri, visakhapatnam)
    #print_chart(eswar, visakhapatnam)
    #print_chart(jd2, austin)
    print_chart(date_2018_03_25, austin)



