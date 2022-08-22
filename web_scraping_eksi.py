import requests
import pyperclip
import re
import csv

class Web_Scraping:

    def __init__(self, url, agent):
        self.url = url
        self.agent = agent
        self.html_text = requests.get(self.url, headers={'User-Agent': self.agent}).text
        self.all = []
        #pyperclip.copy(html_text)
        
    #gets the main url and the page number, returns the html text
    def get_html_text(self, nb):
        new_url = self.url + '?p=' + str(nb)
        return requests.get(new_url, headers={'User-Agent': self.agent}).text

    #returns a list of elements (authors or entries), in a proper way
    def get_elements(self, pattern, html_text):

        elements = re.findall(pattern, html_text)

        elements_br = []
        for e in elements:
            elements_br.append(e.replace('<br/>', '\n '))

        elements_quote1 = []
        for e in elements_br:
            elements_quote1.append(e.replace('&quot;', '"'))

        elements_quote2 = []
        for e in elements_quote1:
            elements_quote2.append(e.replace('&#x27;', "'"))

        elements_link1 = []
        pattern_link1 = '<([\s\S]*?)>'
        for e in elements_quote2:
            elements_link1.append(re.sub(pattern_link1, '', e))

        return elements_link1


    #prints the entries and authors in the page
    def print_dict(self, html_text):
        pattern_entries = '<div class="content">\r\n    ([\s\S]*?)<\/div>'
        pattern_authors = 'data-author="([\s\S]*?)"'

        entries = self.get_elements(pattern_entries, html_text)
        authors = self.get_elements(pattern_authors, html_text)

        if(entries == None or authors == None):
            print('No entries found.')
            return None        
        
        if len(entries) != len(authors):
            print("The number of entries does not match the number of authors.")
            return None

        zip_list = list(zip(authors, entries))

        return zip_list 


    def print_all_pages(self):
        pattern_nbpages = 'pagecount="(.*)\"'
        elements = re.findall(pattern_nbpages, self.html_text)
        nb_pages = int(elements[0])

        for page in range(1, nb_pages + 1):
            #print(f'Page {str(page)}')
            html_text = self.get_html_text(page)
            self.all.append(self.print_dict(html_text))


if __name__ == '__main__':
    #url = input('Please enter a url: ')
    #obj = Web_Scraping(url, 'hello')

    obj = Web_Scraping('https://eksisozluk.com/kelebek--32905', 'hello')
    obj.print_all_pages()

    with open('data/eksisozluk_kelebek.csv', 'w', encoding="UTF8", newline='') as file:
        writer = csv.writer(file)

        for o in obj.all:
            writer.writerows(o)