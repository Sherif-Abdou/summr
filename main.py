import spacy
import sys
from spacy import displacy

text = ""
with open("input.txt") as f:
    text = f.read()

nlp = spacy.load("en_core_web_lg")
doc = nlp(text)

def get_subjs(text):
    arr =  [v.text for v in text.noun_chunks if v.root.dep_ in {"nsubj", "nsubjpass"} and not v.root.is_stop]
    arr += [v.text for v in text if v.tag_ == "VBG" and v.dep_ in {"nsubj", "nsubjpass"}]
    return arr

# Finds the subjects in the first sentence
def subjs(text):
    def translate(token, sent):
        for chunk in sent.noun_chunks:
            if token == chunk.root:
                return chunk.text
        return token.text

    arr = [v for v in text if v.dep_ in {"nsubj", "nsubjpass"} and not v.is_stop]

    arr = [translate(v, text) for v in arr]

    return arr

def first_subj(text):
    def translate(token, sent):
        for chunk in sent.noun_chunks:
            if token == chunk.root:
                return chunk.text
        return token.text

    sent = next(iter(text.sents))

    return subjs(sent)

def rank_sentences(text, subj, i):
    items = []
    f = True
    for j, raw in enumerate(text.sents):
        s = nlp(" ".join(subjs(raw)))
        items.append((raw, subj.similarity(s), j))

    return sorted((sorted(items, key=lambda x: x[1], reverse=True)[:i]), key=lambda x: x[2])

if __name__ == "__main__":
    subj = first_subj(doc)[0]

    count = 3

    ranked = [v[0].text for v in rank_sentences(doc, nlp(subj), count)]
    print()
    print(" ".join(ranked))
    print()

