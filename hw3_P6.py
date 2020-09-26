# Instructions:
# Input:
# every list on a seperate line, for the last line, please also add '\n' (press enter). Enter ctrl+D to terminate input.
# Output:
# The first line is the maximum weight in clique.
# The second line shows nodes in clique. If true, the node is included in the clique; otherwise, the node is not included.

from z3 import *


class node:
    def __init__(self, name, weight, neighbors):
        self.name = name
        self.weight = weight
        self.neighbors = neighbors
        self.bool = Bool(name)

# check every two nodes in the clique should be neighbors for each other.
def check_neighbor_relation(node1, node2):
    if node1.name in node2.neighbors and node2.name in node1.neighbors:
        return True
    else:
        return False

def get_clique_sum(node_list, model):
    clique_sum = 0
    for node in node_list:
        if model.evaluate(node.bool, model_completion=True):
            clique_sum += int(node.weight)
    return clique_sum


def input_process():
    raw_node_list = sys.stdin.readlines()
    node_list = []
    for raw_node in raw_node_list:
        name, weight, neighbors = raw_node[1:-2].split(',', 2)
        new_node = node(name, weight, neighbors)
        node_list.append(new_node)
    return node_list


def main():
    node_list = input_process()
    s = Solver()
    for node1 in node_list:
        for node2 in node_list:
            clique_condition = Implies(And(node1.bool, node2.bool, node1.name != node2.name), check_neighbor_relation(node1, node2))
            s.add(clique_condition)
    node_bool_list = [node.bool for node in node_list]
    s.add(Or(node_bool_list))

# add constraints for the clique: 1. every two nodes should be neighbors for each other. 2. At least one node in the clique.
# let the solver find all the possible cliques and compute the max sum of them.
    max_sum = 0
    while s.check() == sat:
        m = s.model()
        sum_weights = get_clique_sum(node_list, m)
        if sum_weights > max_sum:
            max_sum = sum_weights
            max_m = m
        comparison_list = []
        for x in node_bool_list:
            comparison_list.append((x != m[x]))
        s.add(Or(comparison_list))

    return [max_m, max_sum]


if __name__ == "__main__":
    max_m, max_sum = main()
    print(max_sum)
    print(max_m)
