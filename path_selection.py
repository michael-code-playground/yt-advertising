import os
import sys
import datetime

def build_path():
    # Check if running as executable
    if getattr(sys, 'frozen', False):  
        current_path = os.path.dirname(sys.executable)
    else:
        current_path = os.path.dirname(__file__)
    
    timestamp_file = os.path.join(current_path, "timestamp.txt")
    
    return timestamp_file
      