from timeit import default_timer as time
import sys


def find_element_in_list(element, list_element):
    try:
        index_element = list_element.index(element)
        return index_element
    except ValueError:
        return None


already_found = {1}
init_gen_seq = {1}
found_map = {1: 0}
matching_lens = []
L = 5

USAGE_STR = "Run $ python3 Collatz.py [--primes/-p] [--help/-h] [--limit/-l  <new_lim>] or\n" \
            "     $ python3 Collatz.py -sv (single value) <number> to show the convergence"
ADDITIONAL_HELP_MSG = "Ran with defualt usage, if you'd like to run with additional options:"


def collatz_step(n):
    if n % 2 == 0:
        return n//2
    else:
        return 3*n + 1


def new1_step(n):
    # seems to cycle somewhere...

    if n % 3 == 0:
        return n // 3
    elif n % 3 == 1:
        return n * 5 + 1  # definitely divisible by 3, since the extra 1 will become an extra 6
    else:
        return n * 5 - 1  # definitely divisible by 3, since the extra 2 will become an extra 9


def new2_step(n):
    if n % 3 == 0:
        return n // 3
    elif n % 3 == 1:
        return (n * 2) + 1  # definitely divisible by 3, since the extra 1 will become an extra 3
    else:
        return (n * 5) - 1  # definitely divisible by 3, since the extra 2 will become an extra 9


def new3_step(n):
    if n % 2 == 0:
        return n // 2
    elif n % 3 == 0:
        return n // 3
    else:
        return n * 5 + 1  # definitely divisible by 2, since the extra 1 will become an extra 6


def bad_collatz_step(n):
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


def print_chain(start, step_func):
    count = 0
    while start != 1:
        if start in init_gen_seq:
            print(start, "from init generated sequence (powers of something)")
        else:
            print(start)
        start = step_func(start)
        count += 1

    print(1, "done!\n")
    return count


def fancy_print_chain_1(start, step_func):
    up_count = 0
    down_count = 0
    chain = [(start, False)]
    app = chain.append
    curr = start
    while curr != 1:
        nxt = step_func(curr)
        dir = nxt > curr
        if dir:
            up_count += 1
        else:
            down_count += 1
        app((nxt, dir))
        curr = nxt

    print(chain, up_count, down_count)

    space_count = up_count * 2 + 3
    print(' ' * space_count, start)
    for elem in chain[1:]:
        if elem[1]:
            space_count += 2
        else:
            space_count -= 2
        print(' ' * space_count, elem[0])

    return up_count + down_count


def fancy_print_chain_2(start, step_func):

    count = 0
    chain = [start]
    curr = start
    app = chain.append

    while curr != 1:
        nxt = step_func(curr)
        app(nxt)
        curr = nxt
        count += 1

    chain_sorted = sorted(chain)
    better_chain = []
    app = better_chain.append
    for elem in chain:
        app((elem, chain_sorted.index(elem)))

    last_spaces = -1
    for elem in better_chain:
        if last_spaces != -1:
            dif = elem[1] - last_spaces
            if dif > 0:
                print(' ' * last_spaces, '\\' * dif)
            else:
                print(' ' * elem[1], '/' * (-1 * dif))
        print(' ' * elem[1], elem[0])
        last_spaces = elem[1]

    return count


def format_time(input_seconds):
    base = "%i hours, %i minutes, %i seconds, %f milliseconds"
    millis = input_seconds / .01 % 100
    seconds = int(input_seconds / 1) % 60
    minutes = int(input_seconds / 60) % 60**2
    hours = int(input_seconds / 60**2)
    return base % (hours, minutes, seconds, millis)


def pows_of_2_minus_n(n, lim):
    return [i-n for i in [2**j for j in range(1, lim+1)] if (i-n > 0)]


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


