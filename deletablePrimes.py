# inspired by July 27 Numberphile video:
# "It is conjectured that there are infinitely many deletable primes"

from Euler import prime_sieve

BOUND = 100
primes = [''] + [str(p) for p in prime_sieve(BOUND)]


def allSubNums(num):
    to_ret = [num[:i-1] + num[i:] for i in range(1, len(num) + 1)]
    # print(num, to_ret)
    return to_ret


def recursiveStep(nums):
    if nums == ['']:
        return True
    for n in nums:
        if n in primes and recursiveStep(allSubNums(n)):
            # print("TRUE")
            return True
    # print("FALSE")
    return False


def isDeletablePrime(num):
    return recursiveStep(allSubNums(num))


def main():

    count = 0
    for p in primes:
        if isDeletablePrime(p):
            print(p, 'yes')
            count += 1
        else:
            print(p, 'no')

    print(count, 'out of', len(primes))


main()
