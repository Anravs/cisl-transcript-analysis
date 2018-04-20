import nltk
import string
import re
from nltk import ngrams
#nltk.download('punkt')

from collections import Counter
 
non_speaker = re.compile('[A-Za-z]+: (.*)')
 
def extract_phrases(text, phrase_counter, length):
    for sent in nltk.sent_tokenize(text):
        strip_speaker = non_speaker.match(sent)
        if strip_speaker is not None:
            sent = strip_speaker.group(1)
        words = nltk.word_tokenize(sent)
        for phrase in ngrams(words, length):
            if all(word not in string.punctuation for word in phrase):
                phrase_counter[phrase] += 1
 
phrase_counter = Counter()


fileR = open("questionsdata1out.txt","r")
n = 2 #n of 3 seems to be a good value since after 3 words the sentence seems to shift from general words to more contextually driven words (e.g. "what is the 'name'", 'what is the 'date'", etc.)
for question in fileR:
    extract_phrases(question, phrase_counter, n )

 
most_common_phrases = phrase_counter.most_common(50)
for k,v in most_common_phrases:
    print('{0: <5}'.format(v), k)