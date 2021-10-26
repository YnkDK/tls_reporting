import sys
import os

if not os.path.dirname(os.path.dirname(os.path.realpath(__file__))) in sys.path:
    import warnings
    dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    sys.path.insert(0, dir_path)
    warnings.warn("Missing in sys.path: %s" % dir_path, RuntimeWarning)

from fastapi import FastAPI
from api.api_v1.api import api_v1_router
app = FastAPI()

app.include_router(api_v1_router)
