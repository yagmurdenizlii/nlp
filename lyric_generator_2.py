import os
import re
from transformers import GPT2Tokenizer, TextDataset, GPT2TokenizerFast
from datasets import Dataset
import pandas as pd
import torch
import numpy as np

path = 'C:\\Users\\Yagmur Denizli\\Desktop\\coding_stuff\\staj\\lyrics2'
clean_path = 'C:\\Users\\Yagmur Denizli\\Desktop\\coding_stuff\\staj\\clean_lyrics.txt'
files = os.listdir(path)
#print(files)

with open(path + '\\' + files[0]) as file:
    lyrics = file.read()

#get rid of special characters
lyrics = re.sub(r'[^a-zA-Z\d\s]', u'', lyrics)
lyrics = lyrics.lower().split('\n')

#write the clean lyrics into file
with open(clean_path, 'w') as f:
    f.write('\n'.join(lyrics))

#tokenize
tokenizer = GPT2TokenizerFast.from_pretrained('distilgpt2')
special_tokens = ["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"]
tokenizer.add_tokens(special_tokens)

def tokenization(ex):
    print(type(ex))
    return tokenizer(ex)

tokens1 = tokenizer(lyrics)
