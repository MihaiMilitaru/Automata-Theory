# ###################################
# #            GRUPA: 143           #
# #        Besliu Radu-Stefan       #
# #     Militaru Mihai-Alexandru    #
# #      Tillinger Marius-Petru     #
# ###################################

# TEST FILES: test1_e_nfa_config_file

from operator import indexOf
import sys
import copy

# Global variables
sigma = []
statesAttrib = []
states = []
transitions = []
transitionDict = {}
queue = []
inputStringList = list(sys.argv[2])
totalEpsilonCount = 0

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
      
      if currentState == oldState and currentState != "None"  and line != '':
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
  global totalEpsilonCount
  for item in transitions:
    if item[1] == "epsilon":
      totalEpsilonCount += 1
    if item[0] in transitionDict:
      transitionDict[item[0]].append([x for x in item[1:]])
    else:
      transitionDict[item[0]] = [[item[1], item[2]]]

def getData():
  readConfigFile(getArgs())
  addTransitionsToDict()

# Tests if the NFA accepts the input given
def testAcceptance():
  global inputStringList, transitionDict
  letterCounter = 0
  queue = []

  # Starting node is placed in the queue
  for item in statesAttrib:
    if 'S' in item[1:]:
      queue.append([item[0]])

  # Runs while the queue is not empty and we still
  # have letters in the input given
  while len(queue) and len(inputStringList):
    letterCounter += 1
    newList = []
    firstLetter = inputStringList[0]
    inputStringList = inputStringList[1:]

    # For each item in the queue, we check the
    # possible directions in which the last element can go
    # If the edge is accesible, we append it to the element
    # and placed in the new list
    for queueElement in queue:
      for stateItem in transitionDict[queueElement[-1]]:
        if firstLetter == stateItem[0]:
          tempList = copy.deepcopy(queueElement)
          tempList.append(stateItem[1])
          newList.append(tempList)

      # Each itteration, the elements that don't 
      # respect the minimum length are removed
      # The queue is updated with the remaining elements
      queue = [x for x in newList if len(x) == letterCounter + 1]
    
  # For each element in the queue we verify if the last item
  # has the attribute F. If this condition is met, the NFA
  # accepts this input.
  queue = [x for x in newList if len(x) == letterCounter + 1]
  for queueElement in queue:
    for stateElement in statesAttrib:
      if queueElement[-1] == stateElement[0] and 'F' in stateElement[1:]:
        print(f"ENFA accepts {sys.argv[2]} as input.")
        print(f"Road: {queueElement}")
        exit(0)
  
  print(f"ENFA doesn't accept {sys.argv[2]} as input.")
    
def convertENFAtoNFA():
  global totalEpsilonCount
  while totalEpsilonCount:
    for transition in transitions:
      if transition[1] == "epsilon":
        for item in transitionDict[transition[2]]:
          if item not in transitionDict[transition[0]]:
            transitionDict[transition[0]].append(item)
        
        if 'S' in statesAttrib[indexOf(states, transition[0])]:
          if 'S' not in statesAttrib[indexOf(states, transition[2])]:
            statesAttrib[indexOf(states, transition[2])].append('S')

        if 'F' in statesAttrib[indexOf(states, transition[0])]:
          if 'F' not in statesAttrib[indexOf(states, transition[2])]:
            statesAttrib[indexOf(states, transition[2])].append('F')

        if 'S' in statesAttrib[indexOf(states, transition[2])]:
          if 'S' not in statesAttrib[indexOf(states, transition[0])]:
            statesAttrib[indexOf(states, transition[0])].append('S')

        if 'F' in statesAttrib[indexOf(states, transition[2])]:
          if 'F' not in statesAttrib[indexOf(states, transition[0])]:
            statesAttrib[indexOf(states, transition[0])].append('F')
        
        transitionDict[transition[0]].remove(['epsilon', transition[2]])
        transitions.remove([transition[0], 'epsilon', transition[2]])

    totalEpsilonCount -= 1

getData()
convertENFAtoNFA()
testAcceptance()

# print(f"Sigma -> {sigma}")
# print(f"States -> {states}")
# print(f"States with attributes -> {statesAttrib}")
# print(f"Transitions -> {transitions}")
# print(f"Transition Dictionary -> {transitionDict}")


