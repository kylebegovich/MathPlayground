from itertools import product

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

print_expectancies(3)
print('\n')
print_expectancies(4)

# print()
# for line in function(3): # TODO check for 3,3 hand
    # print(line)
# print()
# for line in function(4):
#     print(line)
