from timeit import default_timer as time
import sys

already_found = {1}
found_map = {1: 3}
pows_of_2 = {1}


def collatz_step(n):
    if n % 2 == 0:
        return n//2
    else:
        return 3*n + 1


def kyle_collatz_step_3s(n):
    if n % 3 == 0:
        return n // 3
    elif n % 3 == 1:
        return n * 7 - 1  # definitely divisible by 3, since the extra 1 will become an extra 6
    else:
        return n * 5 - 1  # definitely divisible by 3, since the extra 2 will become an extra 9


def kyle_collatz_step_2s(n):
    # is dumb, 3 is cyclic: 3->6->3->...
    if n % 2 == 0:
        return n//2
    else:
        return 3*n - 2


def add_all(a_list):
    for elem in a_list:
        if elem not in already_found:
            already_found.add(elem)


def add_all_map(a_list):
    for elem in a_list:
        if elem[0] not in found_map:
            found_map[elem[0]] = elem[1]


def print_chain(start):
    while start != 1:
        if start in pows_of_2:
            print(start, "pow of 2!")
        else:
            print(start)
        start = kyle_collatz_step_2s(start)
    print(1, "\nDone, nothing miraculous this time :(")


def format_time(input_seconds):
    base = "%i hours, %i minutes, %i seconds, %f milliseconds"
    millis = input_seconds / .01 % 100
    seconds = int(input_seconds / 1) % 60
    minutes = int(input_seconds / 60) % 60**2
    hours = int(input_seconds / 60**2)
    return base % (hours, minutes, seconds, millis)


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
    sieve = [True] * (n // 2)
    for i in range(3, int(n ** 0.5) + 1, 2):
        if sieve[i // 2]:
            sieve[i * i // 2::i] = [False] * ((n - i * i - 1) // (2 * i) + 1)
    return [2] + [2 * i + 1 for i in range(1, n // 2) if sieve[i]]


def iterate_through(range_of_nums):
    """returns longest chain, does the thing to the globals and such"""
    longest_chain = (1, 3)
    for i in range_of_nums:
        count = 0
        if i not in already_found:
            curr = i
            steps = [curr]
            map_list = [(curr, count)]
            while curr not in already_found:
                curr = kyle_collatz_step_2s(curr)
                steps.append(curr)
                count += 1

            # supposed to add the mapped elems correctle
            step_counter = found_map[steps[-1]]
            for elem in steps[::-1]:
                found_map[elem] = step_counter
                step_counter += 1

            count += found_map[curr]

            if len(steps) > longest_chain[1]:
                longest_chain = (i, len(steps))

            add_all(steps)
            add_all_map(map_list)

        print("%i took %i steps" % (i, found_map[i]))

    return longest_chain


def main():
    L = 20
    for i in range(1, L):
        already_found.add(2**i)
        found_map[2**i] = i
        pows_of_2.add(2**i)

    if str.isdigit(sys.argv[-1]):
        L = int(sys.argv[-1])

    print("starting")
    start_time = time()
    longest_chain = (1, 3)
    if sys.argv[-2] == "-primes":
        longest_chain = iterate_through(prime_sieve(2**L))
    else:
        longest_chain = iterate_through(range(1, 2**L + 1))

    print("there are %i elements found converging to 1" % len(already_found))
    print(longest_chain)
    print_chain(longest_chain[0])

    end_time = time()
    print(format_time(end_time - start_time))


main()
