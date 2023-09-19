import dash
from dash import html, dcc, clientside_callback
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# Initialize the Dash app
app = dash.Dash(__name__,use_pages=True)
server = app.server

app.layout = html.Div([
        html.Header(id="header",children=[
            html.H1("Indian Election Analysis"),
                html.Nav([
                    html.Ul([
                            html.Li([
                            dcc.Link(f"{page['name']}", href=page["relative_path"])
                            ]) for page in dash.page_registry.values()
                        ])
                    ])
                ], className="header"),
        dash.page_container,
        html.Footer([
            html.Div([
                html.P("© 2023 Your Election Analysis. All rights reserved."),
                html.A("Privacy Policy", href="/privacy"),
                html.A("Terms of Service", href="/terms"),
                ], className="footer-content"),
            ], className="footer"),
        ])
 
app.clientside_callback(
"""
function(value) {
    return value
}""",
Output('year','data'),
Input('drop','value')
)

app.clientside_callback(
"""
function g12(data_year) {
    function seats(N, M, r0 = 2.5) {
        const radii = Array.from({ length: M }, (_, i) => r0 - (r0 - 1) * (i / (M - 1)));
        const counts = new Array(M).fill(0);
        const ptsList = [];

        for (let i = 0; i < M; i++) {
            counts[i] = Math.round(N * radii[i] / radii.slice(i).reduce((acc, val) => acc + val, 0));
            const theta = Array.from({ length: counts[i] }, (_, j) => (j / (counts[i] - 1)) * Math.PI);
            N -= counts[i];

            const pts = theta.map((angle) => ({
                x: radii[i] * Math.cos(angle),
                y: radii[i] * Math.sin(angle),
                r: i,
                theta: angle,
            }));

            ptsList.push(pts);
        }

        const pts = ptsList.flat().sort((a, b) => b.theta - a.theta || b.r - a.r);
        return pts;
    }

    function election(seats, data) {
        const counts = data.map(entry => entry.count);
        const names = data.map(entry => entry.party);
        const partyIds = counts.flatMap((count, index) => Array(count).fill(index));
        const partyNames = counts.flatMap((count, index) => Array(count).fill(names[index]));

        for (let i = 0; i < seats.length; i++) {
            seats[i].party = partyIds[i];
            seats[i].party_names = partyNames[i];
        }
        return seats;
    }

    const n = data_year.length;
    const seatCounts = new Map();

    data_year.forEach(entry => {
        const party = entry.party;
        seatCounts.set(party, (seatCounts.get(party) || 0) + 1);
    });
    const sortedSeatCounts = new Map([...seatCounts.entries()].sort((a, b) => b[1] - a[1]));
    const seatCountsArray = Array.from(sortedSeatCounts, ([party, count]) => ({ party, count }));
    const m = Math.floor((n * 16) / 545);

    const layout1 = seats(n, m);
    const result = election(layout1, seatCountsArray);
    return result;
    }""",
Output('graph','data'),
Input('data_store','data'))

if __name__ == '__main__':
    app.run_server(debug=True)
