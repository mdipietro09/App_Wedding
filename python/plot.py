
import plotly.express as px
import numpy as np
import pandas as pd


class Plot():

    def __init__(self, dtf):
       self.dtf = self.prepare_data(dtf)  


    @staticmethod
    def prepare_data(dtf):
        ## mark the rules
        dtf["avoid"] = dtf["avoid"].apply(lambda x: dtf[dtf["id"]==x]["name"].iloc[0] if pd.notnull(x) else "none")
        dtf["symbol"] = dtf["avoid"].apply(lambda x: "o" if x == "none" else "x")

        ## create axis
        dtf_out = pd.DataFrame()
        lst_tables = []
        for t in dtf["table"].unique():
            dtf_t = dtf[dtf["table"]==t]
            n = len(dtf_t)
            theta = np.linspace(0, 2*np.pi, n)
            dtf_t["x"] = 1*np.cos(theta)
            dtf_t["y"] = 1*np.sin(theta)
            dtf_out = dtf_out.append(dtf_t)

        return dtf_out.reset_index(drop=True).sort_values("table")     


    def plot(self):
        fig = px.scatter(self.dtf, x="x", y="y", color="category", hover_name="name", facet_col="table", facet_col_wrap=3, #symbol="symbol"
                         hover_data={"x":False, "y":False, "category":True, "avoid":True, "symbol":False, "table":False})

        fig.add_shape(type="circle", opacity=0.1, fillcolor="black", col="all", row="all", exclude_empty_subplots=True,
                      x0=self.dtf["x"].min(), y0=self.dtf["y"].min(), x1=self.dtf["x"].max(), y1=self.dtf["y"].max())

        fig.update_layout(plot_bgcolor='white', legend={"bordercolor":"black", "borderwidth":1, "orientation":"h"})
        fig.update_yaxes(visible=False)
        fig.update_xaxes(visible=False)
        return fig
