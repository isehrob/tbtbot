from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# database engine which we will use everywhere
def get_engine():
	import configuration
	return create_engine('sqlite:///%s.db' % configuration.DB_NAME)


def get_db_session():
	# A sessionmaker() instance establishes all conversations with the database
	# and represents a "staging zone" for all the objects loaded into the
	# database session object. Any change made against the objects in the
	# session won't be persisted into the database until you call
	# session.commit(). If you're not happy about the changes, you can
	# revert all of them back to the last commit by calling
	# session.rollback()
	engine = get_engine()
	return sessionmaker(bind=engine)()


def create_all():
	from models import Base
	# models module is the module where the developer
	# creates his own models and Base is a declarative base
	# which has all info about user created models
	# and here we create them all with this information
	engine = get_engine()
	Base.metadata.create_all(engine)

