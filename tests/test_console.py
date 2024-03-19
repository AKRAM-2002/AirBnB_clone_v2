#!/usr/bin/python3
"""
A unit test module for the console command 
"""

import unittest
import sqlalchemy

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User


class TestHBNBCommand(unittest.TestCase):
    """
        Represents the test class for the HBNBCommand class
    """
    
