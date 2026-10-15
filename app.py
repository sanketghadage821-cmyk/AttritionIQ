import os
import sys

# Append the project root directory to sys.path so Streamlit Cloud can resolve local imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import streamlit as st
from src.connect_snowflake import get_snowflake_connection