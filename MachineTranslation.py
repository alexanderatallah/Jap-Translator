import sys, collections, getopt

def initDicts(f):
  d = {}
  partsOfSpeech = {"": None}
  for line in f:
    (f, e, part) = line.strip().split('|')
    d[f] = e
    partsOfSpeech[e] = part
  return (d, partsOfSpeech)

def reorder(words, partsOfSpeech):
  sentences = listSplit(words, ".", True)
  newWords = []
  for sen in sentences:
    i = 0
    while(i < len(sen)):
      if partsOfSpeech[sen[i]] == "NN" and partsOfSpeech[nextWord(i, sen)] == "RP" and nextWord(i, sen) != "and":
        sen[i], sen[i+1] = sen[i+1], sen[i]

      if sen[i] == "of" and partsOfSpeech[nextWord(i, sen)] == "NN" and partsOfSpeech[nextNextWord(i, sen)] == "NN":
        sen[i], sen[i+1], sen[i+2] = sen[i+2], sen[i], sen[i+1]

      if sen[i] == "but" and partsOfSpeech[nextWord(i, sen)] == "NN":
        sen[i] = "the"

      if sen[i] == "and":
        if partsOfSpeech[prevWord(i, sen)] == "VB":
          sen[i] = "then"
        if partsOfSpeech[nextWord(i, sen)] == "VB":
          sen[i] = "when"

      if sen[i] == "because" and partsOfSpeech[nextWord(i, sen)] == "PN":
        moveToClauseStart(i, sen)

      i+=1
    newWords += sen

  return newWords

def prevWord(i, sen):
  return sen[i-1] if i > 0 else ""

def nextWord(i, sen):
  return sen[i+1] if i < len(sen) - 1 else ""

def nextNextWord(i, sen):
  return sen[i+2] if i < len(sen) - 2 else ""

def moveWord(idxDest, idxSource, lista):
  source = lista.pop(idxSource)
  lista.insert(idxDest, source)

def moveToClauseStart(idxSource, sentence):
  idxDest = idxSource
  while (idxDest > 0 and sentence[idxDest - 1] != ","):
    idxDest -= 1
  moveWord(idxDest, idxSource, sentence)

def reverseSentence(sentence):
  clauses = listSplit(sentence, ",")
  reversedSentence = []
  for clause in clauses:
    if clause[-1] == ".":
      reversedSentence = reversedSentence + clause[-2::-1] + ["."]
    else:
      reversedSentence = reversedSentence + clause[::-1] + [","]
  # import pdb; pdb.set_trace()
  return reversedSentence

def listSplit(lista, splitter, includeSplitter = False):
  superlist = []
  sublist = []
  for item in lista:
    if item == splitter:
      if includeSplitter: sublist.append(item)
      superlist.append(sublist)
      sublist = []
      continue
    sublist.append(item)
  if len(sublist) > 0: superlist.append(sublist)
  return superlist

def printEnglish(words, partsOfSpeech, printPOS = False):
  output = ""
  for i in xrange(len(words)):
    word = words[i]
    if printPOS:
      word += ":" + partsOfSpeech[word]
    prevWord = words[i-1] if i > 0 else ""
    if prevWord == "." or prevWord == "":
      word = word[0].upper() + word[1:]

    if prevWord == "" or word == "'s" or \
      (word in partsOfSpeech and partsOfSpeech[word] == "PN"):
      output += word
    else: output += " " + word

  print output

def main():
  printPOS = False
  (options, args) = getopt.getopt(sys.argv[1:], 't')
  if ('-t','') in options:
    printPOS = True
  
  d, p = initDicts(open("dictionary.txt"))
  japanese = open("japanese_text_segmented.txt")
  english = []
  for line in japanese:
    words = line.split("|")
    for w in words:
      if w in d:
        if d[w]: english.append(d[w])
      else: english.append("NOT_IN_DICT:" + w)
  english = reorder(english, p)
  printEnglish(english, p, printPOS)

if __name__ == '__main__':
  main()
  sys.exit(0)
