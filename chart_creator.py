from matplotlib import pyplot as plt


class ChartCreator:
    def __init__(self):
        pass

    def clean(self, df, param, dateparam, start=None, end=None):
        cols = [param, dateparam]
        date_df = df[cols]
        datedropna_df = date_df.dropna()
        datedropna_df[dateparam] = datedropna_df[dateparam].astype("datetime64")
        if (start is not None) and (end is not None):
            startparam = datedropna_df[dateparam][start]
            endparam = datedropna_df[dateparam][end]
            filter_ts = (datedropna_df[dateparam] <= endparam) & (datedropna_df[dateparam] >= startparam)
            datedropna_filtered_df = datedropna_df[filter_ts]
            return datedropna_filtered_df
        else:
            return datedropna_df

    def plot_ts(self, df, param, dateparam):
        fig = plt.figure(figsize=(7.4, 2.5))
        plt.plot(df[dateparam], df[param], markersize=1)
        plt.tick_params(axis='x', labelsize=10, rotation=90)
        plt.title(param)
        plt.tight_layout()
        return fig