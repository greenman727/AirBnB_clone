#!/usr/bin/python3
"""Defines a class BaseModel"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """A class to define BaseModel"""

    def __init__(self, *args, **kwargs):
        """Initializes a neew BaseModel."""
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, tform)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """updates the instance attribute updated_at with the current time"""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        todict = self.__dict__.copy()
        todict["created_at"] = self.created_at.isformat()
        todict["updated_at"] = self.updated_at.isformat()
        todict["__class__"] = self.__class__.name__
        return todict

    def __str__(self):
        """prints class instance of BaseModel"""
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
