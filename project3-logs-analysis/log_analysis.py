import psycopg2

def print_table(output):
    for x in output:
        print('')
        for value in x:
            print(value, "  " ,end='')


dbname = "news"
conn = psycopg2.connect(database=dbname)
cursor = conn.cursor()
print("The most popular articles of all time \n(Title, Views_Count):")
cursor.execute(
    """SELECT articles.title,
       count(log_slug.slug) AS views
    FROM articles
    LEFT JOIN log_slug ON articles.slug = log_slug.slug
    GROUP BY log_slug.slug,
             articles.title
    ORDER BY views DESC;"""
    )
print_table(cursor.fetchall())
print("\n=================")
print("The most popular article authors of all time \n(Author, Views_Count):")
cursor.execute(
    """SELECT authors.name,
           count(*) AS arcticle_views
    FROM articles,
         log_slug,
         authors
    WHERE articles.slug = log_slug.slug
      AND articles.author = authors.id
    GROUP BY authors.name
    ORDER BY arcticle_views DESC;"""
    )
print_table(cursor.fetchall())
print("\n=================")
print("Days where more than 1% of requests lead to errors: \n(Date, Error_Percentage)")
cursor.execute(
    """SELECT date(log1.time),
           ((CAST(log2.error AS DECIMAL) / count(*)) * 100) AS error_percentage
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
    HAVING ((CAST(log2.error AS DECIMAL) / count(*)) * 100) >= cast(1 AS DECIMAL);"""
    )
print_table(cursor.fetchall())
print("\n=================")
conn.close()
