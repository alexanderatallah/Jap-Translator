import sys, collections

def initDicts(f):
  d = {}
  partsOfSpeech = {}
  for line in f:
    (f, e, pos) = line.split('|')
    d[f] = e
    partsOfSpeech[e] = pos
  return (d, partsOfSpeech)

def reorder(words):
  return words

def main():
  d, p = initDicts(open("dictionary.txt"))
  japanese = open("japanese_text_segmented.txt")
  english = []
  for line in japanese:
    words = line.split("|")
    for w in words:
      if w in d: english.append(d[w])
      else: english.append("NOT_IN_DICT:" + w)
  reorder(english)
  print " ".join(english)

if __name__ == '__main__':
  main()
  sys.exit(0)
