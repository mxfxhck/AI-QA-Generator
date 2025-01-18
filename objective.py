import re
import nltk
import numpy as np
from nltk.corpus import wordnet as wn

class ObjectiveTest:

    def __init__(self, data, noOfQues, bloomsLevel):
        self.summary = data
        self.noOfQues = noOfQues
        self.bloomsLevel = bloomsLevel

    def get_trivial_sentences(self):
        sentences = nltk.sent_tokenize(self.summary)
        trivial_sentences = []
        for sent in sentences:
            print(f"Processing sentence: {sent}")  # Debug log
            trivial = self.identify_trivial_sentences(sent)
            if trivial:
                print(f"Trivial sentence identified: {trivial}")  # Debug log
                trivial_sentences.append(trivial)
        print(f"Total trivial sentences: {len(trivial_sentences)}")  # Debug log
        return trivial_sentences

    def identify_trivial_sentences(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        if len(tokens) < 4:  # Skip very short sentences
            print(f"Skipping short sentence: {sentence}")  # Debug log
            return None

        tags = nltk.pos_tag(tokens)
        print(f"POS tags for sentence: {tags}")  # Debug log

        noun_phrases = []
        grammar = r"""
            CHUNK: {<NN>+<IN|DT>*<NN>+}
                   {<NN>+<IN|DT>*<NNP>+}
                   {<NNP>+<NNS>*}
        """
        chunker = nltk.RegexpParser(grammar)
        tree = chunker.parse(tags)
        print(f"Parsed tree: {tree}")  # Debug log

        for subtree in tree.subtrees():
            if subtree.label() == "CHUNK":
                phrase = " ".join([word for word, _ in subtree.leaves()])
                noun_phrases.append(phrase)

        if not noun_phrases:
            print(f"No noun phrases found in sentence: {sentence}")  # Debug log
            return None

        replace_phrase = noun_phrases[-1] if noun_phrases else tokens[-1]
        blanks_phrase = "__________"
        sentence = re.sub(re.escape(replace_phrase), blanks_phrase, sentence, flags=re.IGNORECASE)

        return {"Question": sentence, "Answer": replace_phrase, "Key": len(replace_phrase)}

    def generate_test(self):
        trivial_pair = self.get_trivial_sentences()
        if not trivial_pair:
            print("No trivial sentences found. Cannot generate questions.")
            return [], []

        # Filter by Bloom's Taxonomy level if applicable
        if self.bloomsLevel == "Remembering":
            trivial_pair = [qa for qa in trivial_pair if qa["Key"] > 2]
        elif self.bloomsLevel == "Understanding":
            trivial_pair = trivial_pair  # Placeholder: Add more logic for specific levels
        # Add logic for other levels (Applying, Analyzing, etc.) here

        print(f"Filtered question-answer pairs: {len(trivial_pair)}")

        if not trivial_pair:
            print("No valid question-answer pairs found.")
            return [], []

        question, answer = [], []
        attempts = 0
        while len(question) < int(self.noOfQues) and attempts < 100:
            rand_num = np.random.randint(0, len(trivial_pair))
            if trivial_pair[rand_num]["Question"] not in question:
                question.append(trivial_pair[rand_num]["Question"])
                answer.append(trivial_pair[rand_num]["Answer"])
            attempts += 1

        if len(question) < int(self.noOfQues):
            print(f"Only {len(question)} questions could be generated.")

        return question, answer
