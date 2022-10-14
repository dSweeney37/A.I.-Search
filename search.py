# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()



class Node:
    # Assigns the child and parent nodes to their respective local variables.
    def __init__(self, child, parent):
        self.node = child
        self.root = parent


    # Returns the node's position.
    def getPosition(self):
        return self.node[0]


    # Returns the action leading to the node.
    def getAction(self):
        return self.node[1]


    # Builds and returns a list of actions from the node to the destination node.
    def getActions(self, destination):
        actions = []
        temp = self

        while temp.getPosition() != destination:
            actions.insert(0, temp.getAction())

            temp = temp.root

        return actions



def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]



# Search the deepest nodes in the search tree first.
def depthFirstSearch(problem):
    from util import Stack

    # Initializes the open/closed sets.
    openSet = Stack()
    closedSet = []
    origin = problem.getStartState()


    # Pushes the starting state node onto the fringe.
    openSet.push(Node((origin, None, None), None))

    while True:
        # If there aren't anymore nodes to be expanded, then
        # there is no solution and an empty list is returned.
        if openSet.isEmpty():
            return []

        # Pops the most recently added node from the fringe to be processed.
        node = openSet.pop()
        position = node.getPosition()

        # If the node is a goal state, then a list of actions back to the origin is retrieved.
        if problem.isGoalState(position):
            return node.getActions(origin)

        # If the node's position is not in the closed set, parse the following code block.
        if position not in closedSet:
            # Adds the node's postion to the closed set.
            closedSet.append(position)

            # Retrieves a list of the node's childern and reverses it.
            children = problem.getSuccessors(position)
            children.reverse()

            # Creates new nodes for the children and pushes them onto the openSet.
            for child in children:
                openSet.push(Node(child, node))



# Search the shallowest nodes in the search tree first.
def breadthFirstSearch(problem):
    from util import Queue

    # Initializes the open/closed sets.
    openSet = Queue()
    closedSet = []
    origin = problem.getStartState()


    # Pushes the starting state node onto the fringe.
    openSet.push(Node((origin, None, None), None))
    
    while True:
        # If there aren't anymore nodes to be expanded, then
        # there is no solution and an empty list is returned.
        if openSet.isEmpty():
            return []

        # Pops the earliest added node from the fringe to be processed.
        node = openSet.pop()
        position = node.getPosition()

        # If the node is a goal state, then a list of actions back to the origin is retrieved.
        if problem.isGoalState(position):
            return node.getActions(origin)
            
        # If the parent's coordinates are not in the closed set, parse the following code block.
        if position not in closedSet:
            # Adds the node's postion to the closed set.
            closedSet.append(position)

            # Retrieves a list of the node's childern.
            children = problem.getSuccessors(position)

            # Creates new nodes for the children and pushes them onto the openSet.
            for child in children:
                openSet.push(Node(child, node))



# Search the node with the least total cost first.
def uniformCostSearch(problem):
    from util import PriorityQueue

    # Initializes the open/closed sets.
    openSet = PriorityQueue()
    closedSet = []
    origin = problem.getStartState()


    # Pushes the starting state node onto the fringe.
    openSet.push(Node((origin, None, None), None), 0)

    while True:
        # If there aren't anymore nodes to be expanded, then
        # there is no solution and an empty list is returned.
        if openSet.isEmpty():
            return []

        # Pops the cheapest node from the fringe to be processed.
        node = openSet.pop()
        position = node.getPosition()

        # If the node is a goal state, then a list of actions back to the origin is retrieved.
        if problem.isGoalState(position):
            return node.getPath(origin)

        # If the parent's coordinates are not in the closed set, parse the following code block.
        if position not in closedSet:
            # Adds the node's postion to the closed set.
            closedSet.append(position)

            # Retrieves a list of the node's childern.
            children = problem.getSuccessors(position)

            # Creates new nodes for the children and pushes them onto the openSet.
            for child in children:
                newNode = Node(child, node)

                openSet.push(newNode, problem.getCostOfActions(newNode.getPath(origin)))



def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0



# Search the node that has the lowest combined cost.
def aStarSearch(problem, heuristic=nullHeuristic):
    from util import PriorityQueue
    from searchAgents import manhattanHeuristic

    # Initializes the open/closed sets.
    openSet = PriorityQueue()
    closedSet = []
    origin = problem.getStartState()


    # Pushes the starting state node onto the fringe.
    openSet.push(Node((origin, None, None), None), 0)

    while True:
        # If there aren't anymore nodes to be expanded, then
        # there is no solution and an empty list is returned.
        if openSet.isEmpty():
            return []

        # Pops the cheapest node from the fringe to be processed.
        node = openSet.pop()
        position = node.getPosition()

        # If the node is a goal state, then the path back to the origin is retrieved and returned.
        if problem.isGoalState(position):
            return node.getPath(origin)

        # If the parent's coordinates are not in the closed set, parse the following code block.
        if position not in closedSet:
            # Adds the node's postion to the closed set.
            closedSet.append(position)

            # Retrieves a list of the node's childern.
            children = problem.getSuccessors(position)

            # Creates new nodes for the children and pushes them onto the openSet.
            for child in children:
                newNode = Node(child, node)

                openSet.push(newNode, problem.getCostOfActions(newNode.getPath(origin)) + heuristic(newNode.getPosition(), problem))



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
