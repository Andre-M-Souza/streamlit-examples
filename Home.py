import streamlit as st
from streamlit_lightweight_charts import renderLightweightCharts
import streamlit_lightweight_charts.dataSamples as data
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib import colors
from matplotlib.ticker import PercentFormatter
import numpy as np
import pandas as pd
import altair as alt

st.set_page_config(layout='wide')


def run_again():
    pass


with st.sidebar:

    option = st.selectbox(
        'Mês / Ano ?',
        ('12/2023', '11/2023', '10/2023', '09/2023', '08/2023'),
        on_change=run_again())


# Chart 01
# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
sizes = [15, 30, 45, 10]
explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

# Chart 02
# Bar chart
fruits = ['apple', 'blueberry', 'cherry', 'orange']
counts = [40, 100, 30, 55]
bar_labels = ['red', 'blue', '_red', 'orange']
bar_colors = ['tab:red', 'tab:blue', 'tab:red', 'tab:orange']

# Chart 03
species = ('Adelie', 'Chinstrap', 'Gentoo')
sex_counts = {
    'Male': np.array([73, 34, 61]),
    'Female': np.array([73, 34, 58])}
width = 0.6  # the width of the bars: can also be len(x) sequence

# Chart 04
category_names = ['Disagree',
                  'Neither agree nor disagree', 'Agree']
results = {
    'Question 1': [10, 35, 55],
    'Question 2': [55, 35, 10],
    'Question 3': [20, 30, 50],
}


