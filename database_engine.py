from sqlalchemy import create_engine

def database_data():
    hostname="localhost"
    dbname="ge_data"
    uname="sumit"
    pwd="1234"
    tablename="final"

    engine = create_engine("mysql://{user}:{pw}@{host}/{db}"
                               .format(host=hostname, db=dbname,
                                       user=uname,pw=pwd))
    return engine

engine = database_data()