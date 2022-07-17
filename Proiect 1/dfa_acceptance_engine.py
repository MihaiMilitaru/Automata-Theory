# ###################################
# #            GRUPA: 143           #
# #        Besliu Radu-Stefan       #
# #     Militaru Mihai-Alexandru    #
# #      Tillinger Marius-Petru     #
# ###################################

# TEST FILES: test1_dfa_config_file

import sys

# Global variables
sigma = []
statesAttrib = []
states = []
transitions = []
transitionDict = {}
inputStringList = list(sys.argv[2])

# Checks if args are valid and if the file exists
# Returns file name
def getArgs():
  configFile = sys.argv[1]
  open(configFile)
  
  return configFile

# Reads sigma line
def readSigmaLine(item):
  sigma.append(item)

# Reads states and creates 2 arrays, states and states with
# specific attributes (S, F, or both)
def readStatesLine(item):
  stateItemList = item.split(", ")

  if stateItemList[0] not in states:
    states.append(stateItemList[0])

  statesAttrib.append(stateItemList)

# Reads a line in the transitions block
def readTransitionsLine(item):
  transitionItemList = item.split(', ')
  transitions.append(transitionItemList)

# Checks every line in config file to see if current block changes
# Calls specific function in each case
def readConfigFile(file):
  file = open(file)
  currentState = "None"
  oldState = "None"

  # Verifies if we are currently in a "block"
  # Block = Sigma...End, States...End, Transitions...End
  # If it reaches End, currentState changes accordingly
  for line in file:
    if line[0] == '#':
      continue
    else:
      line = line.split('#')
      line = line[0]
      line = line.strip()
      oldState = currentState
      match line:
        case "Sigma:":
          currentState = "Sigma"

        case "States:":
          currentState = "States"

        case "Transitions:":
          currentState = "Transitions"

        case "End":
          currentState = "None"
      
      if currentState == oldState and currentState != "None" and line != '':
        line = line.strip()
        match currentState:

          case "Sigma":
            readSigmaLine(line)

          case "States":
            readStatesLine(line)

          case "Transitions":
            readTransitionsLine(line)

# Creates transitions dictionary for easier searching
# Each state points to an array of tuples respecting the rule
# (letter, state)
def addTransitionsToDict():
  for item in transitions:
    if item[0] in transitionDict:
      transitionDict[item[0]].append([x for x in item[1:]])
    else:
      transitionDict[item[0]] = [[item[1], item[2]]]

def getData():
  readConfigFile(getArgs())
  addTransitionsToDict()

# Tests if the DFA accepts the input given
def testAcceptance():
  # The starting node is searched
  startNode = None
  for state in statesAttrib:
    if (len(state) > 1 and state[1] == 'S'):
      startNode = state[0]
  
  # Each itteration, we check if the current node has
  # an edge with another node with the value of
  # the current letter
  # If the condition is not met, the DFA doesn't
  # accept the input
  for letter in inputStringList:
    for item in transitionDict[startNode]:
      if letter in item:
        startNode = item[1]
        break
    else:
      print(f"Input {sys.argv[2]} not accepted for this DFA.")
      exit(0)

  # We verify if the last node traversed has the attribute F
  for item in statesAttrib:
    if startNode in item and 'F' in item[1:]:
      print(f"Input {sys.argv[2]} accepted.")
      break
  else:
    print(f"Input {sys.argv[2]} not accepted for this DFA.")
    exit(0)
    

getData()
testAcceptance()

# print(f"Sigma -> {sigma}")
# print(f"States -> {states}")
# print(f"States with attributes -> {statesAttrib}")
# print(f"Transitions -> {transitions}")
# print(f"Transition Dictionary -> {transitionDict}")