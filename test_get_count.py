#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

# Get the count of all objects and State objects
all_objects_count = storage.count()
state_objects_count = storage.count(State)

print("All objects: {}".format(all_objects_count))
print("State objects: {}".format(state_objects_count))

# Try to access the first state object if State objects are present
if state_objects_count > 0:
    try:
        first_state_id = list(storage.all(State).values())[0].id
        first_state = storage.get(State, first_state_id)
        print("First state: {}".format(first_state))
    except IndexError:
        print("Error: Unable to retrieve the first state object.")
else:
    print("No state objects found in the database.")
