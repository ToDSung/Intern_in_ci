# python db api 2.0 測試

## docker 
> docker search 
> 
## postgresql 
docker run --name postgresql -e POSTGRES_USER=username -e POSTGRES_PASSWORD=ciPs1618 -p 10001:5432 -d postgres

## maria db
docker run --name 'Mariadb' -e 'MYSQL_ROOT_PASSWORD=admin' -e 'MYSQL_USER=username' -e 'MYSQL_PASSWORD=ciPs1618' -p 10002:3306 -d mariadb --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

## mssql
docker run --name 'MSSQL2017' -e 'ACCEPT_EULA=Y' -e 'MSSQL_SA_PASSWORD=ciPs1618' -e 'MSSQL_PID=Developer' -e SQLSERVER_USER=username -e SQLSERVER_PASSWORD=ciPs1618 -p 10003:1433 -d microsoft/mssql-server-linux

## threadsafety
|threadsafety|	Meaning|
|--|--|
|0|Threads may not share the module.|
|1|Threads may share the module, but not connections.|
|2|Threads may share the module and connections.|
|3|Threads may share the module, connections and cursors.|

```python=
print(pymysql.threadsafety)
# 1
print(psycopg2.threadsafety)
# 2
print(pyodbc.threadsafety)
# 1
print(cx_Oracle.threadsafety)
# 2
```
## paramstyle
* qmark Question mark style, e.g. ...WHERE name=?
* numeric Numeric, positional style, e.g. ...WHERE name=:1
* named Named style, e.g. ...WHERE name=:name
* format ANSI C printf format codes, e.g. ...WHERE name=%s
* pyformat Python extended format codes, e.g. ...WHERE name=%(name)s
```python=
print(pymysql.paramstyle)
# pyformat
print(psycopg2.paramstyle)
# pyformat
print(pyodbc.paramstyle)
# qmark
print(cx_Oracle.paramstyle)
# named
```

## connect
```python=
import urllib
from sqlalchemy import create_engine, MetaData

#資料庫名稱為 username
postgre_engine = create_engine('postgresql+psycopg2://username:ciPs1618@192.168.66.67:10001')

#連線mysql時 必須先建好資料庫
maria_engine = create_engine('mysql+pymysql://root:admin@192.168.66.67:10002/db_api')

#資料庫名稱為 master
params = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=192.168.66.67,10003;UID=sa;PWD=ciPs1618")
mssql_engine = create_engine('mssql+pyodbc:///?odbc_connect={}'.format(params))

metadata = MetaData()

metadata.create_all(postgre_engine)
#metadata.create_all(maria_engine)
#metadata.create_all(mssql_engine)
                    
connection = postgre_engine.connect()
#connection = maria_engine.connect()
#connection = mssql_engine.connect()
```

## sqlalchemy 分為 core 及 ORM 
```python=
users = Table('users', metadata,
              Column('user_id', Integer(), primary_key=True),
              Column('username', String(15), nullable=False, unique=True),
              Column('email_address', String(255), nullable=False),
              Column('phone', String(20), nullable=False),
              Column('password', String(25), nullable=False),
              Column('created_on', DateTime(), default=datetime.now),
              Column('updated_on', DateTime(),
                     default=datetime.now, onupdate=datetime.now)
             )

def test_sqlalchemy_bulk_insert(n=100000, m=5000):
    t0 = time.time()
    test_list = generate_list(n)
    
    while test_list:
        t1=time.time()
        connection.execute(
            insert(users).values(test_list[:m])
        )
        test_list = test_list[m:]
        print(time.time()-t1)
    print("SQLAlchemy bulk insert: Total time for " + str(n) +" records " + str(time.time() - t0) + " secs")
```
# best 
```python=

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=False)
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)

def test_sqlalchemy_core(n=100000,m=5000):
    t0 = time.time()
    test_list = generate_list(n)
    
    while test_list:
        t1=time.time()
        connection.execute(
            Users.__table__.insert(),test_list[:m]
        )
        test_list = test_list[m:]
        print(time.time()-t1)
    print("SQLAlchemy Core: Total time for " + str(n) +" records " + str(time.time() - t0) + " secs")
```
