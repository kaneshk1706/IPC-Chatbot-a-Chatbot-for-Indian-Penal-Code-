from flask import Flask, request, jsonify, render_template
from googletrans import Translator
import pandas as pd
import time
app = Flask(__name__)

# Read the CSV file
file_path = 'ipc_sections.csv'  # Path to your CSV file
df = pd.read_csv(file_path)

# Get unique offenses for the dropdown
offense_options = df['Offense'].unique()

@app.route('/')
def index():
    return render_template('index5.html')

@app.route('/suggest_offenses')
def suggest_offenses():
    user_input = request.args.get('user_input')
    matching_offenses = [offense for offense in offense_options if isinstance(offense, str) and user_input.lower() in offense.lower()]
    if matching_offenses:
        return jsonify(matching_offenses)
    else:
        return jsonify([])

@app.route('/get_offense_details')
def get_offense_details():
    offense = request.args.get('offense')
    offense_details = df[df['Offense'] == offense]
    return jsonify({
        'Description': offense_details['Description'].values[0],
        'Punishment': offense_details['Punishment'].values[0],
        'IPC Section': offense_details['Section'].values[0]
    })

@app.route('/translate_offense_details')
def translate_offense_details():
    offense = request.args.get('offense')
    description = request.args.get('description')
    punishment = request.args.get('punishment')
    ipc_section = request.args.get('ipc_section')
    target_language = request.args.get('language')

    translator = Translator()
    try:
        # Check if any of the inputs are None
        if description is None or punishment is None or ipc_section is None or offense is None:
            raise ValueError("One or more input values are missing.")

        # Translate each field separately
        translated_description = translator.translate(description, src='en', dest=target_language).text
        translated_punishment = translator.translate(punishment, src='en', dest=target_language).text
        translated_ipc_section = translator.translate(ipc_section, src='en', dest=target_language).text
        translated_offense = translator.translate(offense, src='en', dest=target_language).text

        # Return the translated response with appropriate keys
        return jsonify({
            'Offense Description': translated_description,
            'Punishment': translated_punishment,
            'IPC Section': translated_ipc_section
        })
    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"Error translating offense details: {e}")
        return jsonify({'error': str(e)})  # Return the error message

if __name__ == '__main__':
    app.run(debug=True)
