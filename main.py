from flask import Flask, render_template
import requests
import plotly.graph_objs as go

app = Flask(__name__)

# Code to fetch COVID-19 data from the API
def fetch_data(api_key):
    url = f"https://api.covidactnow.org/v2/states.json?apiKey={api_key}"
    response = requests.get(url)
    data = response.json()
    return data

# Route for the dashboard
@app.route('/')
def dashboard():
    api_key = "858356ccc0b34c3bbbb44c52349b2cd2"  # Replace this with your API key
    data = fetch_data(api_key)
    
    table_data = []
    for entry in data:
        state = entry['state']
        cases = entry['actuals']['cases']
        new_cases = entry['actuals']['newCases']
        deaths = entry['actuals']['deaths']
        vaccination_completed=entry['actuals']['vaccinationsCompleted']
        table_data.append({'state': state, 'cases': cases, 'deaths': deaths, 
                            'new_cases':new_cases,'vaccination_completed':vaccination_completed})

    # Create plots
    
    states = [entry['state'] for entry in table_data]
    new_cases = [entry['new_cases'] for entry in table_data]
    deaths = [entry['deaths'] for entry in table_data]
    
    case_plot = go.Bar(x=states, y=new_cases, name='new cases',marker=dict(color='purple'))
    starebcase_plot = go.Bar(x=deaths, y=states, name='Deaths', orientation='h')

    # Layout
    layout = go.Layout(title='New Cases coming daily from each state')
    layout1 = go.Layout(title='Positive tests coming daily from each state')

    # Plot configuration
    new_case_fig = go.Figure(data=[case_plot], layout=layout)
    starebcase_fig = go.Figure(data=[starebcase_plot], layout=layout1)

    new_case_graph = new_case_fig.to_html(full_html=False)
    starebcase_graph = starebcase_fig.to_html(full_html=False)

    return render_template('index.html', new_case_graph=new_case_graph, starebcase_graph=starebcase_graph, table_data=table_data)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=False)
