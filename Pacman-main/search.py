
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
from game import Directions
from typing import List
from util import Stack
from util import Queue
from util import PriorityQueue

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    stack = Stack()
    start = problem.getStartState()
    stack.push((start, []))
    visited = set()
    while not stack.isEmpty():
        state, actions = stack.pop()
        if problem.isGoalState(state):
            return actions
        if state not in visited:
            visited.add(state)
            for successor, action, step_cost in problem.getSuccessors(state):
                if successor not in visited:
                    stack.push((successor, actions + [action]))
    return []
    util.raiseNotDefined()

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    queue = Queue()
    start = problem.getStartState()
    queue.push((start, []))
    visited = set()
    while not queue.isEmpty():
        current_state, actions = queue.pop()
        if problem.isGoalState(current_state):
            return actions
        if current_state not in visited:
            visited.add(current_state)
            for successor, action, step_cost in problem.getSuccessors(current_state):
                if successor not in visited:
                    queue.push((successor, actions + [action]))

    return []
    util.raiseNotDefined()

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    pq = PriorityQueue()
    start = problem.getStartState()
    pq.push((start, []), 0)
    visited = set()
    costs = {start: 0}
    while not pq.isEmpty():
        current_state, actions = pq.pop()
        if problem.isGoalState(current_state):
            return actions
        if current_state not in visited:
            visited.add(current_state)
            for successor, action, step_cost in problem.getSuccessors(current_state):
                new_cost = costs[current_state] + step_cost
                if successor not in costs or new_cost < costs[successor]:
                    costs[successor] = new_cost
                    pq.push((successor, actions + [action]), new_cost)

    return []
    util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    queue = util.PriorityQueue()
    queue.push((problem.getStartState(),[],heuristic(problem.getStartState(),problem)),heuristic(problem.getStartState(),problem))
    checked = set()
    pathcost = {}
    priority = {}
    pathcost[problem.getStartState()] = 0
    priority[problem.getStartState()] = heuristic(problem.getStartState(),problem)
    while not queue.isEmpty():
        curState = queue.pop()
        checked.add(curState[0])
        if problem.isGoalState(curState[0]):
            return curState[1]
        successors = problem.getSuccessors(curState[0])
        for succ in successors:
            if succ[0] not in checked:
                pathcost[succ[0]] = pathcost[curState[0]] + succ[2]
                queue.push((succ[0],curState[1] + [succ[1]],pathcost[succ[0]] + heuristic(succ[0],problem)),pathcost[succ[0]] + heuristic(succ[0],problem))
                checked.add(succ[0])
                priority[succ[0]] = pathcost[succ[0]] + heuristic(succ[0],problem)
            elif priority[succ[0]] > pathcost[curState[0]] + succ[2] + heuristic(succ[0],problem):
                pathcost[succ[0]] = pathcost[curState[0]] + succ[2]
                queue.update((succ[0],curState[1] + [succ[1]],pathcost[succ[0]] + heuristic(succ[0],problem)),pathcost[succ[0]] + heuristic(succ[0],problem))
                priority[succ[0]] = pathcost[succ[0]] + heuristic(succ[0],problem)
    return []
    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch