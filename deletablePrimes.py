# inspired by July 27 Numberphile video:
# "It is conjectured that there are infinitely many deletable primes"

from Euler import prime_sieve

BOUND = 1000
primes = [''] + [str(p) for p in prime_sieve(BOUND)]


def all_sub_nums(num):
    to_ret = [num[:i-1] + num[i:] for i in range(1, len(num) + 1)]
    # print(num, to_ret)
    return to_ret


def recursive_step(nums):
    if nums == ['']:
        return True
    for n in nums:
        if n in primes and recursive_step(all_sub_nums(n)):
            # print("TRUE")
            return True
    # print("FALSE")
    return False


def is_deletable_prime(num):
    return recursive_step(all_sub_nums(num))


def main():

    count = 0
    for p in primes:
        if is_deletable_prime(p):
            print(p, 'yes')
            count += 1
        else:
            print(p, 'no')

    print(count, 'out of', len(primes))


# main()

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

digit_2_set = construction_step({'2', '3', '5', '7'})
# print(sorted(list(digit_2_set)))
# print(len(digit_2_set))
# print(19*4)

def reduce_to_del_primes(unknown_set):
    new_del_primes = []
    for elem in unknown_set:
        if elem in primes and is_deletable_prime(elem):
            new_del_primes.append(elem)
    return sorted(new_del_primes)

digit_2_del_primes = reduce_to_del_primes(digit_2_set)
print(digit_2_del_primes)
print(len(digit_2_del_primes))
digit_3_set = construction_step(digit_2_del_primes)
print(sorted(list(digit_3_set)))
print(len(digit_3_set))
digit_3_del_primes = reduce_to_del_primes(sorted(list(digit_3_set)))
print(digit_3_del_primes)
print(len(digit_3_del_primes))

print()
print(19*16, 304 - 270)

print(2 + 3 + 2 + 1 + 2 + 3 + 2 + 3 + 2 + 1 + 3 + 2 + 2 + 1 + 2 + 3)
