# ###################################
# #            GRUPA: 143           #
# #        Besliu Radu-Stefan       #
# #     Militaru Mihai-Alexandru    #
# #      Tillinger Marius-Petru     #
# ###################################

# TEST FILES: test1_dfa_config_file, test2_dfa_config_file

from operator import indexOf
import sys

# Global variables
sigma = []
statesAttrib = []
states = []
transitions = []
transitionDict = {}
mainMatrix = []
adjacencyList = []
mappedItems = []
mappedStates = []
mappedItemsAttrib = []

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

# Get minimized DFA
def getMinDFA():
  global mappedStates
  stateLen = len(states)

  # Initialize matrix
  for i in range(stateLen):
    mainMatrix.append([0 for x in range(stateLen)])
    for j in range(i, stateLen):
      mainMatrix[i][j] = -1

  # Compute matrix values
  for i in range(stateLen):
    for j in range(i):
      if 'F' in statesAttrib[i][1:] and 'F' not in statesAttrib[j][1:] or 'F' in statesAttrib[j][1:] and 'F' not in statesAttrib[i][1:]:
        mainMatrix[i][j] = 1

  # Initialize adjacency list
  for state in states:
    currentItem = []
    for letter in sigma:
      if state in transitionDict:
        for item in transitionDict[state]:
          if item[0] == letter:
            currentItemIndex = indexOf(states, item[1])
            currentItem.append(currentItemIndex)
    adjacencyList.append(currentItem)

  # Loop while there are changes to the matrix
  while True:
    done = True
    for i in range(stateLen):
      for j in range(i):
        if mainMatrix[i][j] == 0:
          for k in range(len(sigma)):
            a = adjacencyList[i][k]
            b = adjacencyList[j][k]
            if a < b:
              aux = a
              a = b
              b = aux
            if mainMatrix[a][b] == 1:
              mainMatrix[i][j] = 1
              done = False
              break
    if done:
      break
  
  # Combine states
  for i in range(stateLen):
    for j in range(i):
      if mainMatrix[i][j] == 0:
        tempLen = len(mappedItems)
        for k in range(tempLen):
          splitItem = mappedItems[k].split("--")
          if states[i] in splitItem or states[j] in splitItem:

            splitItem.append(states[i])
            splitItem.append(states[j])

            splitItem = sorted(set(splitItem))
            mappedItems[k] = "--".join(splitItem)
            break
        else:
          mappedItems.append("--".join(sorted([states[i], states[j]])))
  
  # Create mapped states array, made from all combined states
  for item in mappedItems:
    tempItem = item.split('--')
    mappedStates.extend(tempItem)
  mappedStates = [*set(mappedStates)]
  for item in states:
    if item not in mappedStates:
      mappedItems.append(item)

  # Add attributes to mapped items
  for item in mappedItems:
    splitItem = item.split("--")
    itemToAdd = [item]
    for item2 in splitItem:
      for item3 in statesAttrib:
        if item2 == item3[0] and 'F' in item3[1:] and 'F' not in itemToAdd[1:]:
          itemToAdd.append('F')
        if item2 == item3[0] and 'S' in item3[1:] and 'S' not in itemToAdd[1:]:
          itemToAdd.append('S')

    if len(itemToAdd) == 1:
      itemToAdd = itemToAdd[0]
    mappedItemsAttrib.append(itemToAdd)

def printDFA():
  print("Sigma:")
  for letter in sigma:
    print(f"  {letter}")
  print("End")

  print("States:")
  for key in mappedItems:
    if [key, 'S', 'F'] in mappedItemsAttrib or [key, 'F', 'S'] in mappedItemsAttrib:
      print(f"  {key}, S, F")
    elif [key, 'S'] in mappedItemsAttrib:
      print(f"  {key}, S")
    else:
      if key in mappedItems:
        for el in mappedItemsAttrib:
          if el[0] == key and 'F' in el[1:]:
            print(f"  {key}, F")
            break
        else:
          print(f"  {key}")
  print("End")

  print("Transitions:")
  for state in mappedItems:
    firstState = state.split("--")[0]
    itemIndex = indexOf(states, firstState)
    for i in range(len(sigma)):
      print(f"{state}, {sigma[i]}, ", end="")
      item = states[adjacencyList[itemIndex][i]]
      for state2 in mappedItems:
        if item in state2.split("--"):
          print(state2)
          break
  print("End")

getData()
getMinDFA()
printDFA()

# print(f"Sigma -> {sigma}")
# print(f"States -> {states}")
# print(f"States with attributes -> {statesAttrib}")
# print(f"Transitions -> {transitions}")
# print(f"Transition Dictionary -> {transitionDict}")
# print(f"Matrix -> {mainMatrix}")
# print(f"Adjacency list -> {adjacencyList}")
# print(f"Mapped items -> {mappedItems}")
# print(f"Mapped items attributes -> {mappedItemsAttrib}")
# print(f"Mapped states -> {mappedStates}")