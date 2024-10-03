##############################################################
# created by: Deborah Sanchez
# email: debsanchez.business@outlook.com
# date: 9-27-2024
# desc: This sample Python project uses all of the techniques
# you learned in weeks 1-4 and combines them into a fully 
# functioning scary movie recommendation generator application.
# This project is week 5 of a 5 week project which can be 
# downloaded at https://github.com/crickidie.
##############################################################

import os
import sys
import time
import random
import requests

from html.parser import HTMLParser
from ascii_magic import AsciiArt as am
from threading import Thread, Event

imdbMoveUrl     = 'https://www.imdb.com'
imdbListYears   = ['85','86','87','88','89','90','91','92','93','94','95']
imdbKeywordUrl  = '/search/title/?title_type=feature&release_date=19XX-01-01,19XX-12-31&genres=horror&keywords=WWWW'
imdbListUrl     ='/search/title/?title_type=feature&release_date=19XX-01-01,19XX-12-31&genres=horror'

class WaitCls(Thread):
    def __init__(self):
         super(WaitCls, self).__init__()
         self._stopevent = Event()

    def run(self):
        self._stopevent.clear()

        while not self._stopevent.is_set():
            for i in [1,2,3]:
                print(".", end='')
                sys.stdout.flush()
                time.sleep(.75)

            print('\b\b\b', end='')
            print('   ', end='')
            print('\b\b\b', end='')
            sys.stdout.flush()
            time.sleep(.75)

    def join(self, timeout=None):
        self._stopevent.set()
        Thread.join(self, timeout)

class ImageCls(HTMLParser):
    img = False

    def handle_starttag(self, tag, attrs):
        if (tag != 'img' or attrs.count == 0):
            return

        for i in attrs:
            if (i[0] == 'src' and i[1].endswith('.jpg') and self.img == False):
                self.save_image(i[1])
                self.img = True

    def save_image(self, image_path):
        file = open(r"image_file.jpg", "wb")
        file.write(requests.get(image_path).content)
        file.close()

    def convert_image_to_ascii(self) -> str:
        aa = am.from_image("image_file.jpg")
        aa.to_terminal(columns=100)

class MovieCls(HTMLParser):
    inTagTitle  = False
    inTagYear   = False
    inTagSynop  = False
    inTagImg    = False
    Title       = ''
    ImageUrl    = ''
    Year        = ''
    Synopsis    = ''

    def handle_starttag(self, tag, attrs):
        if ((tag != 'span' and tag != 'a') or attrs.count == 0):
            return

        for s in attrs:

            # title and synopsis
            if (tag == 'span'):
                if (s[0] == 'class' and s[1] == 'hero__primary-text'):
                    self.inTagTitle = True
                elif (s[0] == 'class' and s[1] == 'sc-9579cce5-2 fbJbRX'):
                    self.inTagSynop = True

            # year and image
            elif(tag == 'a'):
                if (s[0] == 'class' and s[1] == 'ipc-link ipc-link--baseAlt ipc-link--inherit-color'):
                    self.inTagYear = True
                elif (s[0] == 'class' and s[1] == 'ipc-lockup-overlay ipc-focusable' and len(self.ImageUrl) == 0):
                    self.inTagImg = True
                elif (s[0] == 'href' and s[1].startswith('/title/') and self.inTagImg):
                    self.ImageUrl = s[1]

    def handle_endtag(self, tag):
        if (tag == 'span' and self.inTagTitle):
            self.inTagTitle = False
        elif (tag == 'a' and self.inTagYear):
            self.inTagYear = False
        elif (tag == 'span' and self.inTagSynop):
            self.inTagSynop = False
        elif (tag == 'a' and self.inTagImg):
            self.inTagImg = False

    def handle_data(self, data):
        if (self.inTagTitle):
            self.Title = data
        elif (self.inTagYear and data.isdigit()):
            self.Year = data
        elif (self.inTagSynop):
            self.Synopsis = data

class MovieListCls(HTMLParser):
    urlArray       = []

    def handle_starttag(self, tag, attrs):
        if (tag != 'a' or attrs.count == 0):
            return

        href = ''
        for a in attrs:

            if (a[0] == 'href' and a[1].startswith('/title/')):
                href = a[1]

            if (a[1] == 'ipc-title-link-wrapper'):
                self.urlArray.append(href)

def wait():
    time.sleep(.75)

def working() -> WaitCls:
    w = WaitCls()
    w.start()
    return w

# this defintion generates the title and description of the application
def generate_title():
    os.system('cls')
    print("  ██████  ▄████▄   ▄▄▄       ██▀███ ▓██   ██▓    ███▄ ▄███▓ ▒█████   ██▒   █▓ ██▓▓█████   ██████ ")
    print("▒██    ▒ ▒██▀ ▀█  ▒████▄    ▓██ ▒ ██▒▒██  ██▒   ▓██▒▀█▀ ██▒▒██▒  ██▒▓██░   █▒▓██▒▓█   ▀ ▒██    ▒ ")
    print("░ ▓██▄   ▒▓█    ▄ ▒██  ▀█▄  ▓██ ░▄█ ▒ ▒██ ██░   ▓██    ▓██░▒██░  ██▒ ▓██  █▒░▒██▒▒███   ░ ▓██▄   ")
    print("▒██████▒▒▒ ▓███▀ ░ ▓█   ▓██▒░██▓ ▒██▒ ░ ██▒▓░   ▒██▒   ░██▒░ ████▓▒░   ▒▀█░  ░██░░▒████▒▒██████▒▒")
    print("▒ ▒▓▒ ▒ ░░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░  ██▒▒▒    ░ ▒░   ░  ░░ ▒░▒░▒░    ░ ▐░  ░▓  ░░ ▒░ ░▒ ▒▓▒ ▒ ░")
    print("░ ░▒  ░ ░  ░  ▒     ▒   ▒▒ ░  ░▒ ░ ▒░▓██ ░▒░    ░  ░      ░  ░ ▒ ▒░    ░ ░░   ▒ ░ ░ ░  ░░ ░▒  ░ ░")
    print("░  ░  ░  ░          ░   ▒     ░░   ░ ▒ ▒ ░░     ░      ░   ░ ░ ░ ▒       ░░   ▒ ░   ░   ░  ░  ░  ")
    print("         ░                           ░ ░                                 ░                       ")
    print("\n")

