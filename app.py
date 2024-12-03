from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# Ensure the static directory exists
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    selected_year = request.form['year']
    
    if file:
        # Read the CSV file into a DataFrame
        data = pd.read_csv(file)

        # Check if the required columns exist
        required_columns = ['year', 'State', 'Party', 'Seats', 'Votes']
        if not all(col in data.columns for col in required_columns):
            return "CSV must contain 'year', 'State', 'Party', 'Seats', and 'Votes' columns.", 400

        # Store the DataFrame in a global variable or session for later use
        app.config['data'] = data

        # Filter data for the selected year
        filtered_data = data[data['year'] == int(selected_year)]

        # Perform analysis: Calculate total votes and percentage
        total_votes = filtered_data['Votes'].sum()
        filtered_data['Percentage'] = (filtered_data['Votes'] / total_votes) * 100

        # Prepare data for charts
        party_votes = filtered_data.groupby('Party')['Votes'].sum().reset_index()
        years = filtered_data['year'].unique().tolist()
        
        # Prepare votes over years for each party
        votes_by_party = {}
        for party in filtered_data['Party'].unique():
            votes_by_party[party] = filtered_data[filtered_data['Party'] == party].groupby('year')['Votes'].sum().reindex(years, fill_value=0).tolist()

        # Convert votes_by_party to a list of lists for Chart.js
        votes_by_party_list = [votes_by_party[party] for party in party_votes['Party']]

        # Pass data to the template
        return render_template('result.html', 
                               party_votes=party_votes.to_dict(orient='records'), 
                               years=years, 
                               votes_by_party=votes_by_party_list,
                               party_names=party_votes['Party'].tolist())

@app.route('/analyze', methods=['POST'])
def analyze():
    selected_year = request.form['year']
    data = app.config.get('data')

    if data is None:
        return "No data available. Please upload a file first.", 400

    # Filter data for the selected year
    filtered_data = data[data['year'] == int(selected_year)]

    # Perform analysis: Calculate total votes and percentage
    total_votes = filtered_data['Votes'].sum()
    filtered_data['Percentage'] = (filtered_data['Votes'] / total_votes) * 100

    # Prepare data for charts
    party_votes = filtered_data.groupby('Party')['Votes'].sum().reset_index()
    years = filtered_data['year'].unique().tolist()
    
    # Prepare votes over years for each party
    votes_by_party = {}
    for party in filtered_data['Party'].unique():
        votes_by_party[party] = filtered_data[filtered_data['Party'] == party].groupby('year')['Votes'].sum().reindex(years, fill_value=0).tolist()

    # Convert votes_by_party to a list of lists for Chart.js
    votes_by_party_list = [votes_by_party[party] for party in party_votes['Party']]

    # Pass data to the template
    return render_template('result.html', 
                           party_votes=party_votes.to_dict(orient='records'), 
                           years=years, 
                           votes_by_party=votes_by_party_list,
                           party_names=party_votes['Party'].tolist())

if __name__ == '__main__':
    app.run(debug=True)