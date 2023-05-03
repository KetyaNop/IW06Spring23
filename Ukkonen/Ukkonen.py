import sys
import time
import random


class Node:
    def __init__(self, start=None, end=None):
        self.start = start
        self.end = end
        self.children = {}
        self.suffix_link = None
        self.leaf_count = 0

    def edge_length(self):
        if self.end is not None:
            return self.end[0] - self.start + 1
        return -1


class SuffixTree:
    def render_tree(self, node, level):
        for child in node.children:
            for i in range(level):
                sys.stdout.write(" ")
            sys.stdout.write("|")
            for i in range(level):
                sys.stdout.write("-")
            curr_node = node.children[child]
            print(self.string[curr_node.start : curr_node.end[0] + 1])
            self.render_tree(curr_node, level + 1)

    def __str__(self):
        return "String: %s, Remaining_suffixes: %d" % (
            self.string,
            self.remaining_suffixes,
        )

    def __init__(self, string):
        self.count = 0
        self.string = string
        self.root = Node()
        self.active_node = self.root
        self.active_edge = None
        self.active_length = 0
        self.remaining_suffixes = 0
        self.end = [-1]

        self.build_tree()

    def build_tree(self):
        # Loop through all characters
        for i in range(len(self.string)):
            # print("adding: %s step: %d" % (self.string[i], i + 1))
            self.add_prefix(i)
            # self.render_tree(self.root, 1)
            # print("------")

    def add_prefix(self, i):
        self.end[0] = i
        self.remaining_suffixes += 1
        previous_new_node = None
        curr_char = self.string[i]

        while self.remaining_suffixes > 0:
            # print("loop")
            if self.active_length == 0:
                self.active_edge = curr_char
            # if active edge does not exist at active point, then
            # create a new leaf node
            if self.active_edge not in self.active_node.children:
                self.active_node.children[curr_char] = Node(i, self.end)
                # if (self.string[self.active_node.start : self.active_length]) == "":
                #     print("creating new leaf: %s from root" % (curr_char))
                # else:
                #     print(
                #         "creating new leaf from active edge: %s"
                #         % (self.string[self.active_node.start : self.active_length])
                #     )
            # current character already exists at active edge + 1 in tree implicitly, update active point and increment remainder
            else:
                if self.active_length == 0:
                    # print("character already exist at active edge + string label 0")
                    self.update_active_point(i)
                    # self.remaining_suffixes += 1 # remaining suffix is added implicitly since we break and remaining suffix decremend is skipped
                    break
                elif (
                    self.string[
                        self.active_node.children[self.active_edge].start
                        + self.active_length
                    ]
                    == curr_char
                ):
                    # print(
                    #     "character already exist at active edge + string label ",
                    #     self.active_length,
                    # )
                    self.update_active_point(i)
                    # self.remaining_suffixes += 1 # remaining suffix is added implicitly since we break and remaining suffix decremend is skipped
                    break
                # print("fall off tree, we split node at active point")
                # we fall off the tree, so we need to split edge, insert an internal node a new leaf node
                new_leaf_node = Node(i, self.end)
                new_split_node = Node(
                    self.active_node.children[self.active_edge].start
                    + self.active_length,
                    self.end,
                )
                split_node_char = self.string[
                    self.active_node.children[self.active_edge].start
                    + self.active_length
                ]
                self.active_node.children[self.active_edge].end = [
                    self.active_length
                    - 1
                    + self.active_node.children[self.active_edge].start
                ]
                self.active_node.children[self.active_edge].children[
                    split_node_char
                ] = new_split_node
                self.active_node.children[self.active_edge].children[
                    curr_char
                ] = new_leaf_node

                if previous_new_node is not None:
                    # print(
                    #     "add suffix link from %s to %s"
                    #     % (
                    #         self.string[
                    #             previous_new_node.start : previous_new_node.end[0] + 1
                    #         ],
                    #         self.string[
                    #             self.active_node.children[self.active_edge]
                    #             .start : self.active_node.children[self.active_edge]
                    #             .end[0]
                    #             + 1
                    #         ],
                    #     )
                    # )
                    previous_new_node.suffix_link = self.active_node.children[
                        self.active_edge
                    ]

                # save node for suffix link
                previous_new_node = self.active_node.children[self.active_edge]

                # update active point

                # case 1: if active node is root
                if self.active_node == self.root:
                    if (
                        self.string[i - self.remaining_suffixes + 2]
                        in self.active_node.children
                    ):
                        self.active_length = 1
                        self.active_edge = self.string[i - self.remaining_suffixes + 2]
                        # print(
                        #     "new active edge: %s, active length: %d"
                        #     % (self.active_edge, self.active_length)
                        # )
                    else:
                        self.active_length = 0
                        self.active_edge = None
                        # print("new active edge: (root, Null, 0)")

                # case 2: if active node is not the root node
                if self.active_node != self.root:
                    # case 2.1: if there is a suffix link
                    if self.active_node.suffix_link is not None:
                        # print("active point is not root node and suffix link exists")
                        self.active_node = self.active_node.suffix_link
                    # case 2.2: if there is no suffix link
                    else:
                        self.active_node = self.root

            self.remaining_suffixes -= 1
        # self.remaining_suffixes -= 1

    def walk_down(self, node):
        if self.active_length >= node.edge_length():
            self.active_edge += node.edge_length()
            self.active_length -= node.edge_length()
            self.active_node = node
            return True
        return False

    def update_active_point(self, i):
        curr_char = self.string[i]
        self.active_length += 1
        if self.active_length == 0:
            self.active_edge = curr_char

        if (
            self.active_length
            > self.active_node.children[self.active_edge].edge_length()
        ):
            self.active_length = 1
            self.active_node = self.active_node.children[self.active_edge]
            self.active_edge = curr_char
        # if (
        #     self.active_length
        #     == self.active_node.children[self.active_edge].edge_length()
        # ):
        #     print("active point is at the end of an edge")
        # print(
        #     "active edge: %s, active length: %d"
        #     % (self.active_edge, self.active_length)
        # )

    def count_leaf_nodes(self, node):
        if node is None:
            return 0
        if len(node.children) == 0:
            return 1
        count = 0
        for childNode in node.children:
            count = count + self.count_leaf_nodes(node.children[childNode])
        return count

    def pre_process(self, node):
        self.pre_process_helper(node)
        for childNode in node.children:
            self.pre_process_helper(node.children[childNode])

    def pre_process_helper(self, node):
        node.leaf_count = self.count_leaf_nodes(node)


