

class Food(object):
    def __init__(self, n, v, w):
        self.name = n
        self.value = v
        self.calories = w
    def getValue(self):
        return self.value
    def getCost(self):
        return self.calories
    def density(self):
        return self.getValue()/self.getCost()
    def __str__(self):
        return self.name + ': <' + str(self.value)\
                 + ', ' + str(self.calories) + '>'

def buildMenu(names, values, calories):
    """return menu list of Food aobjects given 3 lists"""
    menu = []
    for i in range(len(values)):
        menu.append(Food(names[i], values[i],
                          calories[i]))
    return menu

def greedy(items, maxCost, keyFunction):
    """Assumes items a list, maxCost >= 0,
         keyFunction maps elements of Items to numbers"""
    ## sorted list in descending order of function value
    itemsCopy = sorted(items, key = keyFunction,
                       reverse = True)
    result = []
    ## uses tuple unpacking to initialize totalValue and totalCost
    ## the variables are not tuples, they are ints.  the tuple is forgotten after this line
    ## cleaner way to write variables
    totalValue, totalCost = 0.0, 0.0

    # go through items from largest to smallest and add if theres space
    for i in range(len(itemsCopy)):
        if (totalCost+itemsCopy[i].getCost()) <= maxCost:
            result.append(itemsCopy[i])
            totalCost += itemsCopy[i].getCost()
            totalValue += itemsCopy[i].getValue()
    return (result, totalValue)

def testGreedy(items, constraint, keyFunction):
    taken, val = greedy(items, constraint, keyFunction)
    print('Total value of items taken =', val)
    for item in taken:
        print('   ', item)

def testGreedys(foods, maxUnits):
    print('Use greedy by value to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits, Food.getValue)
    print('\nUse greedy by cost to allocate', maxUnits,
          'calories')

    ## lambda is quick function creator
    ## lambda x : x+10 -> s
    testGreedy(foods, maxUnits,
               lambda x: 1/Food.getCost(x))
    print('\nUse greedy by density to allocate', maxUnits,
          'calories')
    testGreedy(foods, maxUnits, Food.density)

def maxVal(toConsider, available_space):
    """Assumes toConsider a list of items, available_space a weight
       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and a tuple of the items of that solution"""

    ## an empty list of items, return empty result
    if toConsider == [] or available_space == 0:
        # result = (value, tuple_of_chosen_items)
        result = (0, ())

    elif toConsider[0].getCost() > available_space:
        #Explore right branch only via recursion
        #Do not take this item, since there is not enough space
        result = maxVal(toConsider[1:], available_space)

    else:
        nextItem = toConsider[0]
        #Explore left branch via recursion
        withVal, withToTake = maxVal(toConsider[1:],
                                     available_space - nextItem.getCost())

        # take result of recursion and add nextItem value
        withVal += nextItem.getValue()

        #Explore right branch via recursion
        #item NOT chosen
        withoutVal, withoutToTake = maxVal(toConsider[1:], available_space)

        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    return result

def testMaxVal(foods, maxUnits, printItems = True):
    print('Use search tree to allocate', maxUnits,
          'calories')
    val, taken = maxVal(foods, maxUnits)
    print('Total value of items taken =', val)
    if printItems:
        for item in taken:
            print('   ', item)

names = ['wine', 'beer', 'pizza', 'burger', 'fries',
         'cola', 'apple', 'donut', 'cake']
values = [89,90,95,100,90,79,50,10]
calories = [123,154,258,354,365,150,95,195]
foods = buildMenu(names, values, calories)

# testGreedys(foods, 750)
# print('')
# testMaxVal(foods, 750)

import random

def buildLargeMenu(numItems, maxVal, maxCost):
    items = []
    for i in range(numItems):
        items.append(Food(str(i),
                          random.randint(1, maxVal),
                          random.randint(1, maxCost)))
    return items

# for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45):
#    print('Try a menu with', numItems, 'items')
#    items = buildLargeMenu(numItems, 90, 250)
#    testMaxVal(items, 750, False)

# def fib(n):
#     if n == 0 or n == 1:
#         return 1
#     else:
#         return fib(n - 1) + fib(n - 2)

# # for i in range(121):
# #    print('fib(' + str(i) + ') =', fib(i))


# def fastFib(n, memo = {}):
#     """Assumes n is an int >= 0, memo used only by recursive calls
#        Returns Fibonacci of n"""
#     if n == 0 or n == 1:
#         return 1
#     try:
#         return memo[n]
#     except KeyError:
#         result = fastFib(n-1, memo) + fastFib(n-2, memo)
#         memo[n] = result
#         return result

# for i in range(121):
#    print('fib(' + str(i) + ') =', fastFib(i))

def fastMaxVal(toConsider, avaliable, memory = {}):
    """Assumes toConsider is a list of subjects,
        avaliable a int of space/budget left
        memory supplied by recursive calls

        memory uses tuples of:
        (number of subjects , available space/budget left)  as the key.
        the memory is built up with that tuple is how nodes are saved



       Returns a tuple of the total value of a solution to the
         0/1 knapsack problem and the subjects of that solution"""

    # if node has already been explored, return
    if (len(toConsider), avaliable) in memory:
        result = memory[(len(toConsider), avaliable)]
    # if no items, or no avaliable space, return 0 tuple
    elif toConsider == [] or avaliable == 0:
        result = (0, ())

    elif toConsider[0].getCost() > avaliable:
        #Explore right branch only, (don't take toConsider[0])
        # memory inserted as is, no adjustments
        result = fastMaxVal(toConsider[1:], avaliable, memory)
    else:
        nextItem = toConsider[0]
        #Explore left branch, taking nextItem
        withVal, withToTake =\
                 fastMaxVal(toConsider[1:],
                            avaliable - nextItem.getCost(), memory)
        withVal += nextItem.getValue()
        #Explore right branch
        withoutVal, withoutToTake = fastMaxVal(toConsider[1:],
                                                avaliable, memory)
        #Choose better branch
        if withVal > withoutVal:
            result = (withVal, withToTake + (nextItem,))
        else:
            result = (withoutVal, withoutToTake)
    # add result to memory,
        # key: (num of items, avaliable Space)
        # value: (total value, (tuple of items taken))
    memory[(len(toConsider), avaliable)] = result
    return result

def testMaxVal(foods, maxUnits, algorithm, printItems = True):
    print('Menu contains', len(foods), 'items')
    print('Use search tree to allocate', maxUnits,
          'calories')
    val, taken = algorithm(foods, maxUnits)
    if printItems:
        print('Total value of items taken =', val)
        for item in taken:
            print('   ', item)

for numItems in (5, 10, 15, 20, 25, 30, 35, 40, 45, 50):
   items = buildLargeMenu(numItems, 90, 250)
   testMaxVal(items, 750, fastMaxVal, True)
