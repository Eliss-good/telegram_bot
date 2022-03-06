
import time

end_time = '12:12:10'
splited_close_time = end_time.split(':')


close_time = time.time() + int(splited_close_time[0]) * 60 * 60 + int(splited_close_time[1]) * 60 + int(splited_close_time[2])
print(close_time)