###########################
# 6.0002 Problem Set 1a: Space Cows
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time

#================================
# Part A: Transporting Space Cows
#================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    file = open(filename, 'r')
    cows = {}
    for line in file:
        arr = line.rstrip().split(',')
        cows[arr[0]] = int(arr[1])
    return cows

# Problem 2
def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    cows_left = cows.copy()
    all_trips = []

    heaviest_cow = 'none'
    heaviest_weight = 0


    ## this could be made more efficient by create a copied/sorted list of
    # the cows by weight, rather than searching through each time

    while len(cows_left) > 0:
        cargo_space_left = limit
        passengers =[]

        # add passengers until no cargo space left
        while cargo_space_left > 0:
            for cow in cows_left:
                weight = cows_left[cow]
                # compare and update heaviest cow
                if  heaviest_weight < weight <= cargo_space_left:
                    heaviest_cow = cow
                    heaviest_weight = cows_left[heaviest_cow]
            # when none cow remains heaviest, no space left
            if heaviest_cow == 'none':
                break
            # update passengers, and reset to look for next heaviest cow
            passengers.append(heaviest_cow)
            cargo_space_left -= heaviest_weight
            cows_left.pop(heaviest_cow)
            heaviest_cow = 'none'
            heaviest_weight = 0

        all_trips.append(passengers)
    return all_trips

# Problem 3
def brute_force_cow_transport(cows,limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    cow_list = list(cows.keys())

    all_possible_trips = []

    for trips in get_partitions(cow_list):
        is_permutation_valid = True
        # check weight of each trip
        for trip in trips:
            trip_weight = 0
            for cow in trip:
                trip_weight += cows[cow]
            if trip_weight > limit:
                is_permutation_valid = False
                # stop checking other trips in permutation
                break

        # return first valid permutation
        # permutations have more trips as for loop goes on
        if is_permutation_valid:
            all_possible_trips.append(trips)

    min_trips = len(cow_list)
    best_trips = []
    for trips in all_possible_trips:
        if len(trips) < min_trips:
            min_trips = len(trips)
            best_trips = trips
    return best_trips






# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """

    cows1 = load_cows('ps1_cow_data.txt')

    # test greedy algo
    start = time.time()
    trips = greedy_cow_transport(cows1,10)
    end = time.time()
    time1 = (end - start)*1000
    num_trips = len(trips)
    print(f"Greedy Algorithm took {time1} to find a solution with {num_trips} trips" )


    start = time.time()
    trips = brute_force_cow_transport(cows1,10)
    end = time.time()
    time2 = (end - start)*1000
    num_trips = len(trips)
    print(f"Brute Force Algorithm took {time2} to find a solution with {num_trips} trips" )



cows1 = load_cows('ps1_cow_data.txt')
# cows2 = load_cows('ps1_cow_data_2.txt')
# cows3 = load_cows('ps1_cow_data_3.txt')


compare_cow_transport_algorithms()

'''
Problem A.5 Writeup
1.  What were your results from compare_cow_transport_algorithms?
    Which algorithm runs faster? Why?

    Greedy Algorithm took      000.01573562622070 msec to find a solution with 6 trips
    Brute Force Algorithm took 280.26695442199707 msec to find a solution with 5 trips

    The Greedy Algorithm was faster, by ~20,000 times.  It builds a solution form the bottom up.  at worst, the time is O(n^2), where n is the number of cows.  it checks every cow for each possible trip.  At worst, the heaviest cow is the last one checked and completly fills up the cargo.  having to check each cow again for the remaining space.  Doing this check n times, such that there are n trips, 1 for each cow.

    The brute force is recursive, and is O(2^n) which as an exponential, greatly increase the number of operations, time, and memory required.

2.  Does the greedy algorithm return the optimal solution? Why/why not?

    No.  it does not maximize cows per trip, just the weight.  this allows for 'wasted' cargo space, such as below:  Herman, Maggie is an ideal trip, no wasted space.  but Oreo would be better paired with 2 cows that weigh 2 each, instead of the cow that weighs 3.  trip 4 has a wasted cargo space of 1, which requires Florence to be taken alone now.
    ['Betsy']
    ['Henrietta']
    ['Herman', 'Maggie']
    ['Oreo', 'Moo Moo']
    ['Millie', 'Milkshake', 'Lola']
    ['Florence']

    more optimal would be:
    ['Betsy'],
    ['Henrietta'],
    ['Herman', 'Maggie']
    ['Moo Moo', 'Millie', 'Lola'],
    ['Milkshake', 'Florence', 'Oreo'],



3.  Does the brute force algorithm return the optimal solution? Why/why not?

    Yes, or at least a version the optimal solution, as it has checked every valid (regarding cargo space) permutation of trips.  Then finds the most optimal one.

'''



