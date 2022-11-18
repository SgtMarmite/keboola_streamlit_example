import streamlit as st
from st_aggrid import GridOptionsBuilder
import pandas as pd
import math


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def render_stats():
    query_df = pd.read_csv(st.session_state['extracted_file'])
    query_df['time'] = pd.to_datetime(query_df['time'], unit='s')

    stats = ["cpu_percent", "ram_percent", "interval_net_in", "interval_net_out", "total_net_in", "total_net_out"]

    def aggrid_interactive_graph(df: pd.DataFrame, field):
        """Creates a graph based on a dataframe.
        Args:
            df (pd.DataFrame): Source dataframe
            field (string): name of the stat to print
        Returns:
            dict: The selected row
        """
        st.header(f"📊 Stat: {field}")
        options = GridOptionsBuilder.from_dataframe(
            df, enableRowGroup=True, enableValue=True, enablePivot=True
        )

        options.configure_side_bar()
        options.configure_selection("single")

        return st.line_chart(data=df, x="time", y=field)

    for stat in stats:
        aggrid_interactive_graph(df=query_df, field=stat)  # create the table

    formated_columns = ["ram_used", "interval_net_in", "interval_net_out", "total_net_in", "total_net_out"]
    for col in formated_columns:
        query_df[col] = query_df[col].apply(convert_size)

    st.write(query_df)
