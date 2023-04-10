import sys
import os

# Add the path to the 'utils' directory to sys.path
utils_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', 'talkwave', 'utils'))
if not os.path.isdir(utils_path):
    raise ValueError(f"Cannot find 'utils' directory at {utils_path}")
sys.path.insert(0, utils_path)
