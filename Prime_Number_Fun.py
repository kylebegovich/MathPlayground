import sys

# --- generate prime numbers----------------------------------------------------------------------
def prime_sieve(n):
    """
    Return a list of prime numbers from 2 to a prime < n. Very fast (n<10,000,000) in 0.4 sec.

    Example:
    >>>prime_sieve(25)
    [2, 3, 5, 7, 11, 13, 17, 19, 23]

    Algorithm & Python source: Robert William Hanks
    http://stackoverflow.com/questions/17773352/python-sieve-prime-numbers
    """
    if n <= 1:
        return []

    sieve = [True] * (n // 2)
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [2 * i + 1 for i in range(1, n // 2) if sieve[i]]


def mersenne_prime_sieve(n):
    """
    return a list of mersenne primes up to 2^n - 1
    """
    if n <= 1:
        return []

    sieve = [(2**i) - 1 for i in range(n)]
    for i in range(3, int(n ** 0.5) + 1, 2):
        for j in range(len(sieve)):
            elem = sieve[j]
            if (elem / i).is_integer():
                sieve[j] = -1

    return [sieve[i] for i in range(len(sieve)) if sieve[i] != -1]


def find_twins_from_primes(primes):
    out_list = []
    app = out_list.append
    for i in range(len(primes) - 1):
        if primes[i] + 2 == primes[i+1]:
            app((primes[i], primes[i+1]))

    return out_list


def find_cousins_from_primes(primes):
    out_list = []
    app = out_list.append

    if 3 in primes and 7 in primes:
        app((3, 7))  # since 5 is between them, they aren't one off from another, and we need this condition

    for i in range(len(primes) - 1):
        if primes[i] + 4 == primes[i+1]:
            app((primes[i], primes[i+1]))

    return out_list


def find_sexys_from_primes(primes):
    out_list = []
    app = out_list.append
    for i in range(len(primes) - 2):
        if primes[i] + 6 == primes[i+1]:
            app((primes[i], primes[i+1]))
        elif primes[i] + 6 == primes[i+2]:
            app((primes[i], primes[i+2]))

    return out_list


def palindromic_primes(primes):
    return [p for p in primes if (p == int(str(p)[::-1]))]


N = 12


def test():
    if any(s.isDigit() for s in sys.argv):
        n = 
    else:
        n = N

    primes = prime_sieve(2**n)
    print("\nMersennes:\n", mersenne_prime_sieve(n))

    print(primes)
    print("\nTwins:\n", find_twins_from_primes(primes))
    print("\nCousins:\n", find_cousins_from_primes(primes))
    print("\nSexys:\n", find_sexys_from_primes(primes))
    print("\nPalindromics:\n", palindromic_primes(primes))


test()
