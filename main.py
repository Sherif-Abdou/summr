import spacy
import neuralcoref
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
neuralcoref.add_to_pipe(nlp)


def main(text, count):
    doc = nlp(text)
    # doc = nlp(doc._.coref_resolved)
    doc = resolve_coreferences(doc)
    subjs = first_subj(doc)
    subj = subjs[0]

    # count = int(input("How many sentences? "))

    ranked = [v[0].text for v in rank_sentences(doc, nlp(subj), count)]
    string = " ".join(ranked) 
    return string.replace("\n", "")

def update_ref_map(doc):
    reference_map = {}
    for cluster in doc._.coref_clusters:
        main_span = cluster.main
        for mention in cluster.mentions:
            if main_span.sent == mention.sent or main_span.text == mention.text:
                continue
            reference_map[mention] = main_span
    return reference_map

def resolve_coreferences(doc):
    reference_map = update_ref_map(doc)
    new_text = ""
    last_end = 0
    
    for mention_span, main_span in reference_map.items():
        start, end = (mention_span.start, mention_span.end)
        if len(mention_span) == 1 and mention_span[0].tag_ == "PRP$":
            # doc = nlp(doc[:start].text + " " + main_span.text + "'s " + doc[end:].text)
            new_word = main_span.text + "'s "
        else:
            # doc = nlp(doc[:start].text + " " + main_span.text + " " + doc[end:].text)
            new_word = main_span.text + " "
        new_text += doc[last_end:start].text + new_word
        last_end = end
    new_text += doc[last_end:].text

    return nlp(new_text)

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
