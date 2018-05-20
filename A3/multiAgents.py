# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util, sys
import math

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newGhostPositions = successorGameState.getGhostPositions()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        scaredScore = min(newScaredTimes)
        capsules = successorGameState.getCapsules()


        "*** YOUR CODE HERE ***"      

        if len(newFood) == 0:
          return 10 + successorGameState.getScore()

        closest_food = newFood[0]
        min_distance = abs(closest_food[0] - newPos[0]) + abs(closest_food[1] - newPos[1])

        for food in newFood:
          temp_distance = abs(food[0] - newPos[0]) + abs(food[1] - newPos[1])
          if temp_distance < min_distance:
            min_distance = temp_distance
            closest_food = food
        
        

        ghost_cost = 999999
        for i in newGhostPositions:
          min_cost = abs(i[0] - newPos[0]) + abs(i[1] - newPos[1])
          if min_cost < ghost_cost:
            ghost_cost = min_cost
      

        if ghost_cost > 2:
          return 1/float(min_distance**2) + successorGameState.getScore()
          
        else:
          return ghost_cost



def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState, depth=0, agent=0, low=False, high=True):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """

        total = gameState.getNumAgents()
        if agent >= total:
          agent = 0

        if (len(gameState.getLegalActions(agent)) == 0) or \
          (depth == self.depth*total):
          return self.evaluationFunction(gameState)
        options = []

        if (agent+1)%total == 0:
          newhigh = True
          newlow = False
      
        else:
          newhigh = False
          newlow = True

        for branch in gameState.getLegalActions(agent):
          newGameState = gameState.generateSuccessor(agent, branch)     

          options.append(self.getAction(newGameState, depth+1, agent+1, \
            newlow, newhigh)),


        if depth == 0:
          key = max(options)
          index = options.index(key)
          return gameState.getLegalActions(agent)[index]
        
        elif high:
          return max(options)
        
        elif low:
          return min(options)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState, depth=0, agent=0, low=False, high=True, alpha=-99999, \
      beta = 99999):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """     
        stack = []
        total = gameState.getNumAgents()
        if agent >= total:
          agent = 0

        if (len(gameState.getLegalActions(agent)) == 0) or \
          (depth == self.depth*total):
          return self.evaluationFunction(gameState)
        options = []

        if (agent+1)%total == 0:
          newhigh = True
          newlow = False
      
        else:
          newhigh = False
          newlow = True

        for branch in gameState.getLegalActions(agent):
          newGameState = gameState.generateSuccessor(agent, branch)     

          options.append(self.getAction(newGameState, depth+1, agent+1, \
            newlow, newhigh, alpha, beta)),

          if low:
            beta = min(options + [beta])
          if high:
            alpha = max(options + [alpha])
          if alpha >= beta:            
            break

        if depth == 0:
          key = max(options)
          index = options.index(key)
          return gameState.getLegalActions(agent)[index]
        
        elif high:
          return max(options)
        
        elif low:
          return min(options)
     


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState, depth=0, agent=0, low=False, high=True):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        total = gameState.getNumAgents()
        if agent >= total:
          agent = 0

        if (len(gameState.getLegalActions(agent)) == 0) or \
          (depth == self.depth*total):
          return self.evaluationFunction(gameState)
        options = []

        if (agent+1)%total == 0:
          newhigh = True
          newlow = False
      
        else:
          newhigh = False
          newlow = True

        for branch in gameState.getLegalActions(agent):
          newGameState = gameState.generateSuccessor(agent, branch)     

          options.append(self.getAction(newGameState, depth+1, agent+1, \
            newlow, newhigh)),


        if depth == 0:
          key = max(options)
          index = options.index(key)
          return gameState.getLegalActions(agent)[index]
        
        elif high:
          return max(options)
        
        elif low:
          return sum(options)/len(options)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood().asList()
    newGhostStates = currentGameState.getGhostStates()
    newGhostPositions = currentGameState.getGhostPositions()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    scaredScore = min(newScaredTimes)
    capsules = currentGameState.getCapsules()

    "*** YOUR CODE HERE ***"      

    if len(newFood) == 0:
      return 10 + currentGameState.getScore()

    closest_food = newFood[0]
    min_distance = abs(closest_food[0] - newPos[0]) + abs(closest_food[1] - newPos[1])
    total_distance = 0

    for food in newFood:
      temp_distance = abs(food[0] - newPos[0]) + abs(food[1] - newPos[1])
      total_distance += 1/float(temp_distance)
      if temp_distance < min_distance:
        min_distance = temp_distance
        closest_food = food
    


    ghost_cost = 999999
    for i in newGhostPositions:
      min_cost = abs(i[0] - newPos[0]) + abs(i[1] - newPos[1])
      if min_cost < ghost_cost:
        ghost_cost = min_cost
  

    capsules_distance = 100000
    if len(capsules) != 0:
      capsules_distance = abs(capsules[0][0] - newPos[0]) + abs(capsules[0][1] - newPos[1])

    a = 1/float(len(newFood))
    b = 1/float(min_distance)
    c = 0.1*currentGameState.getScore()
    d = 5/float(capsules_distance)
    e = scaredScore

    if currentGameState.isLose():
      return -10000
    if scaredScore > 2 and scaredScore < 30:
      return 1/ghost_cost
    if ghost_cost > 2:
      if random.random()<0.995:
        return a + b + c + d + e
      else:
        return 10000
    else:
      return ghost_cost



# Abbreviation
better = betterEvaluationFunction


