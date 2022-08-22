#put all lyrics together

import random

from sklearn.model_selection import train_test_split
import artist_names
import csv
import numpy as np
import statistics
import os
import re
from transformers import DataCollatorWithPadding, GPT2LMHeadModel, GPT2Model, GPT2Tokenizer, TextDataset, GPT2TokenizerFast, Trainer, TrainingArguments
from datasets import Dataset
import pandas as pd
import torch
from datasets import load_metric
from transformers import AutoModelForSequenceClassification

def put_all_together():
    path = 'C:\\Users\\Yagmur Denizli\\Desktop\\coding_stuff\\staj\\lyrics\\'

    list_of_files = [path + artist + '.csv' for artist in artist_names.list]
    
    all_lyrics = []

    for file_path in list_of_files:
        df = pd.read_csv(file_path)
        df = df.dropna()

        text_list = df['Lyric'].values.tolist() 

        new_all_lyrics = []

        for line in text_list:
            new_line = line
            for name in artist_names.list_with_spaces:
                new_line = new_line.replace(name.lower(), '')
            new_all_lyrics.append(new_line)

        for row in new_all_lyrics:
            if type(row) is str:
                row_list = row.split()
                nb_words = len(row_list)
                if nb_words > 256:
                    nb_chunks = nb_words // 256 + 1
                    arr = np.array_split(row_list, nb_chunks)

                    for array in arr:
                        all_lyrics.append(' '.join(array) + '\n')
    
                elif nb_words > 20:
                    all_lyrics.append(row)

    df = pd.DataFrame(all_lyrics, columns=[""])
    df.to_csv('all_lyrics.csv', index=False)
  
    print('fin')       

    return new_all_lyrics

def find_random_length(all_lyrics):

    lengths = []

    for song in all_lyrics:
        length = len(song.split())
        if length > 10 and length < 1000:
            lengths.append(length)

    average = sum(lengths) / len(lengths)
    std = statistics.stdev(lengths)  

    return int(np.random.normal(average, std))

def create_test_data(all_lyrics):
    print(type(all_lyrics))
    for song in all_lyrics:

        split_list = song.split()

        song_length = len(split_list)
        test_length = len(split_list) // 10

        #pandas shuffle
        #scikit
        big_chunk = split_list[:-test_length]
        small_chunk = split_list[-test_length:]

        #control
        if len(big_chunk) + len(small_chunk) != song_length:
            print('error')

        return [big_chunk, small_chunk]



def train_func():
    

    tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
    special_tokens = ["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]
    tokenizer.add_tokens(special_tokens)

    training_data, test_data = train_test_split(all_lyrics, test_size = 0.15, random_state=42)

    tokenizer.pad_token = tokenizer.eos_token

    tokenized_training_data = tokenizer('this is a sentence',  return_tensors = 'pt', padding = True, truncation = True, add_special_tokens = True)

    data_collator = DataCollatorWithPadding(tokenizer)

    model = GPT2Model.from_pretrained('gpt2')
    model.resize_token_embeddings(len(tokenizer))

    training_args = TrainingArguments(output_dir="test_trainer")

    trainer = Trainer(
        model = model,
        args = training_args,
        train_dataset = tokenized_training_data,
        eval_dataset = tokenized_training_data,
        data_collator = data_collator,
        tokenizer = tokenizer
        )

    trainer.train()

    print('fin')


if __name__ == '__main__':

    all = put_all_together()

    train_func()