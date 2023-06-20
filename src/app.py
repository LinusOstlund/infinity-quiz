from flask import Flask, render_template, request, redirect, url_for, session

import json
import os
import random
import openai
from quizmaster import Quizmaster

# from main import generate_question

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
quizmaster = Quizmaster()


@app.route("/", methods=["GET", "POST"])
def quiz():
    if request.method == "POST":
        selected_option = request.form.get("option")
        return redirect(url_for("result", selected_option=selected_option))
    else:
        # Call the function to generate a new question
        # response = generate_question()  # Add this line
        response = quizmaster()
        print(f"Response in FLASK: {response}")
        question = response["Question"]
        options = response["Options"]
        answer = response["Answer"]
        session["question"] = question  # Store the question in the session
        session["answer"] = answer  # Store the answer in the session
        return render_template(
            "quiz.html", question=question, options=options, answer=answer
        )


@app.route("/result/<selected_option>")
def result(selected_option):
    # Here you can handle the answer selected by the user
    answer = session.get("answer")  # Get the answer from the session
    question = session.get("question")  # Get the question from the session
    rationale = quizmaster.rationale(question, selected_option, answer)
    if selected_option == answer:
        response = f"You selected {selected_option}, which is the correct answer!"
    else:
        response = (
            f"You selected {selected_option}, but the correct answer was {answer}."
        )

    # Render the result template
    return render_template("result.html", response=response, rationale=rationale)


if __name__ == "__main__":
    app.run(debug=True)
