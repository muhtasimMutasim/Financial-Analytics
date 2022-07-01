
"""
    This is the main file that is being sent requests.
        
"""


import json
import os.path
from os import path
import sys
import os

from fastapi import FastAPI, APIRouter, Request
from datetime import datetime
import random


app = FastAPI()
# router = APIRouter()



###############################################################
# Testing endpoints
###############################################################

@app.get("/test")
def test():
    
    # Coment if you dont care if the API is up and running
    existence = "FAST API is up and running"
    
    # Uncomment to see if db exists in the db folder
    # existence = path.exists("../db/dbfile.json")
    
    return {"Test": existence }