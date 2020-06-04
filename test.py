def formGraphList(nodes, matrix):
    res = { str(node): [] for node in nodes}
    for node in nodes:
        i=0
        for dist in matrix[node]:
            if float(dist) != 0:
                res[str(node)].append((str(i), float(dist)))
            i+=1
    return res