#!/usr/bin/python3
"""Defines a class Rreview."""
from models.base_model import BaseModel


class Review(BaseModel):
    """Defines a review."""

    place_id = ""
    user_id = ""
    text = ""
