from flask import Flask, request, send_file, render_template
import os
import nbformat
from flask_cors import CORS
from nbconvert import PDFExporter
import subprocess
import shutil

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'analysisType' not in request.form:
        return 'Missing file or analysis type'
    
    file = request.files['file']
    analysis_type = request.form['analysisType']

    if file.filename == '':
        return 'No selected file'
    
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Select notebook based on the analyisis type
        notbook_filename = select_notebook(analysis_type)

        # Call Jupyter notebook processing function
        result_filepath = process_notebook(filepath, notbook_filename)

        return send_file(result_filepath, as_attachment=True)

def select_notebook(analysis_type):
    # Mapping analysis types to corresponding notebook file names
    notebook_mapping = {
        "Standard": "Notebooks/prueba_analisis_IMEx.ipynb", 
        "Duplicates": "Notebooks/IMEx_Macro_2.ipynb", 
        "Blanks": "Notebooks/Blanks_report.ipynb"
    }
    return notebook_mapping.get(analysis_type, 'default_report.ipynb')

def process_notebook(filepath, notebook_filename):
    result_pdf = os.path.join(RESULT_FOLDER, 'report.html')
    temp_notebook = 'temp_notebook.ipynb'

    # Copy the selected notebook to a temporary file to modify
    shutil.copy(notebook_filename, temp_notebook)

    # Open and modify the notebook to include the file path
    with open(temp_notebook, 'r') as file:
        notebook_content = file.read()

    # Update the notebook content with the file path
    notebook_content = notebook_content.replace('FILE_PATH_PLACEHOLDER', filepath)


    with open(temp_notebook, 'w') as file:
        file.write(notebook_content)

    # Run the Jupyter notebook with the updated file path
    command = f'jupyter nbconvert --to html --no-input --execute --output {result_pdf} {temp_notebook}'
    print("Running command:", command)  # Debug print statement
    subprocess.run(command, shell=True, check=True)
    
    # Clean up
    os.remove(temp_notebook)
    
    return result_pdf

if __name__ == '__main__':
    app.run(debug=True)
