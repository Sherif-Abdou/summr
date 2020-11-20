import spacy
from spacy import displacy
from spacy.matcher import Matcher

nlp = spacy.load("./advanced_vocab_model")

doc = nlp(input())
matcher = Matcher(nlp.vocab)

pattern = [{"POS": "ADJ", "ENT_TYPE": "ADVANCED_WORD"}]
matcher.add("ADVANCED", None, pattern)

for match, start, end in matcher(doc):
    string_id = nlp.vocab.strings[match_id]  # Get string representation
    span = doc[start:end]  # The matched span
    print(match_id, string_id, start, end, span.text)

