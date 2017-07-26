from timeit import default_timer as time

L = 20

already_found = {1}
pows_of_2 = {1}


def collatz_step(n):
    if n % 2 == 0:
        return n//2
    else:
        return (3*n + 1) // 2


def add_all(a_list):
    for elem in a_list:
        if elem not in already_found:
            already_found.add(elem)


def print_chain(start):
    while start != 1:
        if start in pows_of_2:
            print(start, "pow of 2!")
        else:
            print(start)
        start = collatz_step(start)
    print(1, "\nDone, nothing miraculous this time :(")


def format_time(input_seconds):
    base = "%i hours, %i minutes, %i seconds, %f milliseconds"
    millis = input_seconds / .01 % 100
    seconds = int(input_seconds / 1) % 60
    minutes = int(input_seconds / 60) % 60**2
    hours = int(input_seconds / 60**2)
    return base % (hours, minutes, seconds, millis)


if __name__ == '__main__':

    for i in range(1, L):
        already_found.add(2**i)
        pows_of_2.add(2**i)

    start_time = time()
    longest_chain = (1, 3)
    for i in range(1, 2**L + 1):
        if i not in already_found:
            count = 0
            curr = i
            steps = [curr]
            while curr not in already_found:
                curr = collatz_step(curr)
                steps.append(curr)
                count += 1

            if len(steps) > longest_chain[1]:
                longest_chain = (i, len(steps))

            print("%i took %i steps" % (curr, count))
            add_all(steps)

    print("there are %i elements found converging to 1" % len(already_found))
    print(longest_chain)
    print_chain(longest_chain[0])

    end_time = time()
    print(format_time(end_time - start_time))
