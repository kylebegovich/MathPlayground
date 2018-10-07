from itertools import product, combinations
import numpy as np


def solve(expectancies, cutoffs):
    # print(expectancies, cutoffs)
    a = np.array(expectancies)
    # print('a = ', a)
    b = np.array(cutoffs)
    # print('b = ', b)
    try:
        x = np.linalg.solve(a, b)
    except:
        return None
    # print('x = ', x)
    return x


# print(solve([(3, 1), (1, 2)], [100, 100]))
# print()

def function(n):
    one_to_n = list([i for i in range(1, n + 1)])
    zero_to_n = list([i for i in range(n + 1)])
    table = [[0 for j in range(((n+1)**2) + 1)] for i in range((n ** 2) + 2)]
    # print(len(range((2 ** (n+1)) + 2)))
    # setting the first row as all the strategies
    strategies = list(product(zero_to_n, repeat=2))
    # print(len(strategies), strategies)
    # print(len(table[0]))
    for col in range(1, ((n+1)**2) + 1):
        table[0][col] = strategies[col-1]

    counter = 1
    hands = list(product(one_to_n, repeat=2))
    # print(len(hands), hands
    for row in range(1, (n ** 2) + 1):
        # setting the first column as all the hand combos
        table[row][0] = hands[row-1]
        for col in range(1, ((n+1)**2) + 1):
            hand_outcome = (0, 0)

            # both fold (cutoff value exclusive)
            if table[0][col][0] >= table[row][0][0] and table[0][col][1] >= table[row][0][1]:
                if table[row][0][0] > table[row][0][1]:
                    hand_outcome = (1, 0)
                elif table[row][0][0] == table[row][0][1]:
                    hand_outcome = (0, 0)
                elif table[row][0][0] < table[row][0][1]:
                    hand_outcome = (-1, 0)
                else:
                    print("something wrong")

            # both bet
            elif table[0][col][0] < table[row][0][0] and table[0][col][1] < table[row][0][1]:
                if table[row][0][0] > table[row][0][1]:
                    hand_outcome = (0, 1)
                elif table[row][0][0] == table[row][0][1]:
                    hand_outcome = (0, 0)
                elif table[row][0][0] < table[row][0][1]:
                    hand_outcome = (0, -1)
                else:
                    print("something wrong")

            # P1 bets, P2 folds
            elif table[0][col][0] < table[row][0][0] and table[0][col][1] >= table[row][0][1]:
                hand_outcome = (1, 0)

            # P1 folds, P2 bets
            elif table[0][col][0] >= table[row][0][0] and table[0][col][1] < table[row][0][1]:
                hand_outcome = (-1, 0)

            # else:
            #     print("something wrong")

            table[row][col] = hand_outcome

    # summing each column
    for col in range(1, ((n+1)**2) + 1):
        a_sum = 0
        b_sum = 0
        for row in range(1, (n ** 2) + 1):
            a_sum += table[row][col][0]
            b_sum += table[row][col][1]
            # print(col, row, a_sum, b_sum)

        # table[(2**n)+1][i] = str(str(a_sum) + "*a + " + str(b_sum) + "b")
        table[-1][col] = (a_sum, b_sum)

    return table


def print_expectancies(n):
    output = function(n)
    for col in range(1, ((n+1)**2) + 1):
        tupe = output[-1][col]
        strat = output[0][col]
        # print(tupe, strat)
        print(strat, "expects", tupe[0], "a + ", tupe[1], "b")

def print_opposite_expectancies(n):
    output = function(n)
    for col in range(1, ((n+1)**2) + 1):
        tupe = output[-1][col]
        strat = output[0][col]
        # print(tupe, strat)
        print(strat, "expects", -1*tupe[0], "a + ", -1*tupe[1], "b")

print_opposite_expectancies(3)


def best_response(n):
    table = function(n)
    for line in table:
        print(line)
    print()
    for i in range(1, (n+1)**2 + 1, n+1):
        print('\n', table[0][i][0])
        for pair in combinations(range(n+1), 2):
            # print(i, pair, ' ', pair[0]+i, pair[1]+i)
            print(table[0][i+pair[0]], table[0][i+pair[1]])
            # print([table[-1][pair[0]+i], table[-1][pair[1]+i]])
            sol = solve([table[-1][pair[0]+i], table[-1][pair[1]+i]], [1, 1])
            if sol is not None:
                print(sol, table[-1][pair[0]+i], table[-1][pair[1]+i])
            else:
                print("no solution", table[-1][pair[0]+i], table[-1][pair[1]+i])


best_response(3)

# print()
# for line in function(3):
    # print(line)
# print()
# output = function(3)
# [print(output[i][10]) for i in range(((3+1)**2) + 1)]
