import sys, collections, getopt

VOWELS = ["a", "e", "i", "o", "u"]

def initDicts(f):
  d = {}
  partsOfSpeech = {"": None}
  for line in f:
    (f, e, part) = line.strip().split('|')
    d[f] = e
    partsOfSpeech[e] = part
  return (d, partsOfSpeech)

def reorder(words, partsOfSpeech):
  partsOfSpeech["is"] = "VB"
  partsOfSpeech["a"] = partsOfSpeech["an"] = "RP"
  partsOfSpeech["when"] = "RP"
  partsOfSpeech["then"] = "RP"

  sentences = listSplit(words, ".", True)
  newWords = []
  for sen in sentences:
    i = 0
    while(i < len(sen)):
      # Switch any instance of NN, RP to RP, NN, except when RP is "of".
      if partsOfSpeech[sen[i]] == "NN" and partsOfSpeech[nextWord(i, sen)] == "RP" and nextWord(i, sen) != "and":
        sen[i], sen[i+1] = sen[i+1], sen[i]

      # Look for the existence of "of" and switch the nouns on either side of the "of".
      if sen[i] == "of" and partsOfSpeech[nextWord(i, sen)] == "NN" and partsOfSpeech[nextWord(i+1, sen)] == "NN":
        sen[i], sen[i+1], sen[i+2] = sen[i+2], sen[i], sen[i+1]

      # Look for the existence of "but": if it comes after a noun or noun phrase, change it to "the".
      if sen[i] == "but" and partsOfSpeech[nextWord(i, sen)] == "NN":
        sen[i] = "the"

      # Look for the existence of "and": if it comes before a verb, change it to "when". If it comes after a verb, change it to "then".
      if sen[i] == "and":
        if partsOfSpeech[prevWord(i, sen)] == "VB":
          sen[i] = "when"
        if partsOfSpeech[nextWord(i, sen)] == "VB":
          sen[i] = "then"

      # Look for the existence of "because". Move it to the beginning of the clause.
      if sen[i] == "because" and partsOfSpeech[nextWord(i, sen)] == "PN":
        moveToClauseStart(i, sen)

      # Look for nouns followed by commas; change these nouns to "is a [noun]"
      if partsOfSpeech[sen[i]] == "NN" and partsOfSpeech[nextWord(i, sen)] == "PN" \
        and partsOfSpeech[(prevWord(i, sen))] not in ["RP", "NN"]:
        # print sen[i-3] + " " + sen[i-2] + " " + sen[i-1] + " " + sen[i] + " " + sen[i+1]
        sen.insert(i, "an") if nextWord(i, sen)[0].lower() in VOWELS else sen.insert(i, "a")
        sen.insert(i, "is")
        i += 2

      # Switch nouns or adjectives followed by verbs to verbs followed by nouns or adjectives.
      if partsOfSpeech[sen[i]] == "VB" and partsOfSpeech[prevWord(i, sen)] in ["JJ", "NN"] \
        and partsOfSpeech[prevWord(i-1, sen)] == "RP" and partsOfSpeech[prevWord(i-2, sen)] == "NN":
        # print sen[i-3] + " " + sen[i-2] + " " + sen[i-1] + " " + sen[i]
        moveWord(i, i-3, sen)

      # If a verb is preceded by an adjective and before that a noun, place it before the adjective
      if partsOfSpeech[sen[i]] == "VB" and partsOfSpeech[prevWord(i, sen)] == "JJ" \
        and partsOfSpeech[nextWord(i, sen)] == "PN":
        moveWord(i, i-1, sen)

      # If an adjective is followed by a particle and a noun, then delete the particle
      if partsOfSpeech[sen[i]] == "JJ" and partsOfSpeech[nextWord(i, sen)] == "RP" \
        and partsOfSpeech[(nextWord(i+1, sen))] == "NN":
        print sen[i+1]
        sen.pop(i+1)

      i+=1
    newWords += sen

  return newWords

def prevWord(i, sen):
  return sen[i-1] if i > 0 else ""

def nextWord(i, sen):
  return sen[i+1] if i < len(sen) - 1 else ""

def moveWord(idxSource, idxDest, lista):
  source = lista.pop(idxSource)
  lista.insert(idxDest, source)

def moveToClauseStart(idxSource, sentence):
  idxDest = idxSource
  while (idxDest > 0 and sentence[idxDest - 1] != ","):
    idxDest -= 1
  moveWord(idxSource, idxDest, sentence)

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
