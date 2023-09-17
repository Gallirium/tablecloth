# tablecloth
Automatic generation of SQL queries to create tables and fill with random values.

DISCLAIMER: The following probably only works on my machine, unless you happen to run the exact versions of Arch and MariaDB that I’m using.

First you have to actually create the database in mariadb:

MariaDB [(none)]> create database $DATABASE;

Then, using the mariadb-dump client, you can import the contents of the text file generated by the script into the table (as root):

mariadb -p $DATABASE < GENERATED.sql

The actual contents of the .sql file are directly editable, meaning that it is easy to write a script to generate a semi-functional database for us. I say semi-functional because I haven’t had the pleasure of trying to create primary and foreign keys yet. Defining a schema sounds like a ton of work.