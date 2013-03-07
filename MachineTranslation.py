import sys, collections

def initDicts(f):
  d = {}
  partsOfSpeech = {"": None}
  for line in f:
    (f, e, part) = line.strip().split('|')
    d[f] = e
    partsOfSpeech[e] = part
  return (d, partsOfSpeech)

def reorder(words, partsOfSpeech):
  newWords = []
  for i in xrange(len(words)):
    word = words[i]
    prevWord = words[i-1] if i > 0 else ""
    nextWord = words[i+1] if i < len(words) - 1 else ""

  return newWords

def printEnglish(words, partsOfSpeech):
  output = ""
  for i in xrange(len(words)):
    word = words[i]
    prevWord = words[i-1] if i > 0 else ""
    if prevWord == "." or prevWord == "":
      word = word[0].upper() + word[1:]

    if prevWord == "" or word == "'s" or \
      (word in partsOfSpeech and partsOfSpeech[word] == "PN"):
      output += word
    else: output += " " + word

  print output

def main():
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
  printEnglish(english, p)

if __name__ == '__main__':
  main()
  sys.exit(0)
