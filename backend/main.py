from __future__ import annotations
import os
import logging
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Union


from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from werkzeug.exceptions import HTTPException

from .auth import verify_id_token