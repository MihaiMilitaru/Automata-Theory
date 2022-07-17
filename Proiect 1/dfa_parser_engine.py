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
startNodeActive = False

# Checks if args are valid and if the file exists
# Returns file name
def verifyArgs():
  if len(sys.argv) != 2:
    print("The only argument must be the config file.")
    exit(0)

  configFile = sys.argv[1]
  try :
    open(configFile)
  except :
    print(f"Config file {configFile} doesn't exist.")
    exit(0)
  
  return configFile

# Reads sigma line
def readSigmaLine(item):
  sigma.append(item)

# Reads state line and verifies if it respects
# the restrictions
def readStatesLine(item):
  stateItemList = item.split(", ")
  if len(stateItemList) > 3:
    print("Too many attributes for one state.")
    exit(0)

  if len(stateItemList) > 1:
    for stateItem in stateItemList[1:]:
      if stateItem != 'S' and stateItem != 'F':
        print("Invalid attribute of state item.")
        exit(0)

  if stateItemList[0] not in states:
    states.append(stateItemList[0])

  global startNodeActive
  if 'S' in item[1:]:
    if not startNodeActive:
      startNodeActive = True
    else:
      print("There are multiple start nodes in the config file.")
      exit(0)

  statesAttrib.append(stateItemList)

# Reads transitions line
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

# Checks if the transitions are valid
def checkTransitions():
  for item in transitions:
    if len(item) != 3:
      print("Invalid transition.")
      exit(0)

    if (item[0] not in states and item[2] not in states):
      print("Invalid states in transition.")
      exit(0)

    if (item[1] not in sigma):
      print("Invalid letter in transition.")
      exit(0)

# Creates transitions dictionary for easier searching
# Each state points to an array of tuples respecting the rule
# (letter, state)
def addTransitionsToDict():
  for item in transitions:
    if item[0] in transitionDict:
      transitionDict[item[0]].append([x for x in item[1:]])
    else:
      transitionDict[item[0]] = [[item[1], item[2]]]

# Verifies that the DFA given respects determinism
def verifyDeterminism():
  for state in transitionDict:
    verifSet = set()
    for item in transitionDict[state]:
      verifSet.add(item[0])
    if len(verifSet) != len(transitionDict[state]):
      print("Config file doesn't respect determinism.")
      exit(0)
    verifSet = set()

def verifyFile():
  readConfigFile(verifyArgs())
  checkTransitions()
  addTransitionsToDict()
  verifyDeterminism()

verifyFile()

print("FILE FORMAT : OK")
# print(f"Sigma -> {sigma}")
# print(f"States -> {states}")
# print(f"States with attributes -> {statesAttrib}")
# print(f"Transitions -> {transitions}")
# print(f"Transition Dictionary -> {transitionDict}")