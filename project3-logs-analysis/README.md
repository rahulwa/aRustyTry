## Log Analysis Project

This project is an internal reporting tool that will use information from the `news` database to discover what kind of articles the a news site's readers like and errors.

Setting up `news` database

- From the command line, launch the psql console by typing: `psql`
- Check to see if a news database already exists by listing all databases with the command: `\l`
- If a news database already exists, drop it with the command: `DROP DATABASE news`;
- Create the news database with the command: `CREATE DATABASE news`;
- exit the console by typing: `\q`
- [Download the schema and data for the news database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- Unzip the downloaded file. You should now have an sql script called newsdata.sql.
- From the command line, navigate to the directory containing newsdata.sql.
- Import the schema and data in newsdata.sql to the news database by typing: `psql -d news -f newsdata.sql`


Run this project:
`python3 log_analysis.py`


Not using sql views for this project.