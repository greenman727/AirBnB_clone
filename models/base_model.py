#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """Defines the BaseModel."""

    def __init__(self, *args, **kwargs):
        """Initializes a new BaseModel."""
        tform = "%Y-%m-%dT%H:%M:%S.%f"
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
        """Update updated_at with the current datetime."""
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """Returns the dictionary of the BaseModel instance."""
        todict = self.__dict__.copy()
        todict["created_at"] = self.created_at.isoformat()
        todict["updated_at"] = self.updated_at.isoformat()
        todict["__class__"] = self.__class__.__name__
        return todict

    def __str__(self):
        """Return the string representation of the BaseModel instance."""
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
