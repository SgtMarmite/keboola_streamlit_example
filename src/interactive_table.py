import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
import pandas as pd
from pathlib import Path


def interactive_table():
    query_df = pd.read_csv(st.session_state['uploaded_file'])
    st.header(f"📊 Explore {Path(st.session_state['uploaded_file']).name}")

    def aggrid_interactive_table(df: pd.DataFrame):
        """Creates an st-aggrid interactive table based on a dataframe.
        Args:
            df (pd.DataFrame]): Source dataframe
        Returns:
            dict: The selected row
        """
        options = GridOptionsBuilder.from_dataframe(
            df, enableRowGroup=True, enableValue=True, enablePivot=True
        )

        options.configure_side_bar()
        options.configure_selection("single")
        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            theme="streamlit",
            height=800,
            update_mode=GridUpdateMode.MODEL_CHANGED,
            allow_unsafe_jscode=True,
        )

        return selection  # return the selected row

    selection = aggrid_interactive_table(df=query_df)  # create the table
