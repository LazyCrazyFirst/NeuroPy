def writing_to_a_file(variables, value):
    variable = {}

    for k, i in zip(variables, range(len(variables))):
        variable[k] = (value[i])

    filename = 'variables.txt'
    file = open(filename, 'w+', encoding="utf-8")
    k = 0
    for value in variable.items():
        k += 1
        varia = str((value[0], value[1])).replace("(", "").replace(")", "").replace("'", "").replace(",", "")
        file.write(varia)
        if (len(variable) != k):
            file.write('\n')

    file.close()


def reading_from_a_file():
    geting = {}
    filename = 'variables.txt'
    file = open(filename, 'r', encoding="utf-8")
    value = ''
    for i in file.readlines():
        i = i.split()
        try:
            geting[i[0]] = int(i[1])
        except:
            for h in i[1:]:
                value += h + ' '
            geting[i[0]] = value[:len(value) - 1]
            value = ''
    file.close()
    return geting
