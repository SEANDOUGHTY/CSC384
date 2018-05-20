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


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    #print "Start:", problem.getStartState()
    #print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    #print "Start's successors:", problem.getSuccessors(problem.getStartState())
    

    stack = util.Stack()
    stack.push((problem.getStartState(),))
    final_path = ()
    
    while stack.isEmpty() == False:
        step = stack.pop()
        if problem.isGoalState(step[0]):
            final_path = step
            break
        for option in problem.getSuccessors(step[0]):
            if option[0] not in step:
                stack.push(option + step)
    
    instruction = list(final_path[-3::-3])
    
    return instruction


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    queue = util.Queue()
    queue.push((problem.getStartState(),))
    cost = {problem.getStartState():0}
    final_path = ()

    while queue.isEmpty() == False:
        step = queue.pop()
        if problem.isGoalState(step[0]):
            final_path = step
            break
        
        if problem.getCostOfActions(step[-3::-3]) <= cost[step[0]]:
            for option in problem.getSuccessors(step[0]):
                if option[0] in cost:
                    if problem.getCostOfActions((option+step)[-3::-3]) < \
                       cost[option[0]]:
                        
                        queue.push(option + step)
                        cost[option[0]] = \
                            problem.getCostOfActions((option+step)[-3::-3])
                else:
                    queue.push(option + step)
                    cost[option[0]] = \
                        problem.getCostOfActions((option+step)[-3::-3])                    

    instruction = list(final_path[-3::-3])
    
    cost = problem.getCostOfActions(instruction)
    return instruction


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    pqueue = util.PriorityQueue()
    pqueue.push((problem.getStartState(),), 1)
    cost = {problem.getStartState():0}
    final_path = ()

    while pqueue.isEmpty() == False:
        step = pqueue.pop()
        if problem.isGoalState(step[0]):
            final_path = step
            break
        
        if problem.getCostOfActions(step[-3::-3]) <= cost[step[0]]:
            for option in problem.getSuccessors(step[0]):
                if option[0] in cost:
                    if problem.getCostOfActions((option+step)[-3::-3]) < \
                       cost[option[0]]:
                        
                        cost[option[0]] = \
                            problem.getCostOfActions((option+step)[-3::-3])
                        pqueue.push((option + step), cost[option[0]])
                else:
                    cost[option[0]] = \
                            problem.getCostOfActions((option+step)[-3::-3])
                    pqueue.push((option + step), cost[option[0]])                   

    instruction = list(final_path[-3::-3])
    
    cost = problem.getCostOfActions(instruction)
    return instruction


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    pqueue = util.PriorityQueue()
    pqueue.push((problem.getStartState(),), 1)
    cost = {problem.getStartState():0}
    final_path = ()
    
    while pqueue.isEmpty() == False:
        step = pqueue.pop()
        if problem.isGoalState(step[0]):
            final_path = step
            break
        
        #print(problem.getCostOfActions(step[-3::-3]) <= cost[step[0]])    
        if problem.getCostOfActions(step[-3::-3]) <= cost[step[0]]:
            for option in problem.getSuccessors(step[0]):
                g = problem.getCostOfActions((option+step)[-3::-3])
                h = heuristic(option[0], problem)
                if option[0] in cost:
                    if (g + h) < cost[option[0]]:
                            
                            cost[option[0]] = g + h
                            pqueue.push((option + step), cost[option[0]])
                else:
                    cost[option[0]] = g + h
                    pqueue.push((option + step), cost[option[0]])
            
    instruction = list(final_path[-3::-3])
        
    cost = problem.getCostOfActions(instruction)
    return instruction    


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
