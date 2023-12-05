#!/usr/bin/python3
"""Defines models directory"""
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
