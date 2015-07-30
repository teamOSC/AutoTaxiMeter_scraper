#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import sys
from bs4 import BeautifulSoup
import os
import json
import re

def main():
    arr =[]
    url = 'http://www.taxiautofare.com/Taxi-Fare-Card.aspx'
    soup = BeautifulSoup( urllib2.urlopen(url).read() )
    metadata2 = soup.find('span',{'id' : 'MC_lblCabRates'})
    table2 = metadata2.findNext('table')
    metadata = soup.find('span',{'id' : 'MC_lblTaxiRates'})
    table = metadata.findNext('table')

    for j in table.find_all('a'):
        url = 'http://www.taxiautofare.com/' + j.get('href')
        print url
        arr.append( scrape(url) )
    for j in table2.find_all('a'):
        url = 'http://www.taxiautofare.com/' + j.get('href')
        print url
        try:
            arr.append( scrape(url) )
        except:
            print "Could not access this fare"


    with open("./autotaxi.txt", "w") as f:
        f.write(json.dumps(arr))

def scrape(url='http://www.taxiautofare.com/taxi-fare-card/Chandigarh-Auto-fare'):
        dict = {}
	soup = BeautifulSoup( urllib2.urlopen(url).read() )
        metadata = soup.find('span',{'id' : 'BottomContent_lblFareBreakup'})
        #dict['vehicle'] = 'taxi'
        try:
            dict['operator'] = metadata.get_text()
            dict['booking_fee'] = metadata.findNext('table').find('span',{'id' : 'BottomContent_lblBookingFee'}).get_text()[2:4]

            dict['min_fare'] = metadata.findNext('table').find('span',{'id' : 'BottomContent_lblMinimumFare'}).get_text().split(' ')[0][2:]
            dict['min_dist'] = metadata.findNext('table').find('span',{'id' : 'BottomContent_lblMinimumFare'}).get_text().split(' ')[-1][0]

            dict['fare_per_km'] = metadata.findNext('table').find('span',{'id' : 'BottomContent_lblFarePerUnitDistance'}).get_text()[2:4]
            dict['waiting_charges'] = metadata.findNext('table').find('span',{'id' : 'BottomContent_lblWaitingCharges'}).get_text()
            #dict['night_booking_fee'] = metadata.findNext('table').find('span',{'id' : 'BottomContent_lblNightBookingFee'}).get_text()[2:4]
            #dict['night_gen_fare'] = metadata.findNext('table').find('span',{'id' : 'BottomContent_lblNightExtraFare'}).get_text()

            x = dict['operator']
            #Delhi Mega cabs fare breakup -> mega Cabs
            dict['operator'] = ' '.join( x.split(' ')[1:-2] )
            dict['city'] = ''.join( x.split(' ')[0] )

            a = dict['waiting_charges']
            dict['waiting_charges'] =  a[a.find('s')+1:a.find('.')]
        except:
        	print "Failed"

        return dict


if __name__ == '__main__':
    main()
    #print scrape()

