import copy
import re

"""
    Digraph: Digraph object
    Autores: Lucas Hagen, Andy Ruiz e Leonardo Bombardelli
"""
class Digraph(object):
    nodes = {} # Dicionário com os nodos e seus adjacentes

    """ Constructor """
    def __init__(self):
        self.nodes = {}

    """
        addNode: Adds a node to the Digraph
        @param node: node, can be a int or a char
    """
    def addNode(self, node):
        if node not in self.nodes.keys():
            self.nodes[node] = []

    """
        addNode: Adds one or more nodes to the digraph
        @param nodes: node list (list of int or/and chars)
    """
    def addNodes(self, nodes):
        for node in nodes:
            self.addNode(node)

    """
        addArraw: Adds a arrow between two nodes. If the nodes does not exists, they are going to be created.
        @param origin: origin node (int/char)
        @param dest: destination node (int/char)
    """
    def addArrow(self, origin, dest):
        self.addNodes([origin, dest])
        self.nodes[origin].append(dest)

    """
        addArraws: Adds multiple arrows between a origin node and destination nodes.
        @param origin: origin node (int/char)
        @param arrows: destination nodes list (int/char)
    """
    def addArrows(self, node, arrows):
        self.addNodes([node] + arrows)
        self.nodes[node] = list(set(self.nodes[node] + arrows))

    """
        removeNode: Removes a node.
        @param node: node to be removed (int/char)
    """
    def removeNode(self, node):
        if node in self.nodes.keys():
            self.nodes.pop(node)
            for n in self.nodes.keys():
                if node in self.nodes[n]:
                    self.nodes[n].remove(node)

    """
        containsNode: check if node exists
        @param node: node (int/char)

        @return: Boolean
    """
    def containsNode(self, node):
        return node in self.nodes.keys()

    """
        connectedBFS: Checks if two nodes are connected. (BFS)
        @param origin: origin node (int/char)
        @param dest: destination node (int/char)

        @return: Boolean
    """
    def connectedBFS(self, origin, dest):
        nodeQueue = []
        checked = []
        nodeQueue.insert(0, origin)

        while nodeQueue != []:
            temp = nodeQueue.pop()

            if temp not in checked:
                checked.append(temp)
                if dest in self.nodes[temp]:
                    return True
                else:
                    for i in self.nodes[temp]:
                        nodeQueue.insert(0, i)
        return False

    """
        connectedBFS: Returns all Arrows

        @return: node list (in the following format): [arrow1, arrow2, arrow3, ...], onde:
            arrow1 = [0, 1]
            arrow2 = [1, 0]
            arrow3 = [originNode, destinationNode]
    """
    def getAllArraws(self):
        connections = []
        for node, arrows in self.nodes.items():
            for dest in arrows:
                if [node, dest] not in connections:
                    connections.append([node, dest])
        return connections

    """
        isCiclic: Checks if the digraph is ciclic.

        @return: Boolean
    """
    def isCiclic(self):
        for node in self.nodes.keys():
            nodeQueue = []
            checked = []
            nodeQueue.insert(0, node)

            while nodeQueue:
                temp = nodeQueue.pop()

                if temp not in checked:
                    checked.append(temp)
                    if node in self.nodes[temp]:
                        return True
                    else:
                        for i in self.nodes[temp]:
                            nodeQueue.insert(0, i)
        return False

    """
        reverseDigraph: Reverses all arrows from the Digraph

        @return: new Digraph with all arrows in the oposite direction
    """
    def reverseDigraph(self):
        reverse = Digraph()
        for origin, arrows in self.nodes.items():
            if arrows == []:
                reverse.addNode(origin)
            else:
                for dest in arrows:
                    reverse.addArraw(dest, origin)
        return reverse

    """
        getSCComponents: Lists all strongly connected components from the Digraph.
        This function is based in the Kosaraju's Algorithm.

        @return: list of node lists, ex: [[1, 2, 3], [4, 5], [6]]
    """
    def getSCComponents(self):
        components = []
        visited = []
        stack = []

        for node in self.nodes.keys():
            self.DFSUtil(node, visited, stack)

        rDigraph = self.reverseDigraph()

        visited = []
        while stack:
            temp = stack.pop()
            tempCmp = []
            if temp not in visited:
                rDigraph.DFSUtilReverse(temp, visited, tempCmp)
                components.append(tempCmp)

        return components

    """
        DFSUtil: auxiliar function for getSCComponents. Initializes the stack for the Kosaraju's Algorithm.
        @param node: Node (int/char)
        @param visited: node list
        @param stack: node stack
    """
    def DFSUtil(self, node, visited, stack):
        if node not in visited:
            visited.append(node)
            for child in self.nodes[node]:
                if child not in visited:
                    self.DFSUtil(child, visited, stack)
            stack.append(node)

    """
        DFSUtil: auxiliar function for getSCComponents. Consumes the stack from the Kosaraju's Algorithm.
        @param node: Node (int/char)
        @param visited: node list
        @param component: node list
    """
    def DFSUtilReverse(self, node, visited, component):
        if node not in visited:
            visited.append(node)
            component.insert(0, node)
            for child in self.nodes[node]:
                if child not in visited:
                    self.DFSUtilReverse(child, visited, component)

    """
        copyDigraph: deepcopies the digraph, creating a new object

        @return: copy of the digraph
    """
    def copyDigraph(self):
        return copy.deepcopy(self)


    """
        topologicalSorting: Returns a sorted list with the digraphs topological sorting.

        @return: node list or None (if digraph is ciclic)
    """
    def topologicalSorting(self):
        if self.isCiclic():
            return None

        cpy = self.copyDigraph()
        temp = []
        while cpy.nodes:
            temp.append(cpy.popNoParentsNode())
        return temp

    """
        popNoParentsNode: Searches for a node without parents and removes it.

        @return: Node (int/char) or None (if digrath is ciclic)
    """
    def popNoParentsNode(self):
        if self.isCiclic():
            return None

        for node in self.nodes.keys():
            if not self.nodeHasParents(node):
                self.removeNode(node)
                return node

    """
        nodeHasParents: check if node has parents
        @param node: Node (int/char)

        @return: Boolean
    """
    def nodeHasParents(self, node):
        for arrows in self.nodes.values():
            if node in arrows:
                return True
        return False

    """
        importFromText: Imports nodes and arrows from a string.
        @param str: String specified in the following format:

        "([graph size]
            (<origin node> <destination node1> <destination node2> ...)
            (<origin node2> <destination node1> ...)
            ...
        )"
    """
    def importFromText(self, str):
        for nodeStr in re.findall("([(][0-9 \n]+[)])", str): # Regex: finds all origin and destination combinations
            nodeData = re.findall("[0-9a-zA-Z]+", nodeStr) # Finds all ints and chars in the combination (origin node, destination node)

            self.addArraws(nodeData[0], nodeData[1:]) # Adds the arrows (the nodes are created if needed by the function addArrows)
        return self
