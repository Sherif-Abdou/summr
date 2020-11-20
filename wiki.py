import main 
import re
from re import subn 
from wikipedia import page, summary

def filter_content(content):
    return content

if __name__ == "__main__":
    term = input("Search term: ")
    sentence_count = int(input("Sentence Count: "))
    content = filter_content(summary(term))
    print(f"Content:\n{content}")
    print("Summarizing...")
    print(main.main(content, sentence_count))

