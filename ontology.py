from collections import deque


class TrieNode:
    def __init__(self, letter):
        if letter:
            self.letter = letter
        else:
            self.letter = None
        self.children = {}

    def add(self, child):
        self.children[child.letter] = child


class Trie:
    def __init__(self):
        self.root = TrieNode(None)

    def insert_words(self, word):
        if not word:
            return
        current_node = self.root
        for letter in word:
            if letter in current_node.children:
                current_node = current_node.children[letter]
            else:
                child_node = TrieNode(letter)
                current_node.add(child_node)
                current_node = child_node

    def contains(self, query):
        return self.contains_helper(query, self.root) is not None

    def contains_helper(self, word, node):
        if not word:
            return node
        if word[0] in node.children:
            return self.contains_helper(word[1:], node.children[word[0]])
        else:
            None


class Node:
    def __init__(self, value):
        self.trie = Trie()
        self.title = value
        self.children = []
        self.numChild = 0

    def add_child(self, child):
        node = Node(child)
        self.children.append(node)
        self.numChild += 1


class Tree:
    def __init__(self):
        self.tree = {}

    def add_node(self, node):
        self.tree[node.title] = node

    def make_tree(self, input):
        root = Node(input.popleft())
        self.add_node(root)

        parents = deque()
        parents.append(root)
        input.popleft()
        previous = None

        while input:
            current = input.popleft()
            if current == "(":
                parents.appendleft(previous)
            elif current == ")":
                parents.popleft()
            else:
                node = Node(current)
                previous = node
                self.add_node(node)
                parents[0].add_child(node.title)

    def make_trie(self, root, words):
        self.tree[root].trie.insert_words(words)

    def fetch_count(self, root, words):
        count = []
        if root in self.tree:
            self.fetch_count_helper(root, words, count)
        return len(count)

    def fetch_count_helper(self, root, words, count):
        if self.tree[root].trie.contains(words):
            count.append(1)
        if self.tree[root].numChild > 0:
            for each in self.tree[root].children:
                self.fetch_count_helper(each.title, words, count)
        else:
            return


class Ontology:
    def __init__(self):
        self.tree = Tree()

    def parse_to_tree(self, s):
        if s is None:
            print "Error: The input is empty"
            return -1
        parsed = deque(s.split())
        self.tree.make_tree(parsed)

    def parse_to_trie(self, s):
        if s is None:
            print "Error: The input is empty"
            return -1
        root, words = s.split(": ")
        self.tree.make_trie(root, words)

    def find_count(self, s):
        if s is None:
            print "Error: The input is empty"
            return -1
        root, words = s.split(" ", 1)
        return self.tree.fetch_count(root, words)


def main():
    ontology = Ontology()

    # Retrieve and parse tree string
    tree_length = int(raw_input())
    tree_string = raw_input()
    ontology.parse_to_tree(tree_string)

    # Retrieve and parse entries
    entries_length = int(raw_input())
    for i in range(0, entries_length):
        ontology.parse_to_trie(raw_input())

    # Retrieve and parse searches
    search_length = int(raw_input())
    results = []
    for i in range(0, search_length):
        results.append(ontology.find_count(raw_input()))

    for each in results:
        print each

if __name__ == '__main__':
    main()