from django.http import HttpResponse
from django.shortcuts import render
import re

def home(req):
    return render(req, 'home.html')

def count(req):
    return render(req, 'count.html')

def result(req):
    inputText = req.GET['text']
    parsedText = re.split(r'\W', inputText)
    wordDict = {}

    for word in parsedText:
        word = word.lower()
        if word not in wordDict:
            wordDict[word] = 1;
        else:
            wordDict[word] += 1;

    sortedList = sorted(wordDict.items(), key=lambda x:x[1])
    sortedList.reverse()
    
    return render(req, 'result.html', {'sortedList': sortedList})
