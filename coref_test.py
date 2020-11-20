import spacy
import neuralcoref


nlp = spacy.load("en_core_web_lg")
neuralcoref.add_to_pipe(nlp)

doc = nlp(input())
print(doc._.coref_resolved)
