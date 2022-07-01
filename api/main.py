
"""
This is the entry point for the Purple Cow REST api.
How to run FastAPI file:
    uvicorn main:app --host {insert ip address} --port {desired port number} --reload
    
    uvicorn main:app --host 0.0.0.0 --port 3000 --reload
    
"""

from app.main import app

app = app