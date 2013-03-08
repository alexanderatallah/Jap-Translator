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
  sentences = getSentences(words)
  newWords = []
  for sentence in sentences:

    for i in xrange(len(sentence)):
      word = sentence[i]
      prevWord = sentence[i-1] if i > 0 else ""
      nextWord = sentence[i+1] if i < len(sentence) - 1 else ""
      newWords.append(word)

  return newWords

def getSentences(words):
  sentences = []
  sentence = []
  for word in words:
    sentence.append(word)
    if word == ".":
      sentences.append(sentence[:])
      sentence = []
  return sentences

def printEnglish(words, partsOfSpeech, printPOS = False):
  output = ""
  for i in xrange(len(words)):
    word = words[i]
    ######### COMMENT THIS OUT TO GET ACTUAL TRANSLATION ###########
    ######### DEBUG MODE ###########
    if printPOS:
      word += ":" + partsOfSpeech[word]
    ######### END ############
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
  reorder(english, p)
  printEnglish(english, p, printPOS)

if __name__ == '__main__':
  main()
  sys.exit(0)
