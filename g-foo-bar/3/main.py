
def get_parent(node, height):
    h1 = height
    current = (2 ** h1) -1

    if node == current:
        return -1

    while True:
        h1 -= 1
        left_son = current - (2 ** h1)
        right_son = current - 1

        if node == left_son or node == right_son:
            return current

        if node < left_son:
            # print 'went left', left_son
            current = left_son
        else:
            # print 'went right'
            current = right_son
    
# print get_parent(1, 3)


def solution(height, nodes):
    results = []
    for node in nodes:
        results.append(get_parent(node, height))

    return results
    



print solution(3, [7, 3, 5, 1])
# -1,7,6,3

print solution(5, [19, 14, 28])
# 21,15,29
