
import time
#import crud
import schedule
import threading





from datetime import date, timedelta


def test(whatever):
    
    
    print(whatever)
    

# Run job every 3 second/minute/hour/day/week,
# Starting 3 second/minute/hour/day/week from now
#schedule.every(3).seconds.do(test, whatever="ugh")

# def schedule_detailing():
#     import schedule
#     import time
#     schedule.every(3).seconds.do(lambda: print("ugh"))
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)



# Run job every day at specific HH:MM and next HH:MM:SS
#schedule.every().day.at("10:00").do(job)
# schedule.every().day.at("10:30:42").do(job)

# if __name__ == "__main__":
#   schedule_detailing()


    

# add this code to dundermain in the serverpage - done
# change time to 5min, see if the server picks it up
# Create a route that's a mockup of the text function - demo how it works
# take random med from the db and set up a test time function - click event 
# have a phone number to put in 

def run_continuously(interval=1):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


def background_job():
    print('Hello from the background thread')


schedule.every().second.do(background_job)

# Start the background thread
stop_run_continuously = run_continuously()

# Do some other things...
time.sleep(10)

# Stop the background thread
stop_run_continuously.set()
