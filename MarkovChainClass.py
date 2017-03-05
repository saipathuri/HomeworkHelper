import string
import markovify
import nltk
import re
import language_check
import random
import json

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


class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words
    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence
    
