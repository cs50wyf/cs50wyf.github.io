from math import sqrt

def find_closest(user_data, shows):
# Select all the shows in the database - only really care about show_id and the various ratings
# Cycle through each show and calculate the "distance" between the user's input and the show's data
# Store this "distance" in a dictionary with the keys being the show_id and the values being the distance
# Return the id of the show that is the closest to the user's data using max(distances, key=distances.get)
    distances = {}
    for show in shows:
        distances[show["id"]] = find_distance(user_data, show)
    return min(distances, key=distances.get)


def find_distance(user_data, show_data):
    sq_dist = 0
    for attribute in user_data:
        dist = user_data[attribute] - show_data[attribute]
        sq_dist += dist * dist
    return sqrt(sq_dist)