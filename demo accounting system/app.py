import dash
from dash import Dash, dcc, html, Input, Output
import flask
import form_executor

app = Dash(__name__, use_pages=True)

app.layout = html.Div(
    [
        html.Div(
            [
                # html.H1('Home'),

                html.Div(
                    [
                        dcc.Link(f'{page["name"]}', href=page['relative_path'])
                        for page in dash.page_registry.values()
                    ]
                ),
    
            ],
            className='nav-div'
        ),
        html.Div(
            [
                dash.page_container
            ],
            className='page-displayer'
        )
    ]
)

@app.server.route('/post', methods=['POST'])
def on_post():
    data = flask.request.form
    for k,v in data.items():
        print(k,v)

    form_executor.execute_transction(data)
    return flask.redirect('/4/inventory')

if __name__ == '__main__':
    import test_data
    app.run(debug=True)

