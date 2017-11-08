"""Calendar utils"""

import math

def jd_from_date(dd, mm, yy):
    day = (14 - mm) // 12
    year = yy + 4800 - day
    m = mm + 12*day -3
    julian_day = dd + (153*m+2)//5 + 365*year + year//4 - year//100 + year//400 - 32045
    if julian_day < 2299161:
        julian_day = dd + (153*m+2)//5 + 365*year + year//4 - 32083
    
    return julian_day

def get_new_moon_day(k, time_zone):
    T = k/1236.85; # Time in Julian centuries from 1900 January 0.5
    T2 = T * T
    T3 = T2 * T
    dr = math.pi/180
    Jd1 = 2415020.75933 + 29.53058868*k + 0.0001178*T2 - 0.000000155*T3
    Jd1 = Jd1 + 0.00033*math.sin((166.56 + 132.87*T - 0.009173*T2)*dr) # Mean new moon
    M = 359.2242 + 29.10535608*k - 0.0000333*T2 - 0.00000347*T3 # Sun's mean anomaly
    Mpr = 306.0253 + 385.81691806*k + 0.0107306*T2 + 0.00001236*T3 # Moon's mean anomaly
    F = 21.2964 + 390.67050646*k - 0.0016528*T2 - 0.00000239*T3; # Moon's argument of latitude
    C1 = (0.1734 - 0.000393*T)*math.sin(M*dr) + 0.0021*math.sin(2*dr*M)
    C1 = C1 - 0.4068*math.sin(Mpr*dr) + 0.0161*math.sin(dr*2*Mpr)
    C1 = C1 - 0.0004*math.sin(dr*3*Mpr)
    C1 = C1 + 0.0104*math.sin(dr*2*F) - 0.0051*math.sin(dr*(M+Mpr))
    C1 = C1 - 0.0074*math.sin(dr*(M-Mpr)) + 0.0004*math.sin(dr*(2*F+M))
    C1 = C1 - 0.0004*math.sin(dr*(2*F-M)) - 0.0006*math.sin(dr*(2*F+Mpr))
    C1 = C1 + 0.0010*math.sin(dr*(2*F-Mpr)) + 0.0005*math.sin(dr*(2*Mpr+M))
    
    if T < -11:
        deltat = 0.001 + 0.000839*T + 0.0002261*T2 - 0.00000845*T3 - 0.000000081*T*T3
    else:
        deltat= -0.000278 + 0.000265*T + 0.000262*T2

    JdNew = Jd1 + C1 - deltat

    return math.floor(JdNew + 0.5 + time_zone/24)

def get_sun_longitude(jdn, time_zone):
    T = (jdn - 2451545.5 - time_zone/24) / 36525 # Time in Julian centuries from 2000-01-01 12:00:00 GMT
    T2 = T*T
    dr = math.pi/180 # degree to radian
    M = 357.52910 + 35999.05030*T - 0.0001559*T2 - 0.00000048*T*T2 # mean anomaly, degree
    L0 = 280.46645 + 36000.76983*T + 0.0003032*T2 # mean longitude, degree
    DL = (1.914600 - 0.004817*T - 0.000014*T2)*math.sin(dr*M)
    DL = DL + (0.019993 - 0.000101*T)*math.sin(dr*2*M) + 0.000290*math.sin(dr*3*M)
    L = L0 + DL # true longitude, degree
    L = L*dr
    L = L - math.pi*2*(math.floor(L/(math.pi*2))) # Normalize to (0, 2*PI)
    return math.floor(L / math.pi * 6)

def get_lunar_month11(yy, time_zone):
    off = jd_from_date(31, 12, yy) - 2415021
    k = math.floor(off / 29.530588853)
    nm = get_new_moon_day(k, time_zone)
    sunLong = get_sun_longitude(nm, time_zone) # sun longitude at local midnight
    if sunLong >= 9:
        nm = get_new_moon_day(k-1, time_zone)

    return nm

def get_leap_month_offset(a11, time_zone):
    k = math.floor((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    last = 0
    i = 1 # We start with the month following lunar month 11
    arc = get_sun_longitude(get_new_moon_day(k+i, time_zone), time_zone)
    while True:
        last = arc
        i += 1
        arc = get_sun_longitude(get_new_moon_day(k+i, time_zone), time_zone);
        if arc != last and i < 14:
            break

    return i-1


def convertSolar2Lunar(dd, mm, yy, time_zone):
    dayNumber = jd_from_date(dd, mm, yy)
    k = math.floor((dayNumber - 2415021.076998695) / 29.530588853)
    monthStart = get_new_moon_day(k+1, time_zone)
    if monthStart > dayNumber:
        monthStart = get_new_moon_day(k, time_zone)

    a11 = get_lunar_month11(yy, time_zone)
    b11 = a11
    if a11 >= monthStart:
        lunarYear = yy
        a11 = get_lunar_month11(yy-1, time_zone)
    else:
        lunarYear = yy+1
        b11 = get_lunar_month11(yy+1, time_zone)

    lunarDay = dayNumber-monthStart+1
    diff = math.floor((monthStart - a11)/29)
    lunarLeap = 0
    lunarMonth = diff+11
    if b11 - a11 > 365:
        leapMonthDiff = get_leap_month_offset(a11, time_zone)
        if diff >= leapMonthDiff:
            lunarMonth = diff + 10
            if diff == leapMonthDiff:
                lunarLeap = 1

    if lunarMonth > 12:
        lunarMonth = lunarMonth - 12

    if lunarMonth >= 11 and diff < 4:
        lunarYear -= 1

    print str(lunarDay) + '/' + str(lunarMonth) + '/' + str(lunarYear)

convertSolar2Lunar(1,1,2017,7)