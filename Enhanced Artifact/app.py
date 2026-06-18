import logging
import pandas as pd
from dash import Dash

from config import APP_PORT
from database import AnimalShelter
from layout import create_layout
from callbacks import register_callbacks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_data(db):
    records = db.read({})
    df = pd.DataFrame.from_records(records)

    if df.empty:
        logger.warning("No records found in database.")
        return df

    if "_id" in df.columns:
        df = df.drop(columns=["_id"])

    return df


def create_app():
    db = AnimalShelter()
    df = load_data(db)

    app = Dash(__name__)
    app.title = "Grazioso Salvare Dashboard"

    app.layout = create_layout(df)
    register_callbacks(app, db, df)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=APP_PORT)