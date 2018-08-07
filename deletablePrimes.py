# inspired by July 27 Numberphile video:
# "It is conjectured that there are infinitely many deletable primes"

from Euler import prime_sieve
import time


DIGITS = 5
primes = [''] + [str(p) for p in prime_sieve(10**DIGITS)]
deletable_primes = {'2', '3', '5', '7'}
add_del = deletable_primes.add

del_prime_tree = {}


def all_sub_nums(num):
    to_ret = [num[:i-1] + num[i:] for i in range(1, len(num) + 1)]
    # print(num, to_ret)
    return to_ret


def is_deletable_prime(parent):
    nums = all_sub_nums(parent)
    if nums == ['']:
        return True
    for n in nums:
        if n in deletable_primes or n in primes and is_deletable_prime(n):
            add_del(parent)
            return True
    # print("FALSE")
    return False


def find_children(del_primes, parent):
    children = []
    for dp in del_primes:
        if parent == dp or len(parent) + 1 != len(dp):
            continue
        if parent in dp:
            children.append(dp)
            continue
        for i in range(len(parent)):
            if dp.find(parent[:i]) == dp.find(parent[i:]) != -1:
                children.append(dp)
                break  # ahhhh idk what to do here

    return children


def main():
    count = 0
    for p in primes:
        is_deletable_prime(p)

    print(len(deletable_primes), 'primes are deletable out of', len(primes), 'total primes')
    del_primes = list(map(str, sorted(map(int, list(deletable_primes)))))
    # print(del_primes)

    for p in del_primes:
        if len(p) == DIGITS:
            break
        del_prime_tree[p] = find_children(del_primes, p)
        # if len(children) == 0:
        #     print(p)

    print(del_prime_tree)
    values = ['2']
    while len(values) != 0:
        next = values.pop()
        print(next)
        if next in del_prime_tree:
            for child in del_prime_tree[next]:
                values.append(child)

    print('Done')


start = time.time()
main()
print(time.time() - start)
# With mem: (100000) 6.549623966217041 6.5425872802734375 6.433934688568115
# Without mem: (100000) 7.424246788024902 7.415876150131226

digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
def construction_step(n_minus_1_digit_set):
    new_set = set()
    add = new_set.add
    for elem in n_minus_1_digit_set:
        for digit in digits:
            add(digit + elem)
            add(elem + digit)
        add(elem + '0')
    return new_set


# print(sorted(list(digit_2_set)))
# print(len(digit_2_set))
# print(19*4)

def reduce_to_del_primes(unknown_set):
    new_del_primes = []
    for elem in unknown_set:
        if elem in primes and is_deletable_prime(elem):
            new_del_primes.append(elem)
    return sorted(new_del_primes)


# digit_2_set = construction_step({'2', '3', '5', '7'})
# digit_2_del_primes = reduce_to_del_primes(digit_2_set)
# print(digit_2_del_primes)
# print(len(digit_2_del_primes))
# digit_3_set = construction_step(digit_2_del_primes)
# print(sorted(list(digit_3_set)))
# print(len(digit_3_set))
# digit_3_del_primes = reduce_to_del_primes(sorted(list(digit_3_set)))
# print(digit_3_del_primes)
# print(len(digit_3_del_primes))
#
# print()
# print(19*16, 304 - 270)
#
# print(2 + 3 + 2 + 1 + 2 + 3 + 2 + 3 + 2 + 1 + 3 + 2 + 2 + 1 + 2 + 3)
