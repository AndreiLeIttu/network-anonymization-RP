path = input("Path to graph to be preprocessed: ")

edges = []
n = 0
k = int(input("Value of the k parameter: "))

with open(path, 'r') as file:
    lines = file.readlines()
    skipped_lines = int(input("Number of lines to skip to get to edges:"))
    lines = lines[skipped_lines:]
    print(lines)
    for line in lines: 
        numbers = line.strip('\n').split(' ')
        if (int(numbers[0]) == int(numbers[1])):
            continue
        edges.append((int(numbers[0]), int(numbers[1])))
        n = max(n, edges[-1][0])
        n = max(n, edges[-1][1])

file_name = input("Name of the newly created file?")
with open(file_name+"dzn", 'w') as file:
    output = f"n = {n};\nm = {len(edges)};\nk = {k};\ninitial_edges = [\n"
    for edge in edges:
        output+=f"({edge[0]}, {edge[1]}),\n"
    output+="];"
    file.write(output)