def generate_sub_title():
    wait()
    print("---------------------------------------------")
    print("| Welcome to the Halloween movie generator! |")
    wait()
    print("|                                           |")
    print("| Using some basic input, I can suggest a   |")
    print("| random Halloween movie that you can watch |")
    print("| this holiday season. Choose one of the    |")
    print("| options below to get started.             |")
    print("---------------------------------------------")
    print("\n")

# this definition captures the user input
def get_user_selection() -> str:

    print("Enter '1' to generate a random movie suggestion.")
    wait()
    print("Enter '2' to generate a random movie based on keywords that you provide.")
    wait()
    print("\n")

    i = 0

    while True:
        i = input("Type 1 or 2 and press enter: ")

        if i == '1' or i == '2':
            break
        else:
            print(i, "is not a valid selection. Try again.")

    return i

# this definition captures the user keywords
def get_user_keywords() -> list[str]:
    wait()
    print("---------------------------------------------")
    print("| Type a keyword and press Enter            |")
    print("| When you're done, press Enter with no     |")
    print("| keyword to continue.                      |")
    print("---------------------------------------------")

    rtn = []
    while True:
        s = input("Keyword: ")
        if (len(s.strip()) > 0):
            rtn.append(s)
        else:
            break

    if (len(rtn) == 0):
        print("At least one keyword is required.")
        rtn = get_user_keywords()

    return rtn

# this definition retrieves the html for a url
def get_html(url):
    rsp = requests.get(url=url, headers={'User-Agent': 'Mozilla/5.0'})

    if (rsp.status_code == 200):
        return rsp.text
    else:
        print("The request failed.")

# this definition parses the html to return the movie list
def parse_html_to_list(html) -> list[str]:

    mlc = MovieListCls()

    mlc.feed(html)

    return mlc.urlArray

# this definition returns a movie
def parse_html_to_movie(html) -> MovieCls:
    mc = MovieCls()
    
    mc.feed(html)

    return mc

# this definition return a image
def parse_html_to_image(html) -> ImageCls:
    ic = ImageCls()

    ic.feed(html)

    return ic

# this definition converts an image to ascii
def get_random_movie(urlArray) -> str:
    return urlArray[random.randint(0, len(urlArray) -1)]

# this definition converts the list of stirngs into a single string
def convert_string_array_to_string(strings: list[str]) -> str:
    rtn = ''

    # check required
    if (len(strings) == 0):
        print("We can't search for a movie by keywords without at least one keyword.")
        strings = get_user_keywords()

    # if only one item just return it
    if (len(strings) == 1):
        return strings[0]

    # if multipe, loop and convert
    for str in strings:
        rtn += str + ','

    return rtn[0:(len(rtn) - 1)]

# this definition displays the movie data on the screen
def display_movie(movie: MovieCls, image: ImageCls):
    print("Title   :", movie.Title)
    print("Year    :", movie.Year)
    print("Synopsis:", movie.Synopsis)
    print("\n")
    image.convert_image_to_ascii()
    print('\n')

# this is the main definition that runs the application
def main():

    # display title
    generate_title()
    generate_sub_title()

    # cpature user choice
    i = get_user_selection()

    # generate movie list
    urlArray = []
    if (i == '1'):

        generate_title()

        print('please wait while we pick a movie for you', end='')
        w = working()
        
        for year in imdbListYears:
            html = get_html(imdbMoveUrl + imdbListUrl.replace("XX", year))
            urlArray = parse_html_to_list(html)

        # stop background process
        w.join()

    # generate movie list with keywords
    else:
        generate_title()

        keywords = get_user_keywords()

        generate_title()

        print('please wait while we pick a movie for you', end='')
        w = working()

        for year in imdbListYears:
            html = get_html(imdbMoveUrl + imdbKeywordUrl.replace("XX", year).replace("WWWW", convert_string_array_to_string(keywords)))
            urlArray = parse_html_to_list(html)

        # stop background process
        w.join()

    if (len(urlArray) == 0):
        generate_title()

        print("We couldn't find any movies to return.")
        print("The program will now exit.")
        print("Run the program again using different criteria.")
        exit()

    # pick random move from list
    url = get_random_movie(urlArray)

    # get the html for the movie
    html = get_html(imdbMoveUrl + url)

    # parse the movie html into a movie
    movie = parse_html_to_movie(html)

    # get html for image
    html = get_html(imdbMoveUrl + movie.ImageUrl)

    # parse html
    image = parse_html_to_image(html) 

    generate_title()

    # display the movie
    display_movie(movie, image)

    input("Press enter to exit.")

# run main
if __name__ == "__main__":
    main()
