import dash
import base64
from dash import html, dcc

dash.register_page(__name__)

test_png = 'assets/pp.png'
pp = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

layout = html.Div([
            html.Div([
                html.H2("Our Mission"),
                html.P("At [Your Website Name], our mission is to provide comprehensive and insightful analysis of election data to empower informed decision-making and foster a deeper understanding of the democratic process. We are dedicated to delivering accurate, unbiased, and timely election data visualizations and reports to citizens, journalists, policymakers, and researchers."),
                html.P("Through cutting-edge data analysis techniques and user-friendly visualizations, we aim to bridge the gap between raw election data and actionable insights. Our commitment to transparency and integrity ensures that our audience can explore electoral trends, demographics, voter behavior, and more, fostering a more engaged and informed electorate."),
                html.P("We believe that access to accurate and well-presented election data is essential for a vibrant democracy. Our platform is designed to not only present the numbers but also to tell the stories behind the data, revealing the dynamics that shape elections and highlighting the voices of diverse communities."),
                html.P("Join us on this journey to uncover the stories within the numbers and contribute to a more informed and participatory democratic society."),
                html.P("Feel free to adapt and modify this mission statement to align with the specific goals and values of your election data analysis website."),
            ]),
        html.Div([
            html.H2("Meet the Team"),
            html.Div([
                html.Div([
                    html.Img(src='data:image/png;base64,{}'.format(pp), alt="Team Member 1", width="150", height="150"),
                    html.Div([
                        html.H3("Sumit Raj", style={"margin-left":30}),
                        html.P(html.B("(Aspiring Data Scientist)")),
                        html.Tbody("\"As an aspiring data scientist, I am not just seeking opportunities; I'm carving my path through the digital labyrinth\
                        and embracing data's symphony, I orchestrate insights from chaos, conducting a melody of knowledge. In a world of numbers, I am the interpreter,\
                        decoding stories that shape decisions. An aspiring data scientist, I navigate the sea of information to chart a course for a smarter future.\"")
                    ], className="team-info")
                ], className="team-member")
                ])
            ])
        ], className="container")