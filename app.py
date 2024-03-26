from flask import Flask, render_template, request
from start import summarizer
import io
import fitz

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['GET','POST'])
def analyze():
    if request.method == 'POST':
        rawtext = request.form['rawtext']
        summary, original_txt, len_orig_txt, len_summary = summarizer(rawtext)
    
    return render_template('summary.html', summary=summary, original_txt = original_txt, len_orig_txt = len_orig_txt, len_summary=len_summary)

@app.route('/upload', methods=['POST'])
def upload():
    pdf_file = request.files['pdf-file']
    if pdf_file:
        pdf_data = pdf_file.read()
        pdf_doc = fitz.open(stream=pdf_data, filetype="pdf")
        pdf_text = ''
        for page in pdf_doc:
            pdf_text += page.get_text()
        return render_template('index.html', pdf_text=pdf_text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)



