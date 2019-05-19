#!/usr/bin/env python3

import psycopg2


def connect(database_name):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(database_name))
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database")
        sys.exit(1)


def fetch_query(query):
    """
    Connect to the database, query, fetch results,
    close connection, return results
    """
    db, cursor = connect("news")
    cursor.execute(query)
    results = cursor.fetchall()
    db.close()
    return results


def print_table(output):
    """
    Formats the output returned by database
    """
    for x in output:
        print('')
        for value in x:
            print(value, "  ", end='')
    print("\n" + "=" * 30)


def print_top_articles():
    """
    Fetch top articles using helper function, print results
    """
    print("""The 3 most popular articles of all time:
        (Title, Views_Count)""")
    query = """SELECT articles.title, views
            FROM articles
            LEFT JOIN (select path, count(path) as views
                       from log
                       where status like '%200%'
                       group by log.path) as log
            ON log.path = concat('/article/', articles.slug)
            ORDER BY views DESC limit 3;"""
    results = fetch_query(query)
    print_table(results)


def print_top_authors():
    """
    Fetch top authors using helper function,
    print results
    """
    print("""The most popular article authors of all time:
        (Author, Views_Count)""")
    query = """SELECT authors.name,
                   count(*) AS arcticle_views
            FROM articles
            JOIN authors ON authors.id = articles.author
            JOIN log ON log.path = concat('/article/', articles.slug)
            WHERE log.status = '200 OK'
            GROUP BY authors.name
            ORDER BY arcticle_views DESC;"""
    results = fetch_query(query)
    print_table(results)


def print_top_error_days():
    """
    Fetch top error days using helper function, print results
    """
    print("""Days where more than 1% of requests lead to errors:
        (Date, Error_Percentage)""")
    query = """SELECT date(log1.time),
                   ((CAST(log2.error AS DECIMAL)
                     / count(*)) * 100) AS Error_Percentage
            FROM log AS log1
            JOIN
              (SELECT count(*) AS error,
                      date(TIME) AS TIME
               FROM log
               WHERE status NOT LIKE '2%'
               GROUP BY date(TIME),
                        status) AS log2 ON date(log1.time) = date(log2.time)
            GROUP BY date(log1.time),
                     log2.error
            HAVING ((CAST(log2.error AS DECIMAL)
               / count(*)) * 100) >= cast(1 AS DECIMAL);"""
    results = fetch_query(query)
    # print(" {0:%B %d, %Y} - {1:.2f}% errors".format(date, percentage))
    print_table(results)


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
