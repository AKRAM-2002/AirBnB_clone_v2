#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from os import getenv
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

class DBStorage:
    """This is the DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """
        This is the constructor for the DBStorage class
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')), pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)
        
    def all(self, cls=None):
        """ Query on the current database session depending of the class name (argument cls). """
        objs_list = []
        if cls:
            if isinstance(cls, str):
                try:
                    cls = globals().get(cls)
                except KeyError:
                    pass
            if issubclass(cls, Base):
                objs_list = self.__session.query(cls).all()
        else:
            for subClass in Base.__subclasses__():
                objs_list.extend(self.__session.query(subClass).all())
        objs_dict = {}
        for obj in objs_list:
            key = "{}.{}".format(obj.__class__.__name__, obj.id)
            objs_dict[key] = obj
        return objs_dict
            
    
    def new(self, obj):
        """ Add the object to the current database session """
        self.__session.add(obj)
    
    def save(self):
        """ Commit all changes of the current database session """
        self.__session.commit()
    
    def delete(self, obj=None):
        """ Delete from the current database session """
        if obj:
            self.__session.delete(obj)
    
    def reload(self):
        """ Reload objects from the database """
        Base.metadata.create_all(self.__engine)
        Session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(Session_factory)
        self.__session = Session()