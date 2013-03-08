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
  for sentence in sentences:
    sen = sentence
    # sen = reverseSentence(sentence)
    for i in xrange(len(sen)):
      word = sen[i]
      prevWord = sen[i-1] if i > 0 else ""
      nextWord = sen[i+1] if i < len(sen) - 1 else ""
      newWords.append(word)

  return newWords

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
