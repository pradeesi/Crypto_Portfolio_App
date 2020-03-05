# For details refer to the following article -
# http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Create interface to the database
engine = create_engine('mysql+mysqlconnector://app_admin:inNovat1ve@localhost/crypto_db', echo=False)

# Instantiate a Base Class
Base = declarative_base()

# Crete ORM handle
Session = sessionmaker(bind=engine)
# Instantiate Session
session = Session()


# This block will aonly be used for Multi threading on MySQL Community Edition
# As MySQL Community Edition doesn't support multithreading
# we need to create a local db session for each thread
def local_db_session_for_multithreading_calls():
    # Crete ORM handle
    #Session = sessionmaker(bind=engine)
    return Session()

