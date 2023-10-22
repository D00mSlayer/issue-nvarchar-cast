Parameterized query shows NVARCHAR even for VARCHAR column?

Observation:
I have a table T_VARCHAR with columns - id (int) , name (varchar SQL_Latin1_General_CP1_CI_AS)

I observed that NVARCHAR is used when querying a VARCHAR column in SQL Server (got information from SQL Profiler).
In my example below, I am inserting simple ascii charset to observe the behaviour.

Profiler generated query:
1. Using PyODBC (default settings) inserting ASCII to T_VARCHAR
    declare @p1 int
    set @p1=4
    exec sp_prepexec @p1 output,N'@P1 nvarchar(188)',N'INSERT INTO t_varchar (name) OUTPUT inserted.id VALUES (@P1)',N'!"#$%&''()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    select @p1

2. Using PyODBC (setencoding property to utf-8) inserting ASCII to T_VARCHAR
    declare @p1 int
    set @p1=4
    exec sp_prepexec @p1 output,N'@P1 varchar(94)',N'INSERT INTO t_varchar (name) OUTPUT inserted.id VALUES (@P1)','!"#$%&''()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
    select @p1

Expectation:
Since the column is VARCHAR, shouldn't SQL Server use VARCHAR and not NVARCHAR? Also, reagarding the collate SQL_Latin1_General_CP1_CI_AS, I understand that SQL Server will try to find the closest match with the corresponding code page for any given character; which is CP1252 (https://en.wikipedia.org/wiki/Windows-1252). If it does not find any, it would just replace with `?`.

How to reproduce:
I have attached a github link with the code. Please have a look.

App stack:
SQL Server 2022
Python - 3.10
pyodbc - 4.0.35
schematics - 2.1.1
SQLAlchemy - 1.3.17
ODBC Driver - Microsoft ODBC 17 (https://learn.microsoft.com/en-us/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver16&tabs=alpine18-install%2Calpine17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#17)
