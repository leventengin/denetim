from django.apps import AppConfig
import time, datetime


class IslemConfig(AppConfig):
    name = 'islem'

    def ready(self):
        print("işlem  apppppp.............................")
        s_time = datetime.datetime.now()
        while True:
            elapsed_time = datetime.datetime.now() - s_time
            print("elapsed time....", elapsed_time)
            #print("seconds....", elapsed_time.seconds())
            e_sec = elapsed_time.seconds
            print("e seconds......", e_sec)
            if e_sec > 30:
                print("işlem burada olacak...", datetime.datetime.now())
                s_time = datetime.datetime.now()
            else:
                pass