def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig4, ax4 = plt.subplots(figsize=(5, 5))
    ax4.invert_yaxis()
    ax4.xaxis.set_visible(False)
    ax4.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax4.barh(labels, widths, left=starts, height=0.5,
                         label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax4.bar_label(rects, label_type='center', color=text_color)

    ax4.legend(ncols=len(category_names), bbox_to_anchor=(0, 1),
               loc='lower left', fontsize='small')

    return fig4, ax4


# Chart 05
# Create a random number generator with a fixed seed for reproducibility
rng = np.random.default_rng(19680801)
N_points = 100000
n_bins = 20
dist1 = rng.standard_normal(N_points)

# Chart 06
x = np.linspace(-1, 1, 50)
y1 = 2*x + 1
y2 = 2**x + 1

# Chart 07


# Load styles...
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Title...
st.title(f'Dashboard - KPI(s): {option}')

# Main Container.....
with st.container(border=True):

    col1, col2, col3, col4, col5 = st.columns(5, gap='large')

    with col1:

        with st.container(border=True):

            st.markdown('Good Catches / Near Misses')
            st.metric('registros :sunglasses:', value='54', delta='52')

            fig1, ax1 = plt.subplots()
            ax1.pie(sizes, explode=explode, labels=labels,
                    autopct='%1.1f%%', shadow=True, startangle=90)
            # Equal aspect ratio ensures that pie is drawn as a circle.
            ax1.axis('equal')

            st.pyplot(fig1)

    with col2:

        with st.container(border=True):

            st.markdown('RFT')
            st.metric('blablabla :+1:', value='80 %', delta='85 %')

            fig2, ax2 = plt.subplots()
            ax2.bar(fruits, counts, label=bar_labels, color=bar_colors)

            ax2.set_ylabel('fruit supply')
            ax2.set_title('Fruit supply by kind and color')
            ax2.legend(title='Fruit color')

            st.pyplot(fig2)

    with col3:

        with st.container(border=True):

            st.markdown('Reclamação de Cliente')
            st.metric('registros :sunglasses:', value='54', delta='52')

            fig3, ax3 = plt.subplots()
            bottom = np.zeros(3)

            for sex, sex_count in sex_counts.items():
                p = ax3.bar(species, sex_count, width,
                            label=sex, bottom=bottom)
                bottom += sex_count

                ax3.bar_label(p, label_type='center')

            ax3.set_title('Number of penguins by sex')
            ax3.legend()

            st.pyplot(fig3)

    with col4:

        with st.container(border=True):

            st.markdown('Cycle Time')
            st.metric('registros :sunglasses:', value='54', delta='52')

            fig4, ax4 = survey(results, category_names)
            st.pyplot(fig4)

    with col5:

        with st.container(border=True):

            st.markdown('Schedule Adherence')
            st.metric('registros :sunglasses:', value='54', delta='52')

            # Generate one normal distribution
            dist1 = rng.standard_normal(N_points)
            fig5, ax5 = plt.subplots(1, 1, sharey=True, tight_layout=True)
            # We can set the number of bins with the *bins* keyword argument.
            ax5.hist(dist1, bins=n_bins)
            st.pyplot(fig5)

with st.container(border=True):

    col6, col7, col8, col9, col10 = st.columns(5, gap='large')

    with col6:

        with st.container(border=True):

            st.markdown('Volume de Produção')
            st.metric('registros :sunglasses:', value='54', delta='52')

            fig6 = plt.figure()
            ax6 = fig6.add_subplot(1, 1, 1)
            ax6.plot(x, y1)
            ax6.set_xlabel("I am x")
            ax6.set_ylabel("I am y")
            ax6.set_title("with labels")

            st.pyplot(fig6)

    with col7:

        with st.container(border=True):

            st.markdown('Custo por Litro')
            st.metric('registros :sunglasses:', value='54', delta='52')

            chart_data = pd.DataFrame(
                np.random.randn(20, 3), columns=["a", "b", "c"])

            c = (
                alt.Chart(chart_data)
                .mark_circle()
                .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
            )

            st.altair_chart(c, use_container_width=True)

    with col8:

        with st.container(border=True):

            st.markdown('OTIF')
            st.metric('registros :sunglasses:', value='54', delta='52')

            df = pd.DataFrame(
                np.random.randn(5, 2) / [50, 50] +
                [-23.46411077802282, -46.46128453747276],
                columns=['lat', 'lon'])

            st.map(df)

    with col9:

        with st.container(border=True):

            st.markdown('Hora Extra')
            st.metric('registros :sunglasses:', value='54', delta='52')

            chart_data = pd.DataFrame(
                {
                    "col1": np.random.randn(10),
                    "col2": np.random.randn(10),
                    "col3": np.random.choice(["A", "B", "C"], 10),
                }
            )

            st.area_chart(chart_data, x="col1", y="col2", color="col3")

    with col10:

        with st.container(border=True):

            st.markdown('Absenteísmo')
            st.metric('registros :-1:', value='54', delta='52')

            priceVolumeChartOptions = {
                "height": 300,
                "rightPriceScale": {
                    "scaleMargins": {
                        "top": 0.2,
                        "bottom": 0.25,
                    },
                    "borderVisible": False,
                },
                "overlayPriceScales": {
                    "scaleMargins": {
                        "top": 0.7,
                        "bottom": 0,
                    }
                },
                "layout": {
                    "background": {
                        "type": 'solid',
                        "color": '#131722'
                    },
                    "textColor": '#d1d4dc',
                },
                "grid": {
                    "vertLines": {
                        "color": 'rgba(42, 46, 57, 0)',
                    },
                    "horzLines": {
                        "color": 'rgba(42, 46, 57, 0.6)',
                    }
                }
            }

            priceVolumeSeries = [
                {
                    "type": 'Area',
                    "data": data.priceVolumeSeriesArea,
                    "options": {
                        "topColor": 'rgba(38,198,218, 0.56)',
                        "bottomColor": 'rgba(38,198,218, 0.04)',
                        "lineColor": 'rgba(38,198,218, 1)',
                        "lineWidth": 2,
                    }
                },
                {
                    "type": 'Histogram',
                    "data": data.priceVolumeSeriesHistogram,
                    "options": {
                        "color": '#26a69a',
                        "priceFormat": {
                            "type": 'volume',
                        },
                        "priceScaleId": ""  # set as an overlay setting,
                    },
                    "priceScale": {
                        "scaleMargins": {
                            "top": 0.7,
                            "bottom": 0,
                        }
                    }
                }
            ]

            renderLightweightCharts([
                {
                    "chart": priceVolumeChartOptions,
                    "series": priceVolumeSeries
                }
            ], 'priceAndVolume')
