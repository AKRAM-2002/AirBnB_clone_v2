#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """ State class """
    __tablename__ ='states'
    name = Column(String(128), nullable = False)
    
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref="state", cascade="all, delete-orphans")
    else:
        @property
        def cities(self):
            """
            Getter for cities
            """
            import models
            from models.city import City
            cities = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    cities.append(city)
            return cities
    