def iterate_through(range_of_nums, step_func):
    """returns longest chain, does the thing to the globals and such"""
    last_len = -1
    longest_chain = (1, 0)
    for i in range_of_nums:
        count = 0
        if i not in already_found:  # this gonna make it hella slow
            curr = i
            steps = [curr]
            map_list = [(curr, count)]
            while curr not in already_found:
                curr = step_func(curr)
                steps.append(curr)
                count += 1

            # adds the elems mapped to how many steps it took
            step_counter = found_map[steps[-1]]
            for elem in steps[::-1]:
                found_map[elem] = step_counter
                step_counter += 1

            count += found_map[curr]

            if len(steps) > longest_chain[1]:
                longest_chain = (i, len(steps))

            if len(steps) == last_len:
                if (i-1, last_len) not in matching_lens:
                    matching_lens.append((i-1, last_len))

                matching_lens.append((i, last_len))

            last_len = len(steps)

            add_all(steps)
            add_all_map(map_list)

        print("%i took %i steps" % (i, found_map[i]))

    return longest_chain


def longest_chain_step_equiv_neighbors(fmap, upper_bound):
    # assumes found map is full and correct
    last_elem = -1
    last_steps = -1
    count = 0
    max_count = 0
    best = (0, 0)

    for key in fmap:
        print(key)
        if key > upper_bound:
            print("b1")
            return best
        if key != last_elem + 1:
            print("b2")
            continue
        if fmap[key] == last_steps:
            print("b3")
            count += 1
        elif count > max_count:
            print("b4")
            max_count = count
            count = 0
            best = (key-count, last_steps)

        print("default")

        last_elem = key
        last_steps = fmap[key]

    return best


def main(range_of_vals):
    step_func = collatz_step  # integration of other step types no come

    print("starting")
    start_time = time()
    longest_chain = (1, 0)
    longest_chain = iterate_through(range_of_vals, step_func)

    print(longest_chain)
    print_chain(longest_chain[0], step_func)
    print("there are %i elements found converging to 1" % len(already_found))

    # print(longest_chain_step_equiv_neighbors(found_map, 2**L))

    end_time = time()
    print(format_time(end_time - start_time))


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 1:
        # this is the default behavior, just print collatz numbers with their num steps up to the default L = 5
        main(range(1, 2**L))
        print("\n", ADDITIONAL_HELP_MSG, "\n", USAGE_STR)
        exit(0)

    if "-ij" in args:
        index = find_element_in_list("-ij", args)
        if index is not None and args[index+1].isdigit() and args[index+2].isdigit():
            val = (2**int(args[index+1]) - int(args[index+2]))
            print("total steps =", fancy_print_chain_2(val, collatz_step))
        else:
            print(USAGE_STR)
        exit(0)

    if "-sv" in args:
        index = find_element_in_list("-sv", args)
        if index is not None and args[index+1].isdigit():
            print("total steps =", fancy_print_chain_2(int(args[index+1]), collatz_step))
        else:
            print(USAGE_STR)
        exit(0)

    if "-h" in args or "--help" in args:
        print(USAGE_STR)
        exit(0)

    l_loc = find_element_in_list("-l", args)
    limit_loc = find_element_in_list("--limit", args)
    if l_loc is not None or limit_loc is not None:
        index = l_loc if (l_loc is not None) else limit_loc
        if args[index+1].isdigit():
            L = int(args[index+1])

    if "-p" in args or "--primes" in args:
        # we only want to look at the primes, since their convergence is a little more wonky
        main(prime_sieve(2 ** L))
        exit(0)

    if "-faust" in args:
        twos = pows_of_2_minus_n(2, L)
        threes = pows_of_2_minus_n(3, L)
        fours = pows_of_2_minus_n(4, L)
        fives = pows_of_2_minus_n(5, L)
        collected = list(set().union(twos, threes, fours, fives))
        main(sorted(collected))
        exit(0)

    if len(args) == 3:
        main(range(1, 2 ** L))
        exit(0)
    else:
        print(USAGE_STR)
        exit(0)

