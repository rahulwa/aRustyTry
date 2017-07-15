## Log Analysis Project

This project is an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like and errors.

Run it:
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
