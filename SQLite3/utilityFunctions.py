# -*- coding: utf-8 -*-

# Standard library imports
import sqlite3
from pathlib import Path

# 3rd party imports
import pandas as pd


def databaseConfiguration():
    """Database configuration details"""

    name_db = 'demoDB.db'
    path_db = r'Example'

    dbConfig = {'database': name_db,
                'path_db': Path(path_db) / Path(name_db),
                }

    return dbConfig


def connectToDataBase():
    """Connect to the database"""

    # Configuration details for accessing the database
    dbConfig = databaseConfiguration()

    connection_string = sqlite3.connect(dbConfig['path_db'])
    cursor = connection_string.cursor()
    print(f"Connection to {dbConfig['database']} established")

    return connection_string, cursor


def df2sqlite(dataframe, tbl_name='import'):
    """The function df2sqlite converts a dataframe into a sqlite database.

    Args:
       dataframe (panda.DataFrame): the dataframe to convert in a database
       tbl_name (str): name of the table
    """
    # Connect to the database
    conn, cur = connectToDataBase()

    # Creates a database and a table
    col_str = '"' + '","'.join(dataframe.columns) + '"'
    cur.execute(f"CREATE TABLE IF NOT EXISTS {tbl_name} ({col_str})")
    dataframe.to_sql(tbl_name, conn, if_exists='replace', index=False)

    print('data uploaded to database')

    # Disconnect to the database
    cur.close()
    conn.close()


def sqlite2df(tbl_name):
    """Read a database as a dataframe.
    """
    # Connect to the database
    conn, cur = connectToDataBase()

    dataframe = pd.read_sql_query("SELECT * FROM " + tbl_name, conn)

    # Disconnect to the database
    cur.close()
    conn.close()

    return dataframe
