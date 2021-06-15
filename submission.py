import sys
import os
import pandas as pd
import sqlite3
import time

start_time = time.time()

# import data and convert 'dt_start' &  'dt_end' to datetime format
tarrif = pd.read_csv('./data/input/tariffs.csv')
tarrif['dt_start'] = pd.to_datetime(tarrif['dt_start'])
tarrif['dt_end'] = pd.to_datetime(tarrif['dt_end'])

session = pd.read_csv('./data/input/sessions.csv')
session['dt_start'] = pd.to_datetime(session['dt_start'])
session['dt_end'] = pd.to_datetime(session['dt_end'])
session['minutes'] = (session['dt_end'] - session['dt_start']).dt.components.minutes

# TODO :  Make a function to do this.
# connect a sqlite library to perform joins
conn = sqlite3.connect("./data/output/library.db")
session.to_sql('session', conn, index=False, if_exists='replace' )
tarrif.to_sql('tarrif', conn, index=False, if_exists='replace')

qry = '''
select s.id, s.energy, s.minutes,t.energy_fee, t.parking_fee
from session s join tarrif t
WHERE (s.dt_start between t.dt_start and t.dt_end)
and (s.dt_end between t.dt_start and t.dt_end)'''

df = pd.read_sql_query(qry, conn)


df['tariff_cost'] = (((df.energy * df.energy_fee) + (df.minutes * df.parking_fee)) * 1.15)

round(df.groupby('id')['tariff_cost'].sum(), 2).to_csv('./data/output/tariff_cost.csv')

print('tarrif_cost file is sucessfully generated')
print('time taken for overall operations is {} seconds'.format(time.time() - start_time))
