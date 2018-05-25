from itertools import groupby


def minimize(variables, minterms):
    group = [[] for _ in range(len(variables) + 1)]
    m_dec = [minterms[i] for i in range(len(minterms))]
    for i in range(len(minterms)):
        minterms[i] = bin(minterms[i])[2:]  # cutting 0b
        if len(minterms[i]) < len(variables):
            for j in range(len(variables) - len(minterms[i])):
                minterms[i] = '0' + minterms[i]
        elif len(minterms[i]) > len(variables):
            print("Error: more minterms  than variables\n")
            return
        index = minterms[i].count('1')
        group[index].append(minterms[i])

    print("\tMinterms in groups:")
    for m in group:
        print(m)

    imps = []
    while not is_empty(group):
        temp = combine(group, imps)
        group = remove_duplicats(temp)

    print("\tIpmlicants:")
    for imp in imps:
        print(imp)

    chart = [[0 for _ in range(len(minterms))] for _ in range(len(imps))]
    for i in range(len(minterms)):
        for j in range(len(imps)):
            if is_in_imps(minterms[i], imps[j]):
                chart[j][i] = 1

    print("\tChart:")
    print(' '.join('-' for _ in imps[0]), ":\t", m_dec)
    for i in range(len(imps)):
        print(imps[i], ":\t\t", chart[i])

    solution = find_optimal(chart, imps)
    solution = remove_duplicats(solution)

    print_answer(variables, solution, imps)


def is_empty(group):
    return len(group) == 0


def combine(group, imps):
    checked = []
    new_group = [[] for _ in range(len(group) - 1)]

    for i in range(len(group) - 1):
        for el1 in group[i]:
            for el2 in group[i + 1]:
                was_match, pos = compare_binary(el1, el2)
                if was_match:
                    checked.append(el1)
                    checked.append(el2)
                    new_el = list(el1)
                    new_el[pos] = '-'
                    new_el = ''.join(new_el)
                    new_group[i].append(new_el)

    for subg in group:
        for el in subg:
            if el not in checked:
                imps.append(el)
    return new_group


def remove_duplicats(group):
    new_g = []
    for sub in group:
        new_sub = []
        for el in sub:
            if el not in new_sub:
                new_sub.append(el)
        new_g.append(new_sub)
    return new_g


def compare_binary(el1, el2):
    diff = 0
    pos = 0
    for i in range(len(el1)):
        if el1[i] != el2[i]:
            diff += 1
            pos = i
    return diff == 1, pos


def is_in_imps(m, imp):
    for i in range(len(imp)):
        if imp[i] != "-" and imp[i] != m[i]:
            return False
    return True


def find_optimal(chart, imps):
    final_imps = []
    essentials = find_essentials(chart)
    essentials = remove_duplicats_list(essentials)
    for i in range(len(essentials)):
        for column in range(len(chart[0])):
            if chart[essentials[i]][column] == 1:
                for row in range(len(chart)):
                    chart[row][column] = 0

    if all_zeros(chart):
        return [essentials]
    else:
        optimals = petrick_method(chart)
        cost = []
        for sum in optimals:
            val = 0
            for i in range(len(imps)):
                for el in sum:
                    if i == el:
                        val = val + real_cost(imps[i])
            cost.append(val)
        for i in range(len(cost)):
            if cost[i] == min(cost):
                final_imps.append(optimals[i])
        for imp in final_imps:
            for es in essentials:
                if es not in imp:
                    imp.append(es)
    return final_imps


def find_essentials(chart):
    essentials = []
    for i in range(len(chart[0])):
        xs = 0
        pos = 0
        for j in range(len(chart)):
            if chart[j][i] == 1:
                xs += 1
                pos = j
        if xs == 1:
            essentials.append(pos)
    return essentials


def remove_duplicats_list(imps):
    new = []
    for el in imps:
        if el not in new:
            new.append(el)
    return new


def all_zeros(chart):
    for i in chart:
        for j in i:
            if j != 0:
                return False
    return True


def petrick_method(chart):
    bad_sum = []
    for column in range(len(chart[0])):
        sum = []
        for row in range(len(chart)):
            if chart[row][column] == 1:
                sum.append([row])
        bad_sum.append(sum)
    for i in range(len(bad_sum) - 1):
        bad_sum[i+1] = multiplicate(bad_sum[i], bad_sum[i+1])
    sums = sorted(bad_sum[len(bad_sum) - 1])
    answers = []
    shortest = len(sums[0])
    for sum in sums:
        if len(sum) == shortest:
            answers.append(sum)
        else:
            break
    return answers


def real_cost(imp):
    cost = 0
    for bit in imp:
        if bit != '-':
            cost += 1
    return cost


def multiplicate(sum1, sum2):
    product = []
    if is_empty(sum1) and is_empty(sum2):
        return product
    elif is_empty(sum1):
        return sum2
    elif is_empty(sum2):
        return sum1
    else:
        for el1 in sum1:
            for el2 in sum2:
                if el1 == el2:
                    product.append(el1)
                else:
                    product.append(list(set(el1 + el2)))
        product.sort()
        return list(v for v, _ in groupby(product))


def print_answer(variables, primes, imps):
    print("\tSolution:")
    if len(primes) == 1:
        if len(primes[0]) == 1:
            flag = 1
            for bit in imps[primes[0][0]]:
                if bit != '-':
                    flag = 0
            if flag == 1:
                print("1\n\n")
                return
    for group in primes:
        word = []
        for el in group:
            for i in range(len(imps[el])):
                if imps[el][i] == '-':
                    continue
                elif imps[el][i] == '0':
                    word.append("(~")
                    word.append(variables[i])
                    word.append(")")
                elif imps[el][i] == '1':
                    word.append(variables[i])
            if el != group[len(group) - 1]:
                word.append(" + ")
        print(''.join(word))
