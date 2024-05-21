#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

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
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)
            
    
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

    def close(self):
        """ Remove the private session attribute"""
        self.__session.remove()