def count_occurrences(suffix_tree, node, inputString, pattern):
    if pattern[0] in node.children:
        node = node.children[pattern[0]]
        edgeLength = node.edge_length()
        if edgeLength >= len(pattern):
            if pattern == inputString[node.start : node.start + len(pattern)]:
                return suffix_tree.count_leaf_nodes(node)
        elif pattern[0:edgeLength] == inputString[node.start : (node.end[0] + 1)]:
            return count_occurrences(
                suffix_tree, node, inputString, pattern[edgeLength:]
            )
        else:
            return 0
    return -1


# suffix_tree = SuffixTree("ABCABDABCE$")
# suffix_tree.pre_process(suffix_tree.root)
# print(suffix_tree.render_tree(suffix_tree.root, 1))
# # print(suffix_tree.count_leaf_nodes(suffix_tree.root))
# print(
#     "occurence:",
#     count_occurrences(suffix_tree, suffix_tree.root, suffix_tree.string, "AB"),
# )
# print(suffix_tree.count_leaf_nodes(suffix_tree.root.children["B"].children["C"]))

# test
with open("BitString.txt", "r") as file:
    bit_string = file.read().replace("\n", "")
with open("chimpanzee.txt", "r") as file:
    chim = file.read().replace("\n", "")
with open("Protein.txt", "r") as file:
    protein = file.read().replace("\n", "")
with open("moby10b.txt", "r") as file:
    moby = file.read().replace("\n", "")


# length = [20000, 40000, 80000, 160000, 320000, 640000, 1280000]
length = [1]
dataSet = [
    bit_string,
    moby,
    protein,
    chim,
]
dataSet_description = ["bit string", "moby", "protein", "chim DNA"]

for length_to_test in length:
    print("Test Construction Length: ", length_to_test)
    for data_id in range(len(dataSet)):
        print("\tDataset: ", dataSet_description[data_id])
        data = dataSet[data_id]
        total_time = 0
        for i in range(3):
            tic = time.perf_counter()
            suffix_tree = SuffixTree(data[0:length_to_test] + "$")
            # suffix_tree.pre_process(suffix_tree.root)
            toc = time.perf_counter()
            total_time = total_time + toc - tic
        average_time = total_time / 3
        print("\tAverage Time is: ", average_time)


# test query time

protein_alphabet = [
    "A",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "K",
    "L",
    "M",
    "N",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "V",
    "W",
    "Y",
]
moby_alphabet = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]
DNA_alphabet = ["A", "G", "C", "T"]
binary_string_alphabet = ["0", "1"]

moby_tree = SuffixTree(moby + "$")
bit_tree = SuffixTree(bit_string + "$")
protein_tree = SuffixTree(protein + "$")
DNA_tree = SuffixTree(chim + "$")

query_length = [10, 20, 40, 80, 160, 320]
alphabet = [moby_alphabet, bit_string, protein_alphabet, DNA_alphabet]
suffix_tree = [moby_tree, bit_tree, protein_tree, DNA_tree]
tree_description = ["moby", "bit string", "protein", "chim DNA"]


for length_to_test in query_length:
    print("Test Query length: ", length_to_test)
    for tree_id in range(len(suffix_tree)):
        print("\tDataset: ", tree_description[tree_id])
        tree = suffix_tree[tree_id]
        current_alphabet = alphabet[tree_id]
        total_time = 0
        query = ""
        for i in range(length_to_test):
            query = query + random.choice(current_alphabet)
        for i in range(100):
            tic = time.perf_counter()
            count_occurrences(tree, tree.root, tree.string, query)
            toc = time.perf_counter()
            total_time = total_time + toc - tic
        average_time = total_time / 3
        print("\tAverage Time is: ", average_time)

print(count_occurrences(moby_tree, moby_tree.root, moby_tree.string, "t"))
print(moby_tree.count_leaf_nodes(moby_tree.root.children["it"]))
print(moby_tree.string)
# suffix_tree.render_tree(suffix_tree.root, 1)
