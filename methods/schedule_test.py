# from asyncio.windows_events import IocpProactor
# import schedule
# import time
# from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def joba():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print('-------------------------------------------')


'''
def autorun():
    scheduler = BlockingScheduler()
    scheduler.add_job(joba, 'interval', seconds=10)
    scheduler.start()



def job():
    print("I'm working...")


def spautojob():
    schedule.every(1).minutes.do(job)
    # https://www.jianshu.com/p/b77d934cc252
    # schedule.every().hour.do(job)
    # schedule.every().day.at("10:30").do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    # schedule.every().minute.at(":17").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)
'''
