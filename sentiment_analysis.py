from msilib.schema import File
from transformers import pipeline
import csv
import numpy as np
import artist_names

class Sentiment_Analysis:

    def __init__(self):
        pass

    def loop_artists(self):
        

        list_values = []

        sentiment_analysis = pipeline("sentiment-analysis")

        for artist in artist_names.list:
            path = 'C:\\Users\\Yagmur Denizli\\Desktop\\coding_stuff\\staj\\lyrics\\' + artist + '.csv'
            file = open(path, encoding='utf-8')
            text = csv.reader(file)
            val = self.get_artist_value(text, sentiment_analysis)
            list_values.append([artist,val])
        
        return list_values

    def get_artist_value(self, text, sentiment_analysis):

        header = []
        header = next(text)

        songs = []
        for row in text:
            songs.append(row)
        nb_songs = len(songs)

        songs_with_values = []
        artist_sum = 0

        for s in songs:

            list = s[6].split()
            nb_words = len(list)
            #print(nb_words)
            nb_chunks = (nb_words // 256) + 1
            list_of_chunks = []
            sum_of_sentiments = 0

        #divide the song in parts, put them in list of chunks
            list_of_chunks = np.array_split(list, nb_chunks)

        #calculate the sentiment of each chunk
            for c in list_of_chunks:
                dict = sentiment_analysis(''.join(c))
                label = dict[0].get('label')

                if label == 'NEGATIVE':
                    sum_of_sentiments -= dict[0].get('score')
                else:
                    sum_of_sentiments += dict[0].get('score')
                

        #take the average
            average = sum_of_sentiments / nb_chunks
            #print(average)

            s.append(average)
            songs_with_values.append(s)
            artist_sum += average

        artist_average = artist_sum / nb_songs

        print(artist_average)
        return artist_average

    def write_into_file(self, list):

        with open('data/artist_average.csv', 'w', encoding="UTF8", newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(list)
    
if __name__ == '__main__':
    sent = Sentiment_Analysis()
    list = sent.loop_artists()
    sent.write_into_file(list)
    print('fin')