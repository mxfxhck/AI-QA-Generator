import numpy as np
import nltk as nlp

class SubjectiveTest:

    def __init__(self, data, noOfQues, bloomsLevel):
        self.question_pattern = {
            "Remembering": [
                "Define ",
                "What is ",
                "List ",
            ],
            "Understanding": [
                "Explain in detail ",
                "Describe ",
                "Summarize ",
            ],
            "Applying": [
                "How would you apply ",
                "Demonstrate the use of ",
                "Illustrate how ",
            ],
            "Analyzing": [
                "What are the components of ",
                "How does ",
                "What is the relationship between ",
            ],
            "Evaluating": [
                "What are the advantages and disadvantages of ",
                "Evaluate the importance of ",
                "Critique ",
            ],
            "Creating": [
                "Propose a solution to ",
                "Design a new way to ",
                "Devise a plan for ",
            ]
        }
        self.grammar = r"""
            CHUNK: {<NN>+<IN|DT>*<NN>+}
                   {<NN>+<IN|DT>*<NNP>+}
                   {<NNP>+<NNS>*}
        """
        self.summary = data
        self.noOfQues = noOfQues
        self.bloomsLevel = bloomsLevel

    def generate_test(self):
        sentences = nlp.sent_tokenize(self.summary)
        cp = nlp.RegexpParser(self.grammar)
        question_answer_dict = {}

        # Extract keywords and map to sentences
        for sentence in sentences:
            tagged_words = nlp.pos_tag(nlp.word_tokenize(sentence))
            tree = cp.parse(tagged_words)
            for subtree in tree.subtrees():
                if subtree.label() == "CHUNK":
                    temp = " ".join([sub[0] for sub in subtree]).strip().lower()
                    if temp not in question_answer_dict:
                        if len(nlp.word_tokenize(sentence)) > 10:  # Allow shorter sentences
                            question_answer_dict[temp] = sentence
                    else:
                        question_answer_dict[temp] += " " + sentence

        # Check for empty results
        keyword_list = list(question_answer_dict.keys())
        if not keyword_list:
            print("No keywords extracted. Cannot generate questions.")
            return [], []

        question_answer = []
        for _ in range(int(self.noOfQues)):
            rand_num = np.random.randint(0, len(keyword_list))
            selected_key = keyword_list[rand_num]
            answer = question_answer_dict[selected_key]

            # Select pattern based on Bloom's level
            if self.bloomsLevel in self.question_pattern:
                rand_pattern = np.random.randint(0, len(self.question_pattern[self.bloomsLevel]))
                question = self.question_pattern[self.bloomsLevel][rand_pattern] + selected_key + "."
            else:
                print(f"Unknown Bloom's Level: {self.bloomsLevel}")
                return [], []

            question_answer.append({"Question": question, "Answer": answer})

        # Ensure unique questions
        que, ans = [], []
        attempts = 0
        while len(que) < int(self.noOfQues) and attempts < 100:
            rand_num = np.random.randint(0, len(question_answer))
            if question_answer[rand_num]["Question"] not in que:
                que.append(question_answer[rand_num]["Question"])
                ans.append(question_answer[rand_num]["Answer"])
            attempts += 1

        if len(que) < int(self.noOfQues):
            print(f"Only {len(que)} questions could be generated.")

        return que, ans
