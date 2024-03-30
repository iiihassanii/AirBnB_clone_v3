#!/usr/bin/python3
"""Initialize Blueprint views"""
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views here to avoid circular imports
