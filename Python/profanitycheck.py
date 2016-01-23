# from urllib.request import urlopen, Request
# from urllib.parse import quote
import urllib.request
import urllib.parse

def readText():

    #Read text file
    quotes = open("E:\\Udacity\\Python\\text_files\\movie_quotes.txt")
    contents = quotes.read()

    #Close file input stream
    quotes.close()

    #Profanity check
    checkProfanity(contents)


def checkProfanity(textToCheck):
    url = urllib.parse.quote(textToCheck)
    request = urllib.request.Request("http://www.wdyl.com/profanity?q=" + url)
    response = urllib.request.urlopen(request)
    output = response.read()
    response.close()
    if "true" in output.decode('utf-8'):
        print("Profanity Alert!!")
    else:
        print("No profanity detected - Send that email out!")



readText()
