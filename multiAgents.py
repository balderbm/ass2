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
import random, util
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
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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

    def getAction(self, gameState):


        def MaxVal(gameState,depth):

            if gameState.isWin() or gameState.isLose(): #Check if in winning state
                return gameState.getScore()
            v = -math.inf #set v value to -infinite
            a = Directions.STOP
            actions = gameState.getLegalActions(0) #get all possible moves for pacman in starting position
            for action in actions: #check every possible move
                v2 = MinVal(gameState.generateSuccessor(0,action),depth,1) #go to ghost turn
                if v2>v:
                    v = v2 #get new improved v value
                    a = action
            if depth == 0: #if at final depth return the best action
                return a
            else:
                return v

        def MinVal(gameState,depth,player): #player is which ghost we are checking for
            if gameState.isWin() or gameState.isLose(): #check if in a final state (either win or loss)
                return gameState.getScore()
            v = math.inf #set v to infinite
            actions = gameState.getLegalActions(player) #get possible starting moves for the ghost
            for action in actions: #check every possible move
                if player == gameState.getNumAgents() - 1: #if we are on the last ghost
                    if depth == self.depth -1: #if we are at max depth
                        v2 = self.evaluationFunction(gameState.generateSuccessor(player,action))
                    else:
                        v2 = MaxVal(gameState.generateSuccessor(player,action),depth + 1) #run possible moves for pacman
                else:
                    v2 = MinVal(gameState.generateSuccessor(player,action), depth, player + 1) #next ghost 
                if v2<v:
                    v=v2
            return v
        return MaxVal(gameState,0)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):

        alpha=-math.inf #define alpha and beta
        beta=math.inf
        def MaxVal(gameState,depth,alpha,beta):
            if gameState.isWin() or gameState.isLose(): #check if in a finished state
                return gameState.getScore()
            v = -math.inf #set v to - infinite
            a = Directions.STOP
            actions = gameState.getLegalActions(0)
            for action in actions:
                v2 = MinVal(gameState.generateSuccessor(0,action),depth,1, alpha, beta) #run the minvalue function for each possible move for pacman
                if v2>v:
                    v = v2
                    a = action
                    alpha=max(alpha, v) #get new alpha value if improved v is found
                if v > beta:
                    return v #if a better beta is found, skip remainding checks in this tree
            if depth == 0: #if end of depth return "a" value
                return a
            else:
                return v

        def MinVal(gameState,depth,player,alpha,beta): #player is which ghost that is going to move.
            if gameState.isWin() or gameState.isLose(): #check if in a finished state
                return gameState.getScore()
            v = math.inf #set v to infinite
            actions = gameState.getLegalActions(player) #get first move for ghost
            for action in actions:
                if player == gameState.getNumAgents() - 1: #if we are on the last ghost
                    if depth == self.depth -1: #if we are at max depth
                        v2 = self.evaluationFunction(gameState.generateSuccessor(player,action)) #assign v2 value
                    else:
                        v2 = MaxVal(gameState.generateSuccessor(player,action),depth + 1,alpha, beta) #go to pacmans turn
                else:
                    v2 = MinVal(gameState.generateSuccessor(player,action), depth, player + 1, alpha, beta) #next ghost
                if v2<v:
                    v=v2
                    beta=min(beta,v) #find optimal beta
                if v< alpha: #skip remainding checks if an alpha value greater than v is found
                    return v
            return v
        return MaxVal(gameState,0,alpha, beta)




class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
