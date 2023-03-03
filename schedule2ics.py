#!/usr/bin/env python
# coding: utf-8

# In[1]:


from icalendar import Calendar, Event
import pandas as pd

from datetime import datetime, timedelta
from io import StringIO
from os import scandir, getcwd
from urllib.parse import quote_from_bytes


# In[2]:


lst = [file for file in scandir(getcwd()) if '学生选课课程表' in file.name]
if len(lst) == 1:
    filename = lst[0].name
else:
    # 根据atime排序
    lst.sort(key=lambda file: file.stat().st_atime, reverse=True)
filename = lst[0]
del lst


# In[3]:


with open(filename, 'r') as f:
    html_str = f.read()

semester = '20' + html_str.split('（20', 1)[1].split('季学期）')[0] + '季学期'
dfs = pd.read_html(StringIO(html_str))


# In[4]:


df = dfs[0].iloc[:, [0, 4, 5]]
df.columns = ['name', 'teacher', 'time_loc']

for i in range(df.shape[0]):
    name = df.loc[i]['name'].split(']')[1]
    df.loc[i]['name'] = name

not_done = 1
while not_done:
    not_done = 0 
    for i in range(df.shape[0]):
        row = df.loc[i]
        if ';' in row['teacher']:
            not_done = 1
            teachers = row['teacher'].split(';', 1)
            time_locs = row['time_loc'].split('),', 1)
        
            df.loc[i]['teacher'] = teachers[0]
            df.loc[i]['time_loc'] = time_locs[0]
            
            new_row = pd.Series([row['name'], teachers[1], time_locs[1]],
                               index=df.columns)
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

not_done = 1
while not_done:
    not_done = 0
    for i in range(df.shape[0]):
        row = df.loc[i]
        if '),' in row['time_loc']:
            not_done = 1
            time_locs = row['time_loc'].split('),', 1)
            df.loc[i]['time_loc'] = time_locs[0]
            
            new_row = pd.Series([row['name'], row['teacher'], time_locs[1]],
                                index=df.columns)
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

df['time'] = ''
df['location'] = ''
for i in range(df.shape[0]):
    time, location = df.loc[i]['time_loc'].split('] ')
    location = location.split('(')[0]
    df.loc[i]['time'] = time
    df.loc[i]['location'] = location

del df['time_loc']

df['from_class'] = ''
df['to_class'] = ''
for i in range(df.shape[0]):
    time, classes = df.loc[i]['time'].split('[')
    if '-' in classes:
        from_class, to_class = classes.split('-')
    else:
        from_class = classes
        to_class = ''
    
    df.loc[i]['time'] = time
    df.loc[i]['from_class'] = from_class
    df.loc[i]['to_class'] = to_class

df['weeks'] = ''
df['day'] = ''
for i in range(df.shape[0]):
    weeks, day = df.loc[i]['time'].split('周 ')
    df.loc[i]['weeks'] = weeks
    df.loc[i]['day'] = day

del df['time']

not_done = 1
while not_done:
    not_done = 0
    for i in range(df.shape[0]):
        row = df.loc[i]
        if ',' in row['weeks']:
            not_done = 1
            weekss = row['weeks'].split(',')
            new_row = row.copy()
            new_row['weeks'] = weekss[1]
            
            df.loc[i]['weeks'] = weekss[0]
            df = pd.concat([df, new_row.to_frame().T], ignore_index=True)

df['from_week'] = ''
df['to_week'] = ''
for i in range(df.shape[0]):
    weeks = df.loc[i]['weeks']
    if '-' in weeks:
        from_week, to_week = weeks.split('-')
    else:
        from_week = weeks
        to_week = ''
    df.loc[i]['from_week'] = from_week
    df.loc[i]['to_week'] = to_week

del df['weeks']

cn = ['一', '二', '三', '四', '五', '六', '日']
num = range(1, 8)
weekday = dict(zip(cn, num))
for i in range(df.shape[0]):
    df.loc[i]['day'] = weekday[df.loc[i]['day']]

df = df[['name', 'teacher', 'location', 'day', 'from_class', 'to_class', 'from_week', 'to_week']]

df.sort_values(by=['day', 'from_week', 'from_class', 'name'], inplace=True, ignore_index=True)


# In[5]:


semester_start = datetime(2023, 2, 13)
dt0 = semester_start - timedelta(weeks=1, days=1)
class_time = {
    '1': (8, 0),
    '2': (8, 55),
    '3': (10, 0),
    '4': (10, 55),
    '5': (13, 30),
    '6': (14, 25),
    '7': (15, 30),
    '8': (16, 25),
    '9': (18, 0),
    '10': (18, 55),
    '11': (19, 50),
    '12': (20, 45)
}

cal = Calendar()
cal.add('prodid', 'Marco//schedule2ics')
cal.add('version', '2.0')

for i in range(len(df)):
    row = df.loc[i]
    # name, teacher, location, day, from_class, to_class, from_week, to_week
    dtday = dt0 + timedelta(
        weeks=int(row['from_week']),
        days=int(row['day'])
    )
    hours, minutes = class_time[row['from_class']]
    dtstart = dtday + timedelta(
        hours=hours,
        minutes=minutes
    )
    if any(row['to_class']):
        hours, minutes = class_time[row['to_class']]
        dtend = dtday + timedelta(
            hours=hours,
            minutes=minutes+45
        )
    else:
        dtend = dtstart + timedelta(
            minutes=45
        )
    
    # dtstamp, uid, dtstart, location, summary, transp, rrule, dtend
    event = Event()
    event.add('dtstamp', datetime.utcnow())
    event.add('uid', datetime.utcnow().strftime('%Y%m%dT%H%M%SZ-') + str(i) + '-Marco@BNU')
    event.add('dtstart', dtstart)
    event.add('location', row['location'])
    event.add('summary', row['name'] + ' ' + row['teacher'])
    event.add('transp', 'TRANSPARENT')
    if any(row['to_week']):
        count = int(row['to_week']) - int(row['from_week']) + 1
        event.add('rrule', {
            'FREQ': 'WEEKLY',
            'COUNT': str(count)
        })
    event.add('dtend', dtend)
    cal.add_component(event)

with open(semester+'.ics', 'wb') as f:
    f.write(cal.to_ical())


# In[6]:


with open('Apple.txt', 'w', encoding='utf-8') as f:
    f.write('data:text/calendar,' + quote_from_bytes(cal.to_ical()))

