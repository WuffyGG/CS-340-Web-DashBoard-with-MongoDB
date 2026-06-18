import base64
from pathlib import Path
from dash import dcc, html, dash_table
from config import LOGO_FILE


def encode_logo():
    """Encode the logo image as base64 if the file exists."""
    logo_path = Path(LOGO_FILE)

    if not logo_path.exists():
        return None

    with open(logo_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def create_layout(df):
    """Create the Dash application layout."""
    encoded_image = encode_logo()

    logo_component = html.H3("Grazioso Salvare")

    if encoded_image:
        logo_component = html.A(
            html.Img(
                src=f"data:image/png;base64,{encoded_image}",
                style={"height": "100px"}
            ),
            href="http://www.snhu.edu"
        )

    breed_options = []
    if "breed" in df.columns:
        breed_options = [
            {"label": breed, "value": breed}
            for breed in sorted(df["breed"].dropna().unique())
        ]

    sex_options = []
    if "sex_upon_outcome" in df.columns:
        sex_options = [
            {"label": sex, "value": sex}
            for sex in sorted(df["sex_upon_outcome"].dropna().unique())
        ]

    table_columns = [{"name": i, "id": i} for i in df.columns]

    if "suitability_score" not in df.columns:
        table_columns.append({"name": "suitability_score", "id": "suitability_score"})

    return html.Div([
        html.Center(logo_component),
        html.Center(html.B(html.H1("Grazioso Salvare Dashboard - Daniel Urena"))),
        html.Hr(),

        html.Div([
            html.Label("Select Rescue Type:"),
            dcc.Dropdown(
                id="filter-type",
                options=[
                    {"label": "Water Rescue", "value": "Water Rescue"},
                    {"label": "Mountain or Wilderness Rescue", "value": "Mountain or Wilderness Rescue"},
                    {"label": "Disaster or Individual Tracking", "value": "Disaster or Individual Tracking"},
                    {"label": "Reset", "value": "Reset"}
                ],
                placeholder="Select a rescue type",
                style={"width": "50%"}
            )
        ]),

        html.Br(),
        html.Hr(),

        html.H3("Custom Rescue Suitability Scoring"),

        html.Div([
            html.Div([
                html.Label("Preferred Breeds:"),
                dcc.Dropdown(
                    id="preferred-breeds",
                    options=breed_options,
                    multi=True,
                    placeholder="Select preferred breed(s)",
                    style={"width": "300px"}
                ),
            ], style={"marginBottom": "12px"}),

            html.Div([
                html.Div([
                    html.Label("Minimum Age in Weeks:"),
                    dcc.Input(
                        id="min-age",
                        type="number",
                        value=26,
                        min=0,
                        step=1,
                        style={"width": "120px"}
                    ),
                ], style={"marginRight": "30px"}),

                html.Div([
                    html.Label("Maximum Age in Weeks:"),
                    dcc.Input(
                        id="max-age",
                        type="number",
                        value=156,
                        min=0,
                        step=1,
                        style={"width": "120px"}
                    ),
                ]),
            ], style={"display": "flex", "marginBottom": "12px"}),

            html.Div([
                html.Label("Preferred Sex:"),
                dcc.Dropdown(
                    id="preferred-sex",
                    options=sex_options,
                    placeholder="Select preferred sex",
                    style={"width": "300px"}
                ),
            ], style={"marginBottom": "12px"}),

            html.Div([
                html.Div([
                    html.Label("Breed Weight:"),
                    dcc.Input(
                        id="breed-weight",
                        type="number",
                        value=50,
                        min=0,
                        step=1,
                        style={"width": "120px"}
                    ),
                ], style={"marginRight": "30px"}),

                html.Div([
                    html.Label("Age Weight:"),
                    dcc.Input(
                        id="age-weight",
                        type="number",
                        value=30,
                        min=0,
                        step=1,
                        style={"width": "120px"}
                    ),
                ], style={"marginRight": "30px"}),

                html.Div([
                    html.Label("Sex Weight:"),
                    dcc.Input(
                        id="sex-weight",
                        type="number",
                        value=20,
                        min=0,
                        step=1,
                        style={"width": "120px"}
                    ),
                ]),
            ], style={"display": "flex", "marginBottom": "12px"}),
        ]),

        html.Hr(),

        html.H3("Database Summary Statistics"),

        html.Div(id="breed-summary-table"),

        html.Br(),
        html.Hr(),

        dash_table.DataTable(
            id="datatable-id",
            columns=table_columns,
            data=df.to_dict("records"),
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={"textAlign": "left"},
            sort_action="native",
            filter_action="native",
            row_selectable="single",
            selected_rows=[],
            selected_columns=[],
            style_data={"whiteSpace": "normal", "height": "auto"}
        ),

        html.Br(),
        html.Hr(),

        html.Div(
            className="row",
            style={"display": "flex"},
            children=[
                html.Div(id="graph-id", className="col s12 m6"),
                html.Div(id="map-id", className="col s12 m6")
            ]
        )
    ])