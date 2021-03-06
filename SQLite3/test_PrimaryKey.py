# -*- coding: utf-8 -*-

# Standard library imports

# 3rd party imports
import pandas as pd
import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as error:
        print(error)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as error:
        print(error)


def create_project(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = ''' INSERT INTO projects(name,begin_date,end_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def create_task(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return: task id
    """
    sql = ''' INSERT INTO tasks(name,priority,status_id,project_id,begin_date,end_date)
              VALUES(?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET priority = ? ,
                  begin_date = ? ,
                  end_date = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM tasks")

    rows = cur.fetchall()
    for row in rows:
        print(row)


def select_task_by_priority(conn, priority):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE priority=?', (priority,))

    rows = cur.fetchall()
    for row in rows:
        print(row)


def multi_tables_query(conn):
    """
    Inner join query
    :param conn: the Connection object
    :return:
    """
    sql = '''
        SELECT
            projects.name,
            tasks.name,
            projects.id AS id_projects,
            tasks.id AS id_tasks,
            status_id
        FROM
            projects
            INNER JOIN tasks ON tasks.id = projects.id'''
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()
    for row in rows:
        print(row)


def delete_task(conn, id):
    """
    Delete a task by task id
    :param conn:  Connection to the SQLite database
    :param id: id of the task
    :return:
    """
    sql = 'DELETE FROM tasks WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()


def delete_all_tasks(conn):
    """
    Delete all rows in the tasks table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM tasks'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()


def main():
    database = r'Example\pythonsqlite.db'

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS projects (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        begin_date text,
                                        end_date text,
                                        UNIQUE (name, begin_date, end_date) ON CONFLICT IGNORE
                                    ); """

    sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    priority integer,
                                    status_id integer NOT NULL,
                                    project_id integer NOT NULL,
                                    begin_date text NOT NULL,
                                    end_date text NOT NULL,
                                    UNIQUE (name, begin_date, end_date) ON CONFLICT IGNORE
                                    FOREIGN KEY (project_id) REFERENCES projects (id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    with conn:
        # create projects table
        create_table(conn, sql_create_projects_table)
        # create tasks table
        create_table(conn, sql_create_tasks_table)

        # # create a new project
        # project = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30')
        # project_id = create_project(conn, project)
        #
        # # tasks
        # task_1 = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        # task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')
        #
        # # create tasks
        # create_task(conn, task_1)
        # create_task(conn, task_2)
        #
        # # update task
        # update_task(conn, (2, '2015-01-04', '2015-01-06', 2))

        # query data
        print('1. Query task by priority:')
        select_task_by_priority(conn, 1)
        print('2. Query all tasks')
        select_all_tasks(conn)

        # delete entries
        delete_task(conn, 2)
        # delete_all_tasks(conn)
        print('3. Query all tasks')
        select_all_tasks(conn)

        # multi tables query
        multi_tables_query(conn)

        # check duplicate strategy
        # Data end of day 1
        df = pd.read_excel(r'Example/projects.xlsx')
        nrows = df.to_sql('projects', conn, if_exists='append', index=False)
        print('We have inserted', nrows, 'records to the table.')
        df = pd.read_excel(r'Example/tasks.xlsx')
        nrows = df.to_sql('tasks', conn, if_exists='append', index=False)
        print('We have inserted', nrows, 'records to the table.')
        print('4. Query all tasks')
        select_all_tasks(conn)
        # Data end of day 2
        df = pd.read_excel(r'Example/projects_MAJ.xlsx')
        nrows = df.to_sql('projects', conn, if_exists='append', index=False)
        print('We have inserted', nrows, 'records to the table.')
        df = pd.read_excel(r'Example/tasks_MAJ.xlsx')
        nrows = df.to_sql('tasks', conn, if_exists='append', index=False)
        print('We have inserted', nrows, 'records to the table.')
        print('5. Query all tasks')
        select_all_tasks(conn)

        print('6. Query task by priority:')
        select_task_by_priority(conn, 2)


if __name__ == '__main__':
    main()
