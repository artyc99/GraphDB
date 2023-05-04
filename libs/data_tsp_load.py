import math


def load(path: str):
    vertices = []

    with open(path, 'r+') as file:
        while True:
            line = file.readline()
            if line.startswith('NODE_COORD_SECTION'):
                break

        for line in file:
            if line.startswith('EOF'):
                break

            words = line.split(' ')

            id_ = int(words[0])
            x = float(words[1])
            y = float(words[2])

            vertices.append((id_, x, y))

    edges = []

    for v1 in vertices:
        for v2 in vertices:
            if v1 is not v2:
                edges.append((v1[0], v2[0], lambda x1, x2, y1, y2: math.sqrt((x1-x2)**2 + (y1-y2)**2)))

    return vertices, edges
