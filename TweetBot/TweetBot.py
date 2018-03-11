import pandas as pd
import datetime
from datetime import timedelta
from dateutil import parser
import re
import tweepy
import time
from datetime import date
from pandas import DateOffset
import math
from dateutil.relativedelta import MO, TU, WE, TH, FR, SA, SU
from pandas.tseries.offsets import Easter, Day
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, \
    USMartinLutherKingJr, USPresidentsDay, USMemorialDay, \
    USLaborDay, USThanksgivingDay, USColumbusDay
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar

class tweetbot:
    
    def __init__(self):
        self.time = parser.parse("8:00am")
        self.interval = self.get_timedelta("1d")
    
    def check(self):
        '''Checks to see if tweet conditions are met. If they are,
        it tweets'''
        # takes the difference of the time of the next tweet and current
        # time
        time_difference = self.time - datetime.datetime.now()
        print('Time until next tweet: ',
                timedelta.total_seconds(time_difference))
        # if that time difference is less than zero meaning that the time has
        # passed, the program will send an tweet
        if timedelta.total_seconds(time_difference) < 0:
            print('Time is up. Sending Tweet...')
            # adds the time interval to the time when the email was supposed
            # to be sent
            self.time += self.interval
            self.send_tweet(self.get_tweet_message())
            
    def get_timedelta(self, time_str):
        '''Creates a timedelta from a time interval'''
        regex = re.compile(
                        r'((?P<days>\d+?)d)?((?P<hours>\d+?)hr)?((?P<minutes>\d+?)m)?((?P<seconds>\d+?)s)?')
        parts = regex.match(time_str)
        if not parts:
            return
        parts = parts.groupdict()
        time_params = {}
        for (name, param) in parts.items():
            if param:
                time_params[name] = int(param)
        return timedelta(**time_params)
    
    def get_tweet_message(self):
        class TweetHolidays(AbstractHolidayCalendar):
            rules = [
                Holiday('New Years Day', month=1, day=1, observance=nearest_workday),
                USMartinLutherKingJr,
                Holiday("Valentines's Day", month=2, day=14),
                USPresidentsDay,
                Holiday('Pi Day', month=3, day=14),
                Holiday("Saint Patrick's Day", month=3, day=17),
                Holiday('April Fools', month=4, day=1),
                Holiday('Earth Day', month=4, day=22),
                Holiday("Easter", month=1, day=1, offset=[Easter(), Day(0)]),
                Holiday('May the Fourth', month=5, day=4),
                Holiday("Mothers's Day", month=5, day=1, offset=DateOffset(weekday=SU(2))),
                USMemorialDay,
                Holiday("Father's Day", month=6, day=1, offset=DateOffset(weekday=SU(3))),
                Holiday('July 4th', month=7, day=4, observance=nearest_workday),
                USLaborDay,
                Holiday('Halloween', month=10, day=31),
                USColumbusDay,
                Holiday('Veterans Day', month=11, day=11, observance=nearest_workday),
                USThanksgivingDay,
                Holiday('Christmas', month=12, day=25, observance=nearest_workday)
            ]
        
        cal = TweetHolidays()
        dr = pd.date_range(start=date(date.today().year, 1, 1), end=date(date.today().year, 12, 31))
        holidays = cal.holidays(start=dr.min(), end=dr.max())
        holidaynames = cal.holidays(start=dr.min(), end=dr.max(), return_name=True)
        for x in range(0, len(cal.rules)):
            time_difference = parser.parse(str(holidays[x])) - datetime.datetime.now()
            if timedelta.total_seconds(time_difference) > -86400:
                daysuntil = str(time_difference).split(" ",1)
                try:
                    countdown = int(math.ceil(float(daysuntil[0])))+1
                except:
                    countdown = 1
                    
                if countdown == 0:
                    return("Today is "+holidaynames[x])
                elif countdown == 1:
                    return(str(countdown)+" day until "+holidaynames[x])
                else:
                    return(str(countdown)+" days until "+holidaynames[x])
                break
        
    def send_tweet(self, message):
        CONSUMER_KEY ="XXXXXX"
        CONSUMER_SECRET = "XXXXXX"   
        ACCESS_KEY = "XXXXXXXX"    
        ACCESS_SECRET = "XXXXXXX"
        
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        
        api = tweepy.API(auth)
        api.update_status(message)
        print("Tweet Sent: "+message)
    
if __name__ == "__main__":
    app = tweetbot()
    while(True):
        app.check()
        time.sleep(60)