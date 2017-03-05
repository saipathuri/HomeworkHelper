import string
import markovify
import nltk
import re
import language_check
import random
import json
import os


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words
    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

class EditedTextClass(POSifiedText):
    def __init__(self, input_text, state_size=3, chain=None, runs=None):
        self.input_text = input_text
        self.state_size = state_size
        self.runs = runs or list(self.generate_corpus(self.input_text))
        self.rejoined_text = self.sentence_join(map(self.word_join, self.runs))
        self.chain = chain or markovify.Chain(self.runs, state_size)
    def to_dict(self):
        return {
            "input_text": self.input_text,
            "state_size": self.state_size,
            "chain": self.chain.to_json(),
            "runs": self.runs
        }
    @classmethod
    def from_dict(cls, obj):
        return cls(
            obj["input_text"],
            state_size=obj["state_size"],
            chain=markovify.Chain.from_json(obj["chain"]),
            runs=obj["runs"]
        )

if os.environ.get('AWS_ACCESS_KEY_ID', None) not None:
    with open('/tmp/json.txt') as json_file:
        model2_json = json.load(json_file)
else:
    with open('QuotesJson.txt') as json_file:  
        model2_json = json.load(json_file)
NEW_MODEL = EditedTextClass.from_json(model2_json)

def CreateSentences(EditedTextClass): #definition to generate text. First parameter is the file-path to the .txt file you'll be using to train the model, the second parameter is how many sentences you want out of the markov model.
    tool = language_check.LanguageTool('en-GB')
    text = ""
    for i in range(1): #creates 'NUMSENTENCES' sentence, where NUMSENTENCES is an integer
        text = EditedTextClass.make_sentence(tries = 1) #this, along with the next while loop, basically just forces the markov model to try an infinite number of times to have SOMETHING come out. 
        while (text == None):
            text = EditedTextClass.make_sentence(tries = 1)
        matches = tool.check(text) #checks the grammar of the generated text
        text = language_check.correct(text, matches) #corrects any mistakes the grammar checker found in the text
        print str(text.strip())

def get_sentence():
    return CreateSentences(NEW_MODEL)