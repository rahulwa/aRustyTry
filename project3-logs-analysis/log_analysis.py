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
        # THEN perhaps exit the program
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
    for x in output:
        print('')
        for value in x:
            print(value, "  ", end='')
    print("\n=========================")


def print_top_articles():
    """
    Fetch top articles using helper function, print results
    """
    print("The most popular articles of all time \n(Title, Views_Count):")
    query = """SELECT articles.title,
               count(log_slug.slug) AS views
            FROM articles
            LEFT JOIN log_slug ON articles.slug = log_slug.slug
            GROUP BY log_slug.slug,
                     articles.title
            ORDER BY views DESC;"""
    results = fetch_query(query)
    print_table(results)


def print_top_authors():
    """
    Fetch top authors using helper function,
    print results
    """
    print("""The most popular article authors of all time \n
        (Author, Views_Count):""")
    query = """SELECT authors.name,
                   count(*) AS arcticle_views
            FROM articles,
                 log_slug,
                 authors
            WHERE articles.slug = log_slug.slug
              AND articles.author = authors.id
            GROUP BY authors.name
            ORDER BY arcticle_views DESC;"""
    results = fetch_query(query)
    print_table(results)


def print_top_error_days():
    """
    Fetch top error days using helper function, print results
    """
    print("""Days where more than 1% of requests lead to errors: \n
        (Date, Error_Percentage)""")
    query = """SELECT date(log1.time),
                   ((CAST(log2.error AS DECIMAL) / count(*)) * 100) AS Error_Percentage    # noqa
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
            HAVING ((CAST(log2.error AS DECIMAL) / count(*)) * 100) >= cast(1 AS DECIMAL);"""    # noqa
    results = fetch_query(query)
    print_table(results)


if __name__ == '__main__':
    print_top_articles()
    print_top_authors()
    print_top_error_days()
