import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features

fileR = open("longtest.txt","r")

lines = fileR.read()
splitLines = lines.split("\n")
length = len(splitLines)
print(length)

fileR.close()


fileR = open("longtest.txt","r")

fileW = open("output.txt","w")

possibleQuestions = ['what are', 'can you','what is','do you','how about', 'who is', 'when is', 'when was', 'where is', 'where was', 'where were', 'who were', 'why is', 'why were', 'how are', 'how is', 'how were']

dialogue = ""

counter = 1
 
questions = dict()
concepts = dict()
keywords = dict()
categories = dict()

currConcepts = []
currKeywords = []
currCategories = []

prevConcepts = []
prevKeywords = []
prevCategories = []

lineCount = 50


#Overall looks to group sentences into aomunt of #line_count
#With each grouping, throws it into the Bluemix API and looks to see the entities that have been found
 
for line in fileR:
    dialogue +=  line + " "

    #Keep a list of all the questions asked
    for q in possibleQuestions:
        if q in line.lower():
            questionToInsert = line.rstrip()
            questions[questionToInsert] = counter
            break
    
    #When the end of the grouping has been reached, run the APIs
    if(counter % lineCount == 0):  
        natural_language_understanding = NaturalLanguageUnderstandingV1(
          username="445dc0ab-860e-47bd-8015-19da8176e54e",
          password="gI5SZvY3rN5a",
          version="2017-02-27")
        
        
        response = natural_language_understanding.analyze(
          text = dialogue,
          features=[
            Features.Concepts(),
            #Features.Keywords(),
            Features.Categories()
          ]
        )
        
        currConcepts = []
        currKeywords = []
        currCategories = []
        for concept in response['concepts']:
            if(concept['text'] not in concepts):
                currConcepts.append(concept['text'])
                concepts[concept['text']] = [counter]
            else:
                concepts[concept['text']].append(counter)
        
        '''for keyword in response['keywords']:
            if(keyword['text'] not in keywords):
                currKeywords.append(keyword['text'])
                keywords[keyword['text']] = [counter]
            else:
                keywords[keyword['text']].append(counter)'''
        
        for category in response['categories']:
            if(category['label'] not in categories):
                currCategories.append(category['label'])
                categories[category['label']] = [counter]
            else:
                categories[category['label']].append(counter)
        
        #Print out current information
        print('Current Count is: ')
        print(counter)
        print("Concept are:")
        print(concepts)
        print('\nDifference since last iteration is:')
        print(list(set(currConcepts) - set(prevConcepts)))
        
        '''
        print("Keywords are:")
        print(keywords)
        print('\nDifference since last iteration is:')
        print(list(set(currKeywords) - set(prevKeywords)))
        '''
        
        print("\nCategories are:")
        print(categories)
        print('\nDifference since last iteration is:')
        print(list(set(currCategories) - set(prevCategories)))
        
        prevConcepts = currConcepts        
        prevKeywords = currKeywords
        prevCategories = currCategories
        print('\n\n')
        
        dialogue = ""
        
    counter += 1

#Print out the final infomation summary
print("INFORMATION SUMMARY:\n")
print("All Questions are: ")
print(questions)
fileW.write(json.dumps(questions, indent=2))
fileW.write("\n")
print("--")

print("All Concepts are: ")
print(concepts.keys())
fileW.write(json.dumps(concepts, indent=2))
fileW.write("\n")
print("--")

'''
print("All Keywords are: ")
print(keywords.keys())
fileW.write(json.dumps(keywords, indent=2))
fileW.write("\n")
print("--")
'''
print("All Categories are: ")
print(categories.keys())
fileW.write(json.dumps(categories, indent=2))
fileW.write("\n")

fileR.close()
fileW.close()  