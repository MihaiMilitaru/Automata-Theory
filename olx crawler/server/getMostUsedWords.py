f = open("items3.txt", encoding="utf-8")
g = open("most_used_words.txt", "w", encoding="utf-8")
wordDict = {}

for line in f:
  line = line.strip().split()
  for word in line:
    wordDict[word] = wordDict.get(word, 0) + 1

wordDict = dict(sorted(wordDict.items(), key=lambda item: -item[1]))

for key in wordDict:
  stringToWrite = f"{key} : {str(wordDict[key])}\n"
  g.write(stringToWrite)