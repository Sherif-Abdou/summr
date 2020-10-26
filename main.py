import spacy
import sys
from spacy import displacy
from spacy.tokens import Token

text = ""
# other_nlp = spacy.load("./advanced_vocab_model")
with open("input.txt") as f:
    text = f.read()
"""
for ent in other_nlp(text).ents:
    print(ent.text)

def is_advanced(token):
    other_tok = next(iter(other_nlp(token.text)))
    if other_tok.ent_type_ == "ADVANCED_WORD" and other_tok.pos_ == "ADJ":
        return True
    return False
"""
nlp = spacy.load("en_core_web_md")
# Token.set_extension("is_advanced", getter=is_advanced)

def main(text, count):
    doc = nlp(text)
    subj = first_subj(doc)[0]

    # count = int(input("How many sentences? "))

    ranked = [v[0].text for v in rank_sentences(doc, nlp(subj), count)]
    print()
    string = " ".join(ranked) 
    print(string.replace("\n", ""))
    print()
    return string.replace("\n", "")


# Finds the subjects in a text
def subjs(text):
    def translate(token, sent):
        for chunk in sent.noun_chunks:
            if token == chunk.root:
                return chunk.text
        return token.text

    arr = [v for v in text if v.dep_ in {"nsubj", "nsubjpass"} and not v.is_stop]

    arr = [translate(v, text) for v in arr]

    return arr

# Finds the objects in a text
def objs(text):
    def translate(token, sent):
        for chunk in sent.noun_chunks:
            if token == chunk.root:
                return chunk.text
        return token.text

    arr = [v for v in text if v.dep_ in {"dobj", "pobj"} and not v.is_stop]

    arr = [translate(v, text) for v in arr]

    return arr
   

# Finds the subject of the first sentence
def first_subj(text):
    def translate(token, sent):
        for chunk in sent.noun_chunks:
            if token == chunk.root:
                return chunk.text
        return token.text

    sent = next(iter(text.sents))

    return subjs(sent)


# Ranks sentences based on similarity to the subject and returns the top i results
# Returned in order as they appear in the text
def rank_sentences(text, subj, i):
    items = []
    for j, raw in enumerate(text.sents):
        s = nlp(" ".join(subjs(raw)))
        o = nlp(" ".join(objs(raw)))
        score = subj.similarity(s)+(subj.similarity(o)/2)
        items.append((raw, score, j))

    return sorted((sorted(items, key=lambda x: x[1], reverse=True)[:i]), key=lambda x: x[2])


if __name__ == "__main__":
    file_text = text
    count = input("Count: ")
    main(file_text, int(count))
