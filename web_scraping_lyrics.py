import requests
import pyperclip
import re
import csv

class Web_Scraping:

    def __init__(self, artist_name, agent):
        self.artist_name = artist_name
        self.agent = agent
        self.all = []
        #pyperclip.copy(html_text)
        
    def get_artist_page(self):
        no_space = ''.join(self.artist_name.split())
        artist_url = f'https://www.azlyrics.com/{self.artist_name[0]}/{no_space}.html'.lower()
        artist_html_text = requests.get(artist_url, headers={'User-Agent': self.agent}).text
        print(artist_html_text)
        return artist_html_text

    def get_song_page(self, song_name):
        no_space = ''.join(song_name.split())
        song_url = f'https://www.azlyrics.com/lyrics/{self.artist_name}/{no_space}.html'.lower()
        song_html_text = requests.get(song_url, headers={'User-Agent': self.agent}).text
        return song_html_text

    def get_song_names(self, html_text):

        pattern = '<div class="listalbum-item">([\s\S]*?)<\/div>'
        elements = re.findall(pattern, html_text)

        elements_commentless = []
        pattern_com = '<div class="comment">([\s\S]*?)\)'
        for e in elements:
            elements_commentless.append(re.sub(pattern_com, '', e))
        
        elements_br = []
        for e in elements_commentless:
            elements_br.append(e.replace('<br/>', '\n '))

        elements_quote1 = []
        for e in elements_br:
            elements_quote1.append(e.replace('&quot;', '"'))

        elements_quote2 = []
        for e in elements_quote1:
            elements_quote2.append(e.replace('&#x27;', "'"))

        elements_as = []
        for e in elements_quote2:
            elements_as.append(e.replace('&amp;', "&"))

        elements_link1 = []
        pattern_link1 = '<([\s\S]*?)>'
        for e in elements_quote2:
            elements_link1.append(re.sub(pattern_link1, '', e))

        elements_link1.pop()
        elements_link1.pop()

        return elements_link1

    def get_lyrics(self, html_text):

        pattern = '<b>([\s\S]*?)<\/div>'
        elements = re.findall(pattern, html_text)

        print(len(elements))

        if len(elements) != 3:
            return ''

        lyrics = elements[1]
        lyrics = lyrics.replace('<br/>', '\n ')
        lyrics = lyrics.replace('&quot;', '"')
        lyrics = lyrics.replace('&#x27;', "'")
        lyrics = lyrics.replace('&amp;', "&")

        pattern_link1 = '<([\s\S]*?)>'
        lyrics = re.sub(pattern_link1, '', lyrics)
        
        return lyrics


    def clean_song_names(self, list_of_songs):
        
        list_no_space = []
        for s in list_of_songs:
            list_no_space.append(''.join(s.split()))

        list_no_specials = []
        for s in list_no_space:
            list_no_specials.append(re.sub('[^A-Za-z0-9]+', '', s))
            
        return list_no_specials


    def print_songs(self, html_text):

        song_names = self.get_song_names(html_text)
        clean_names = self.clean_song_names(song_names)

        for s in clean_names:
            print(s)

        return song_names 


    def print_all_songs(self, list):

        for song in list:
            lyrics_html = self.get_song_page(song)
            lyrics = self.get_lyrics(lyrics_html)
            print(lyrics)
            self.all.append(lyrics)


if __name__ == '__main__':
    #url = input('Please enter a url: ')
    #obj = Web_Scraping(url, 'hello')

    obj = Web_Scraping('tamino', 'Mozilla/5.0')
    list = obj.print_songs(obj.get_artist_page())
    obj.print_all_songs(list)

    with open('tamino.csv', 'w', encoding="UTF8", newline='') as file:
        writer = csv.writer(file)

        writer.writerows(obj.all)