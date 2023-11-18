import json

from bTreeOperations import bTreeNode, searchNode

''' 
    buildTree.py file calling functions written in bTreeOperations.py file
'''


class buildtree:
    def __init__(self):
        self.data_path = "../data/"
        self.index_path = "../index/"
        self.page_link = "pageLink.txt"
        self.schemas = "schemas.txt"
        self.page_pool = "pagePool.txt"

    def buildBTree(self, rel, att, od):
        # create root node
        rootnode = bTreeNode(bTreeNode.getBTreePage(self))
        tuplefile = rootnode.getBTreeAttList(rel, att)
        rootnode = rootnode.insertNode(rootnode, tuplefile[0][0], tuplefile[0][1], od, rootnode)
        for i in range(1, len(tuplefile)):
            searchkey = tuplefile[i][0]
            location = tuplefile[i][1]
            rootnode = rootnode.insertNode(searchNode(rootnode, searchkey)[0], searchkey, location, od, rootnode)

        rootnode.__write__()

        with open(self.index_path + 'directory.txt') as f:
            directory = json.loads(f.read())

        # update directory
        with open(self.index_path + 'directory.txt', 'w') as f:
            tree = []
            tree.append(rel)
            tree.append(att)
            tree.append(rootnode.node_page)
            directory.append(tree)
            f.write(json.dumps(directory))
        print(rootnode.__print__())


if __name__ == '__main__':
    buildtree().buildBTree('Suppliers', 'sid', 2)
    buildtree().buildBTree('Supply', 'pid', 2)
