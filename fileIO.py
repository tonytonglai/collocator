with open('input.txt', "r") as f1:
    with open('output.txt', "w") as f2:
        for line in f1:
            # now we can split...
            wordTuple = line.replace('\n', '').split(' ')
            print(wordTuple)
            print('***\n\n')
            f2.write("{} {}\n".format(wordTuple[1], wordTuple[0]))