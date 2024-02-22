# Code modified from https://github.com/JuhaW/NodeArrange, Thank you JuhaW

from collections import OrderedDict
from itertools import repeat

MARGIN_X = 200
MARGIN_Y = 150


class values():
    average_y = 0
    x_last = 0


def auto_position(node_tree):
    nodes_iterate(node_tree)


def outputnode_search(node_tree):  # return node/None
    outputnodes = []
    for node in node_tree.nodes:
        if not node.outputs:
            for input in node.inputs:
                if input.is_linked:
                    outputnodes.append(node)
                    break
    if not outputnodes:
        print("No output node found")
        return None
    return outputnodes


def nodes_iterate(ntree):
    nodeoutput = outputnode_search(ntree)
    if nodeoutput is None:
        return None
    a = []
    a.append([])
    for i in nodeoutput:
        a[0].append(i)

    level = 0

    while a[level]:
        a.append([])

        for node in a[level]:
            inputlist = [i for i in node.inputs if i.is_linked]
            if inputlist:

                for input in inputlist:
                    for nlinks in input.links:
                        # dont add parented nodes (inside frame) to list
                        # if not nlinks.from_node.parent:
                        node1 = nlinks.from_node
                        a[level + 1].append(node1)

            else:
                pass

        level += 1

    del a[level]
    level -= 1

    for x, nodes in enumerate(a):
        a[x] = list(OrderedDict(zip(a[x], repeat(None))))

    top = level
    for row1 in range(top, 1, -1):
        for col1 in a[row1]:
            for row2 in range(row1 - 1, 0, -1):
                for col2 in a[row2]:
                    if col1 == col2:
                        a[row2].remove(col2)
                        break

    levelmax = level + 1
    level = 0
    values.x_last = 0

    while level < levelmax:
        values.average_y = 0
        nodes = [x for x in a[level]]
        nodes_arrange(nodes, level)

        level = level + 1

    return None


def nodes_arrange(nodelist, level):
    parents = []
    for node in nodelist:
        parents.append(node.parent)
        node.parent = None

    widthmax = max([x.dimensions.x for x in nodelist])
    xpos = values.x_last - (widthmax + MARGIN_X) if level != 0 else 0
    values.x_last = xpos

    y = 0

    for node in nodelist:
        if node.hide:
            hidey = (node.dimensions.y / 2) - 8
            y = y - hidey
        else:
            hidey = 0

        node.location.y = y
        y = y - MARGIN_Y - node.dimensions.y + hidey
        node.location.x = xpos

    y = y + MARGIN_Y

    center = (0 + y) / 2
    values.average_y = center - values.average_y

    for node in nodelist:
        node.location.y -= values.average_y

    for i, node in enumerate(nodelist):
        node.parent = parents[i]
