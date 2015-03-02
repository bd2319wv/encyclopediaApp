__author__ = 'Jesse'
from tkinter import *
import webbrowser
import urllib.request
import urllib.parse
import re
from flickrapi import *
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

############flickrApiSetup###########
flKey = '13c592d3851810c8f1a97ed2bd38af90'
flSecret = 'c3e96f35fe4ef875'
'''
Info for flicker API documentation:
https://code.google.com/p/python-flickr-api/wiki/Tutorial
http://www.janeriksolem.net/2009/02/using-python-to-download-images-from.html
'''

############### Streaming Tweets ######################
cKey = 'xLwpqmwpQLNfkKI5Ux5eHSRAP'
cSecret = '56HR60btiSEjc03GO3Xm0i5VQSVOb9Xs5XQQZi2COQoxhjkqJE'
aToken = '1187764111-LK8d4jwuumvY5XVFx5GKeHSQVcUxJsiEJoE1pMS'
aSecret = 'o30rmM7frd8OONtU2QPZGTsw7s8KmGHEpdFYtEKsfJWjw'

#userSearch = str(input("Enter search criteria: "))

class Listener(StreamListener):

    def __init__(self, api=None):
        super(Listener, self).__init__()
        self.numTweets = 0
        #self.tweetArray = []
        saveFile2 = open('tDB3.csv', 'w')
        saveFile2.close()

    def on_data(self, raw_data):

        try:
            #Sets tweet array and splits the data at text to the source, and then while numTweets is less than 10
            #Adds tweets to array
            self.tweetArray = []
            tweet = raw_data.split(',"text":"')[1].split('","source')[0]
            #print(tweet)
            self.numTweets += 1
            if(self.numTweets < 11):
                self.tweetArray.append(tweet)
                print(self.tweetArray)
                saveFile2 = open('tDB3.csv', 'a')
                saveThisTweet = tweet
                saveFile2.write(saveThisTweet)
                saveFile2.write('\n')
                saveFile2.close()
                return True
            else:
                return False






        except:
            print("Failed")




    #Prints status of error if error occurs
    def on_error(self, status_code):
        print(status_code)

#Sets consumer keys and access tokens
authorize = OAuthHandler(cKey, cSecret)
authorize.set_access_token(aToken, aSecret)

#Streams the tweets using the Listener class and depending on the criteria of the userSearch
#twitterStream = Stream(authorize, Listener())
#twitterStream.filter(track=[userSearch])


