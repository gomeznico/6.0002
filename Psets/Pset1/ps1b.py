###########################
# 6.0002 Problem Set 1b: Space Change
# Name:
# Collaborators:
# Time:
# Author: charz, cdenise

#================================
# Part B: Golden Eggs
#================================

# Problem 1
def dp_make_weight(egg_weights, target_weight, memo = {}):
    """
    Find number of eggs to bring back, using the smallest number of eggs. Assumes there is
    an infinite supply of eggs of each weight, and there is always a egg of value 1.

    Parameters:
    egg_weights - tuple of integers, available egg weights sorted from smallest to largest value (1 = d1 < d2 < ... < dk)
    target_weight - int, amount of weight we want to find eggs to fit
    memo - dictionary, OPTIONAL parameter for memoization (you may not need to use this parameter depending on your implementation)

    Returns: int, smallest number of eggs needed to make target weight
    """

    # ##Greedy Method:
    # num_eggs = 0
    # sorted_egg_weights = sorted(egg_weights,reverse=True)
    # remaining_weight = target_weight
    # for i in range(len(sorted_egg_weights)):
    #     egg_weight = sorted_egg_weights[i]
    #     num_added = int(remaining_weight/egg_weight)
    #     remaining_weight -= num_added*egg_weight
    #     num_eggs += num_added
    # return num_eggs


    # if node has already been explored, return saved result
    if target_weight in memo:
        num_eggs = memo[target_weight]
    # if target weight matches one of the eggs, minimum num = 1 by inspection
    elif target_weight in egg_weights:
        memo[target_weight] = 1
        num_eggs = 1
    elif egg_weights == () or target_weight == 0:
        num_eggs = 0

    elif egg_weights[-1] > target_weight:
        #Explore right branch only, don't take egg
        #memo inserted as is, no adjustments
        num_eggs = dp_make_weight(egg_weights[:-1], target_weight, memo)
    else:
        egg=egg_weights[-1]
        #Explore left branch, taking egg
        num_eggsWith = 1 + dp_make_weight(egg_weights, target_weight-egg, memo)

        #Explore right branch not taking egg
        num_eggsWithOut = dp_make_weight(egg_weights[:-1], target_weight, memo)

        #Choose better branch
        if num_eggsWithOut == 0:
            memo[target_weight] = num_eggsWith
            num_eggs = num_eggsWith
        elif num_eggsWith < num_eggsWithOut:
            num_eggs = num_eggsWith
        else:
            num_eggs = num_eggsWithOut

        memo[target_weight] = num_eggs
    return num_eggs

# EXAMPLE TESTING CODE, feel free to add more if you'd like
if __name__ == '__main__':
    egg_weights = (1, 5, 10, 25)
    n = 99
    print(f"Egg weights = {egg_weights}")
    print(f"n = {n}")
    print("Expected ouput: 9 (3 * 25 + 2 * 10 + 4 * 1 = 99)")
    print("Actual output:", dp_make_weight(egg_weights, n))
    print()
