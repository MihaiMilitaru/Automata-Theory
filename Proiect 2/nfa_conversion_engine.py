# ###################################
# #            GRUPA: 143           #
# #        Besliu Radu-Stefan       #
# #     Militaru Mihai-Alexandru    #
# #      Tillinger Marius-Petru     #
# ###################################

# TEST FILES: test1_nfa_to_dfa, test2_nfa_to_dfa, test3_nfa_to_dfa

import sys
import copy

# Global variables
sigma = []
statesAttrib = []
states = []
transitions = []
transitionDict = {}
queue = []
visited = []
newTransitionDict = {}
dfaTransitionDict = {}

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
    if item != ['']:
      if item[0] in transitionDict:
        transitionDict[item[0]].append([x for x in item[1:]])
      else:
        transitionDict[item[0]] = [[item[1], item[2]]]

def getData():
  readConfigFile(getArgs())
  addTransitionsToDict()

# Convert NFA to DFA
def convertToDFA():
  queue.clear()

  # Search for start node
  for state in statesAttrib:
    if 'S' in state[1:]:
      queue.append(state[0])

  # Add starting node to visited array
  visited.append(queue[0])

  while len(queue):
    firstElement = queue[0]
    queue.pop(0)

    # For each letter in sigma, we map possible directions
    for letter in sigma:
      mappedItems = []
      if firstElement in newTransitionDict:
        for element in newTransitionDict[firstElement]:
          if element in transitionDict:
            for item in transitionDict[element]:
              if item[0] == letter:
                mappedItems.append(item[1])
      else:
        for item in transitionDict[firstElement]:
          if item[0] == letter:
            mappedItems.append(item[1])

      mappedItems = set(mappedItems)
      mappedItems = sorted(mappedItems)
      # Check if current states selected form a new combination, otherwise
      # add them
      # If there is only one possible direction, skip state combination
      if len(mappedItems) == 1:
        mappedItems = mappedItems[0]
        mappedItemsName = mappedItems
        if mappedItems not in visited:
          visited.append(mappedItems)
          queue.append(mappedItems)

      else:  
        mappedItemsName = ""
        for key in newTransitionDict:
          if newTransitionDict[key] == mappedItems:
            mappedItemsName = key
            break
        else:
          # If the current combination is new, add the direction to the
          # transition dictionary
            mappedItemsName = "--".join(mappedItems)
            if mappedItemsName != "":
              newTransitionDict[mappedItemsName] = mappedItems
            
        if mappedItemsName != "" and mappedItemsName not in visited:
          visited.append(mappedItemsName)
          queue.append(mappedItemsName)

      # Create DFA transition matrix
      if firstElement in dfaTransitionDict:
        dfaTransitionDict[firstElement].append([letter, mappedItemsName])
      else:
        dfaTransitionDict[firstElement] = [[letter, mappedItemsName]]

# Print DFA
def printDFA():
  print("Sigma:")
  for letter in sigma:
    print(f"  {letter}")
  print("End")

  print("States:")
  for key in dfaTransitionDict:
    ok = 0;
    if [key, 'S', 'F'] in statesAttrib or [key, 'F', 'S'] in statesAttrib:
      print(f"  {key}, S, F")
    elif [key, 'S'] in statesAttrib:
      print(f"  {key}, S")
    else:
      if key in states:
        for el in statesAttrib:
          if el[0] == key and 'F' in el[1:]:
            print(f"  {key}, F")
            break
        else:
          print(f"  {key}")
      else:
        for item in newTransitionDict[key]:
          for newEl in statesAttrib:
            if newEl[0] == item and 'F' in newEl[1:]:
              print(f"  {key}, F")
              ok = 1
              break
          if ok:
            break
        else:
          print(f"  {key}")
  print("End")

  print("Transitions:")
  for key in dfaTransitionDict:
    for item in dfaTransitionDict[key]:
      if item[1] == '':
        continue
      print(f"  {key}, ", end="")
      print(f"{item[0]}, {item[1]}")
  print("End")


getData()
convertToDFA()
printDFA()

# print(f"Sigma -> {sigma}")
# print(f"States -> {states}")
# print(f"States with attributes -> {statesAttrib}")
# print(f"Transitions -> {transitions}")
# print(f"Transition Dictionary -> {transitionDict}")
# print(f"New Transition Dictionary -> {newTransitionDict}")

