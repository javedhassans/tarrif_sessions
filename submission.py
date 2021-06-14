import sys
import os
import pandas as pd
import sqlite3

# TODO : make a function for this to
# def read_csv_to_datetime(filename, column1, column2):
#     """

#     :type filename: object
#     """
#     filename.strip('.csv')
#     df = pd.read_csv(filename)
#     df[column1] = pd.to_datetime(df[column1])
#     df[column2] = pd.to_datetime(df[column2])

tarrif = pd.read_csv('tariffs.csv')
tarrif['dt_start'] = pd.to_datetime(tarrif['dt_start'])
tarrif['dt_end'] = pd.to_datetime(tarrif['dt_end'])

session = pd.read_csv('sessions.csv')
session['dt_start'] = pd.to_datetime(session['dt_start'])
session['dt_end'] = pd.to_datetime(session['dt_end'])


# TODO :  Make a function to do this.
conn = sqlite3.connect("library.db")
session.to_sql('session',conn, index=False)
tarrif.to_sql('tarrif',conn,index=False)

qry = '''
select s.id, s.dt_start, s.dt_end , s.energy, t.energy_fee, t.parking_fee
from session s join tarrif t
WHERE (s.dt_start between t.dt_start and t.dt_end)
and (s.dt_end between t.dt_start and t.dt_end)'''

df = pd.read_sql_query(qry, conn)

df['dt_start'] = pd.to_datetime(df['dt_start'])
df['dt_end'] = pd.to_datetime(df['dt_end'])

# TODO: make a function for this.
df['minutes'] = (df['dt_end'] - df['dt_start'])

df['minutes'] = df['minutes'].dt.components.minutes

df['tariff_cost'] =  (((df.energy * df.energy_fee) + (df.minutes*df.parking_fee)) * 1.15)

round(df.groupby('id')['tariff_cost'].sum(),2).to_csv('tariff_cost.csv')

# TODO : at end you can also save the csv in to sqlite DB.
