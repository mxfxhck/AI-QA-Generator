from flask import Flask, request, render_template, flash, redirect, url_for, session
from objective import ObjectiveTest
from subjective import SubjectiveTest
import time

app = Flask(__name__)

app.secret_key = 'aica2'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_generate', methods=["POST"])
def test_generate():
    print("Received POST request to /test_generate")
    if request.method == "POST":
        try:
            inputText = request.form.get("itext", "").strip()
            testType = request.form.get("test_type", "").strip()
            bloomsLevel = request.form.get("blooms_level", "").strip()
            noOfQues = request.form.get("noq", "").strip()

            if not inputText or not testType or not bloomsLevel or not noOfQues:
                flash('All fields are required!')
                print("Validation failed: Missing input fields")
                return redirect(url_for('index'))

            try:
                noOfQues = int(noOfQues)  # Ensure noOfQues is an integer
            except ValueError:
                flash('Number of questions must be a valid integer!')
                print("Validation failed: Invalid number of questions")
                return redirect(url_for('index'))

            print(f"Test Type: {testType}, Bloom's Level: {bloomsLevel}, Number of Questions: {noOfQues}")

            start_time = time.time()

            if testType == "objective":
                print("Generating objective questions...")
                objective_generator = ObjectiveTest(inputText, noOfQues, bloomsLevel)
                question_list, answer_list = objective_generator.generate_test()
                print(f"Objective test generated in {time.time() - start_time:.2f} seconds")
            elif testType == "subjective":
                print("Generating subjective questions...")
                subjective_generator = SubjectiveTest(inputText, noOfQues, bloomsLevel)
                question_list, answer_list = subjective_generator.generate_test()
                print(f"Subjective test generated in {time.time() - start_time:.2f} seconds")
            else:
                flash('Invalid test type!')
                print("Validation failed: Invalid test type")
                return redirect(url_for('index'))

            # Combine questions, answers, and Bloom's level for frontend display
            testgenerate = [(q, a, bloomsLevel) for q, a in zip(question_list, answer_list)]
            print("Rendering template: generatedtestdata.html")
            return render_template('generatedtestdata.html', cresults=testgenerate)

        except Exception as e:
            print(f"Error: {e}")
            flash('An unexpected error occurred! Please try again.')
            return redirect(url_for('index'))

    print("Fallback: Redirecting to index")
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
