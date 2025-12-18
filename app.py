import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import yaml
import json
import base64
import io

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("YAML and JSON File Viewer"),
    
    html.H3("Upload a YAML file"),
    dcc.Upload(
        id='upload-yaml',
        children=html.Div(['Drag and Drop or ', html.A('Select YAML File')]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    
    html.H3("Upload a JSON file"),
    dcc.Upload(
        id='upload-json',
        children=html.Div(['Drag and Drop or ', html.A('Select JSON File')]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=False
    ),
    
    html.Hr(),
    html.H3("YAML Content"),
    html.Pre(id='yaml-output', style={'whiteSpace': 'pre-wrap'}),
    
    html.H3("JSON Content"),
    html.Pre(id='json-output', style={'whiteSpace': 'pre-wrap'}),
])

def parse_contents(contents, file_type):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        if file_type == 'yaml':
            return yaml.safe_load(decoded)
        elif file_type == 'json':
            return json.loads(decoded)
    except Exception as e:
        return f"Error parsing {file_type.upper()} file: {e}"

@app.callback(
    Output('yaml-output', 'children'),
    Input('upload-yaml', 'contents')
)
def update_yaml(contents):
    if contents is None:
        return "No YAML file uploaded yet."
    parsed = parse_contents(contents, 'yaml')
    return json.dumps(parsed, indent=2)

@app.callback(
    Output('json-output', 'children'),
    Input('upload-json', 'contents')
)
def update_json(contents):
    if contents is None:
        return "No JSON file uploaded yet."
    parsed = parse_contents(contents, 'json')
    return json.dumps(parsed, indent=2)

if __name__ == '__main__':
    app.run(debug=True)
