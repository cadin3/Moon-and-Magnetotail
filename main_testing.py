import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import ephem
import sys
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Circle, PathPatch
import mpl_toolkits.mplot3d.art3d as art3d
from GEItoGSE import GEItoGSE
from find_full_moons import find_full_moons


def main(start_date, end_date):
    #create an array of dates for the analysis, with a cadence of 1 hour
    dates = []
    while start_date <= end_date:
        dates.append(start_date)
        start_date += dt.timedelta(hours=1)
    dates = np.array(dates)
    moon_phase = []
    moon_ra = [] #radians
    moon_dec = [] #radians
    moon_dist = [] #km
    moon_GSE = np.zeros((3,len(dates)))
    for date, i in zip(dates, range(len(dates))): #loop through the dates and compute the phase and position information for the moon 
        m = ephem.Moon(date)
        moon_phase.append(m.moon_phase)
        m_ra = float(repr(m.ra)) #to get in radians
        moon_ra.append(m_ra)
        m_dec = float(repr(m.dec)) #to get in radians
        moon_dec.append(m_dec)
        distance = m.earth_distance * 1.495978707e8 #km
        moon_dist.append(distance)

        GSE_coords = GEItoGSE(m_ra, m_dec, distance, date.year, date.month, date.day, (date.hour+(date.minute/60.))) 
        moon_GSE[:,i] = GSE_coords.reshape(3)
    moon_phase = np.array(moon_phase)*100 #percentage
    full_moon_indices = find_full_moons(dates, moon_phase) #get indices of the full moons
    #make the moon phase plot
    plt.rcParams.update({'font.size': 16})
    fig,ax = plt.subplots(figsize=(16,6))
    ax.plot(dates, moon_phase)
    counter = 0
    for idx in full_moon_indices:
        counter += 1
        if counter == 1:
            ax.plot(dates[(idx-72):(idx+73)], moon_phase[(idx-72):(idx+73)], c='red', label='Magnetotail') #highlight 6 days around the full moon time, since the moon spends ~6 days inside the magnetotail
        else:
            ax.plot(dates[(idx-72):(idx+73)], moon_phase[(idx-72):(idx+73)], c='red')
    ax.set_title('Moon Phase over Time (100% = Full Moon)')
    ax.set_xlabel('Date (Year-Month)')
    ax.set_ylabel('% of Surface Illuminated')
    plt.legend(loc='best')
    plt.show()


start_date_str = 'Jul 1 2013'
end_date_str = 'Sep 1 2013'

start_date = dt.datetime.strptime(start_date_str, '%b %d %Y')
end_date = dt.datetime.strptime(end_date_str, '%b %d %Y')
main(start_date, end_date)