class Main:

    def __init__(self, master):


        #Creates userSearch Variable for storing user input
        self.userSearch = StringVar()

        #sets window to master, sets title, and window size
        self.master = master
        self.master.title("Encyclopedia App")
        self.master.geometry("500x430")

        #Creates labels, buttons, and textbox
        lblTitle = Label(self.master, text="Searchster", font=("Times 16 bold"), fg="green", )
        lblSearch = Label(self.master, text="Search: ", font=("Times 10"))
        txtBoxSearch = Entry(self.master, width=17, textvariable=self.userSearch)
        btnSearch = Button(self.master, text="Search", width=14, command=self.search)
        btnQuit = Button(self.master, text="Close", width=14, command=self.close)
        lblWikiLabel = Label(self.master, text="           Wikipedia URL", font=("Times 10 bold"))
        lblFlickrLabel = Label(self.master, text="            Flickr URL", font=("Times 10 bold"))
        lblTwitterLabel = Label(self.master, text="          Twitter URL", font=("Times 10 bold"))

        #Initialize the URL Labels and set there position in the grid
        self.lblDisplayWikiURL = Label(self.master, text=" ")
        self.lblDisplayWikiURL.grid(row=2, column=4, sticky=W)
        self.lblDisplayFlickrURL = Label(self.master, text=" ")
        self.lblDisplayFlickrURL.grid(row=4, column=4, sticky=W)
        self.lblDisplayTwitterURL = Label(self.master, text=" ")
        self.lblDisplayTwitterURL.grid(row=8, column=4, sticky=W)

        #Places labels, buttons, and textbox in grid format
        lblTitle.grid(row=1, column=2)
        lblSearch.grid(row=2, column=1, sticky=E)
        txtBoxSearch.grid(row=2, column=2)
        btnSearch.grid(row=3, column=2)
        btnQuit.grid(row=4, column=2)
        lblWikiLabel.grid(row=1, column=4, sticky=W)
        lblFlickrLabel.grid(row=3, column=4, sticky=W)
        lblTwitterLabel.grid(row=7, column=4, sticky=W)


    #Wikipedia Callback Event
    def wikicallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://en.wikipedia.org/w/index.php?title=" + str(userSearch))

    #Flickr Callback Event
    def flickrcallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://www.flickr.com/search/?q=" + str(userSearch))

    #Twitter Callback Event
    def twittercallback(self, event):
        userSearch = self.userSearch.get()
        #Opens the hyperlink when left-clicked on
        webbrowser.open("http://twitter.com/search?q=" + str(userSearch) + "&src=typd")




    #Search Function
    def search(self):

        #Streams the tweets using the Listener class and depending on the criteria of the userSearch
        twitterStream = Stream(authorize, Listener())


        #Gets text from search textbox
        userSearch = self.userSearch.get()
        twitterStream.filter(track=[userSearch])
        #tweetArray = Listener.tweetArray
        #Searching and pulling flickr##############
        #Creates flickr array
        flickrArray = []

        #Creates variable for flickr URL and stores the value to be searched in FLickr
        flickrUrl = "http://www.flickr.com/search/?q=" + str(userSearch)
        flickrValues = {'s': userSearch}

        #Encodes the data (Converts to bytes for searching)
        flickrData = urllib.parse.urlencode(flickrValues)
        flickrData = flickrData.encode('utf-8')

        #Requests the data from the url and the response opens that url to search
        flickrRequest = urllib.request.Request(flickrUrl, flickrData)
        flickrResponse = urllib.request.urlopen(flickrRequest)

        #Reads and stores the data
        flickrRespData = flickrResponse.read()

        #Search for matching criteria within the respData
        flickrREGEX = re.findall((userSearch), str(flickrRespData))

        #Creates array and stores each matching item in that array

        for eachFlickrItem in flickrREGEX:
            if(len(flickrArray)>5):
                break
            else:
                flickrArray.append(eachFlickrItem + "\n")



        #Opens the webbrowsers
        webbrowser.open("http://en.wikipedia.org/w/index.php?title=" + str(userSearch))
        webbrowser.open("http://www.flickr.com/search/?q=" + str(userSearch))
        webbrowser.open("http://twitter.com/search?q=" + str(userSearch) + "&src=typd")

        #Displays Wikipedia hyperlink in label and binds it to left-click event and places in grid
        self.lblDisplayWikiURL.config(text="http://en.wikipedia.org/w/index.php?title=" + str(userSearch), fg="Blue", cursor="hand2")
        self.lblDisplayWikiURL.bind('<Button-1>', self.wikicallback)

        '''I'll leave the original format for the URL's in here in case anybody need it or we have to change back'''
        #lblDisplayWikiURL = Label(self.master, text="http://en.wikipedia.org/w/index.php?title=" + str(userSearch), fg="Blue", cursor="hand2")
        #lblDisplayWikiURL.bind('<Button-1>', self.wikicallback)
        #lblDisplayWikiURL.grid(row=2, column=4, sticky=W)
        #lblDisplayFlickrURL = Label(self.master, text="http://www.flickr.com/search/?q=" + str(userSearch), fg="Blue", cursor="hand2")
        #lblDisplayFlickrURL.bind('<Button-1>', self.flickrcallback)
        #lblDisplayFlickrURL.grid(row=4, column=4, sticky=W)
        #lblDisplayTwitterURL = Label(self.master, text="http://twitter.com/search?q=" + str(userSearch) + "&src=typd", fg="Blue", cursor="hand2")
        #lblDisplayTwitterURL.bind('<Button-1>', self.twittercallback)
        #lblDisplayTwitterURL.grid(row=8, column=4, sticky=W)


        #Displays Flickr hyperlink in label and binds it to left-click event and places in grid
        self.lblDisplayFlickrURL.config(text="http://www.flickr.com/search/?q=" + str(userSearch), fg="Blue", cursor="hand2")
        self.lblDisplayFlickrURL.bind('<Button-1>', self.flickrcallback)
        lblDisplayFlickrData = Label(self.master, text=flickrArray)
        lblDisplayFlickrData.grid(row=6, column=4, sticky=W)

        #Opens the tDB3 file and reads for displayingin the lblDisplayTwitterData below, and then closes it
        saveFile2 = open('tDB3.csv', 'r')
        readFile = saveFile2.read()
        saveFile2.close()

        #Displays Twitter hyperlink in label and binds it to left-click event and places in grid
        self.lblDisplayTwitterURL.config(text="http://twitter.com/search?q=" + str(userSearch) + "&src=typd", fg="Blue", cursor="hand2")
        self.lblDisplayTwitterURL.bind('<Button-1>', self.twittercallback)
        lblDisplayTwitterData = Label(self.master, text=readFile)
        lblDisplayTwitterData.grid(row=9, column=4, sticky=W)

    #Function for closing the window
    def close(self):
        self.master.destroy()


#Creates the root window and loops it
def main():
    root = Tk()
    Main(root)
    root.mainloop()

#Loops the code so the windows stay open
if __name__ == "__main__":
    main()




