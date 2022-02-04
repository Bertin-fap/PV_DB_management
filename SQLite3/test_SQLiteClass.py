# -*- coding: utf-8 -*-

# Standard library imports

# 3rd party imports
import sqlite3


class Employee:
    """A sample Employee class"""

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay

    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def __repr__(self):
        return "Employee('{}', '{}', {})".format(self.first, self.last, self.pay)


def insert_emp(conn, emp):
    cur = conn.cursor()
    cur.execute("INSERT INTO employees VALUES (:first, :last, :pay)",
                {'first': emp.first, 'last': emp.last, 'pay': emp.pay})


def get_emps_by_name(conn, lastname):
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return cur.fetchall()


def update_pay(conn, emp, pay):
    cur = conn.cursor()
    cur.execute("""UPDATE employees SET pay = :pay
                WHERE first = :first AND last = :last""",
                {'first': emp.first, 'last': emp.last, 'pay': pay})


def remove_emp(conn, emp):
    cur = conn.cursor()
    cur.execute("DELETE from employees WHERE first = :first AND last = :last",
                {'first': emp.first, 'last': emp.last})


def main():
    # create a database connection
    conn = sqlite3.connect(':memory:')

    # create employees table
    c = conn.cursor()
    c.execute('''CREATE TABLE employees (
                first text,
                last text,
                pay integer
                )''')

    emp_1 = Employee('John', 'Doe', 80000)
    emp_2 = Employee('Jane', 'Doe', 90000)

    with conn:
        insert_emp(conn, emp_1)
        insert_emp(conn, emp_2)

        emps = get_emps_by_name(conn, 'Doe')
        print(emps)

        update_pay(conn, emp_2, 95000)
        remove_emp(conn, emp_1)

        emps = get_emps_by_name(conn, 'Doe')
        print(emps)


if __name__ == '__main__':
    main()
