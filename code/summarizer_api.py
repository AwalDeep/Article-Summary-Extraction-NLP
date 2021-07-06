from flask import Flask,render_template,request
from summarizer import Summarizer
app = Flask(__name__)

summarizer = Summarizer(2)
summarizer.create_word_embeddings()

@app.route('/summary')
def form():
    return render_template('form.html')

@app.route('/summary/', methods=['GET', 'POST'])
def summarize():
    if request.method == 'GET':
        return f"The URL /summary is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        input = list(dict(form_data).values())[0]
        clean_sentences = summarizer.preprocess(input)
        summary = summarizer.summarize(clean_sentences.iloc[0])
        return render_template('form.html', form_data=summary)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1008)
