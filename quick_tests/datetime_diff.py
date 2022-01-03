from datetime import datetime
import time

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

time.sleep(2)
then = datetime.now()
# then = datetime(2005, 5, 17)

now = str(now)
then = str(then)

print(now)
date_time_obj = datetime.strptime(now, '%Y-%m-%d %H:%M:%S')
print(date_time_obj)

# diff = then - now
# print(diff.seconds)