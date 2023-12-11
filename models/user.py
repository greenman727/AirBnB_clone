#!/usr/bin/python3
"""Defines a class User."""
from models.base_model import BaseModel


class User(BaseModel):
    """User class for the user"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""
