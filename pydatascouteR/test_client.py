# Create test file: test_client.py
from pydatascouteR.client import get_goalkeepers, get_forwards

gk = get_goalkeepers()
print("Goalkeepers:")
print(gk)

fw = get_forwards()
print("\nForwards:")
print(fw)