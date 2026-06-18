import pandas as pd
import plotly.express as px
import dash_leaflet as dl
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output

from filters import get_rescue_query
from scoring import rank_dogs_by_suitability


def register_callbacks(app, db, original_df):

    @app.callback(
        Output("datatable-id", "data"),
        [
            Input("filter-type", "value"),
            Input("preferred-breeds", "value"),
            Input("min-age", "value"),
            Input("max-age", "value"),
            Input("preferred-sex", "value"),
            Input("breed-weight", "value"),
            Input("age-weight", "value"),
            Input("sex-weight", "value")
        ]
    )
    def update_dashboard(
        filter_type,
        preferred_breeds,
        min_age,
        max_age,
        preferred_sex,
        breed_weight,
        age_weight,
        sex_weight
    ):

        query = get_rescue_query(filter_type)
        records = db.read(query)

        if not records:
            return []

        preferred_breeds = preferred_breeds or []
        min_age = min_age if min_age is not None else 0
        max_age = max_age if max_age is not None else 9999

        breed_weight = breed_weight if breed_weight is not None else 0
        age_weight = age_weight if age_weight is not None else 0
        sex_weight = sex_weight if sex_weight is not None else 0

        ranked_records = rank_dogs_by_suitability(
            records,
            preferred_breeds,
            min_age,
            max_age,
            preferred_sex,
            breed_weight,
            age_weight,
            sex_weight
        )

        dff = pd.DataFrame.from_records(ranked_records)

        if dff.empty:
            return []

        if "_id" in dff.columns:
            dff = dff.drop(columns=["_id"])

        return dff.to_dict("records")

    @app.callback(
        Output("breed-summary-table", "children"),
        [Input("datatable-id", "data")]
    )
    def update_breed_summary(_):
        summary_data = db.get_breed_statistics(limit=10)

        if not summary_data:
            return html.P("No breed summary data available.")

        return dash_table.DataTable(
            columns=[
                {"name": "Breed", "id": "breed"},
                {"name": "Count", "id": "count"}
            ],
            data=summary_data,
            page_size=10,
            style_table={"width": "500px", "overflowX": "auto"},
            style_cell={"textAlign": "left"},
            style_header={"fontWeight": "bold"}
        )

    @app.callback(
        Output("graph-id", "children"),
        [Input("datatable-id", "derived_virtual_data")]
    )
    def update_graphs(view_data):

        if view_data is None:
            dff = original_df
        else:
            dff = pd.DataFrame.from_dict(view_data)

        if dff.empty or "breed" not in dff.columns:
            return [html.P("No breed data available.")]

        fig = px.pie(
            dff,
            names="breed",
            title="Breed Distribution"
        )

        return [dcc.Graph(figure=fig)]

    @app.callback(
        Output("map-id", "children"),
        [
            Input("datatable-id", "derived_virtual_data"),
            Input("datatable-id", "derived_virtual_selected_rows")
        ]
    )
    def update_map(view_data, selected_rows):

        if view_data is None:
            dff = original_df
        else:
            dff = pd.DataFrame.from_dict(view_data)

        if dff.empty:
            return [html.P("No map data available.")]

        row = 0

        if selected_rows and selected_rows[0] < len(dff):
            row = selected_rows[0]

        lat_column = "location_lat"
        lon_column = "location_long"

        if lat_column not in dff.columns or lon_column not in dff.columns:
            return [html.P("Location data is unavailable.")]

        return [
            dl.Map(
                style={"width": "1000px", "height": "500px"},
                center=[30.75, -97.48],
                zoom=10,
                children=[
                    dl.TileLayer(id="base-layer-id"),
                    dl.Marker(
                        position=[
                            dff.iloc[row][lat_column],
                            dff.iloc[row][lon_column]
                        ],
                        children=[
                            dl.Tooltip(
                                str(
                                    dff.iloc[row].get(
                                        "breed",
                                        "Unknown breed"
                                    )
                                )
                            ),
                            dl.Popup([
                                html.H1("Animal Name"),
                                html.P(
                                    str(
                                        dff.iloc[row].get(
                                            "name",
                                            "Unknown"
                                        )
                                    )
                                )
                            ])
                        ]
                    )
                ]
            )
        ]

    @app.callback(
        Output("datatable-id", "style_data_conditional"),
        [Input("datatable-id", "selected_columns")]
    )
    def update_styles(selected_columns):

        if not selected_columns:
            return []

        return [
            {
                "if": {"column_id": column},
                "background_color": "#D2F3FF"
            }
            for column in selected_columns
        ]