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


# TODO figure out how the above version works and make this one work
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
    twins = []
    app = twins.append
    for i in range(len(primes) - 1):
        if primes[i] +2 == primes[i+1]:
            app((primes[i], primes[i+1]))

    return twins


def test(n):
    primes = prime_sieve(2**n)
    print(primes)
    print("\nbreak\n")
    # print(mersenne_prime_sieve(n))

    print(find_twins_from_primes(primes))


test(25)
