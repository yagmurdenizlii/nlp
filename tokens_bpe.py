#hugging face tokenizers quicktour

#The main API of the library is the class Tokenizer, here is how we instantiate one with a BPE model:
from tokenizers import Tokenizer
from tokenizers.models import BPE
tokenizer = Tokenizer(BPE(unk_token="[UNK]"))

#To train our tokenizer, we will need to instantiate a [trainer]{.title-ref},
#in this case a BpeTrainer

from tokenizers.trainers import BpeTrainer
trainer = BpeTrainer(special_tokens=["[UNK]", "[CLS]", "[SEP]", "[PAD]", "[MASK]"])

# the easiest pre-tokenizer possible by splitting on whitespace.
from tokenizers.pre_tokenizers import Whitespace
tokenizer.pre_tokenizer = Whitespace()

#training
import artist_names

path = 'C:\\Users\\Yagmur Denizli\\Desktop\\coding_stuff\\staj\\lyrics\\'

#list_of_files = [path + artist for artist in artist_names.list]
#tokenizer.train(list_of_files, trainer)
#tokenizer.save(f"data/tokenizer-all.json")

for artist in artist_names.list:
    tokenizer.train([path + artist + '.csv'])
    tokenizer.save('data/tokenizer-' + artist + '.json')

print('fin')