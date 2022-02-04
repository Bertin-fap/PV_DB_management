# -*- coding: utf-8 -*-

# Standard library imports

# 3rd party imports
import pandas as pd

# Local imports
import utilityFunctions as uF


def createTable(dataset, tbl_name):
    """Create a table, put data and read data from db.
    """
    df = pd.read_excel(dataset)
    df.columns = [x.strip().replace(' ', '_') for x in df.columns]
    print(df.columns)

    uF.df2sqlite(df, tbl_name=tbl_name)

    userData = uF.sqlite2df(tbl_name)
    print(userData)


def directQuery(tbl_name):
    """Direct query of the database.
    """
    conn, cur = uF.connectToDataBase()

    # Query the database
    cur.execute('''  
                SELECT *
                FROM {0}
                WHERE (ID > "{1}")
              '''.format(tbl_name, '1153410'))

    dict_query = {i: row for i, row in enumerate(cur.fetchall())}

    # Disconnect to the database
    cur.close()
    conn.close()

    return dict_query


if __name__ == '__main__':

    # Data end of day 1
    tables_2401 = {
        'MEP': r'Example/Sample_MEP_2401.xlsx',
        'ReferenceLot': r'Example/Sample_ReferenceLots_2401.xlsx',
        'ScreenPrinting': r'Example/Sample_ScreenPrinting_2401.xlsx',
    }

    for table, data in tables_2401.items():
        createTable(data, table)

    query = directQuery('MEP')
    print(query)

    # Data end of day 2
    tables_2501 = {
        'MEP': r'Example/Sample_MEP_2501.xlsx',
        'ReferenceLot': r'Example/Sample_ReferenceLots_2501.xlsx',
        'ScreenPrinting': r'Example/Sample_ScreenPrinting_2501.xlsx',
    }

    for table, data in tables_2501.items():
        createTable(data, table)

    query = directQuery('MEP')
    print(query)
