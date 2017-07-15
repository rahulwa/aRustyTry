## Log Analysis Project

This project is an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like and errors.

Setting up `news` database

- [Download database from here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- unzip and import it in postgresql by running
 	`psql -d news -f newsdata.sql`

Run this project:
`python3 log_analysis.py`


Used SQL view is

```sql
CREATE VIEW log_slug AS
SELECT ip,
       METHOD,
       status,
       id,
       TIME,
       path,
       trim(LEADING '/arcticle'
            FROM path) "slug"
FROM log;
```
