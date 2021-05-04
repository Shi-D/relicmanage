import pandas as pd
import csv
from datetime import datetime, timedelta, timezone



# 时间、人流量、是否下雨、是否周末、是否寒暑假期间
with open('museum.csv', 'w') as f:
    writer = csv.writer(f)

    date = datetime(2021, 4, 18)
    print(date)
    date_list = []

    for i in range(330):
        date_list.append(date)
        date -= timedelta(days=1)

    date_list.reverse()
    writer.writerow(['no', 'date', 'number', 'is_rain', 'is_weekends', 'is_vacation'])
    for i in range(330):
        if i % 7 == 0 or i % 7 == 6:
            writer.writerow([i, date_list[i], 1000, 0, 1, 0])
        else:
            writer.writerow([i, date_list[i], 1000, 0, 0, 0])

    print(date_list)