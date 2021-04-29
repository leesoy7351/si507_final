
#########################################
##### Name: Soyoung Lee             #####
##### Uniqname: soyolee             #####
#########################################

from flask import Flask, render_template, request, redirect, flash
import sqlite3
from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import plotly.graph_objects as go
import sqlite3
import plotly.express as px
import secrets

app = Flask(__name__)

app.secret_key = secrets.FALSK_SECRETE_KEY

def get_data(query):
    conn = sqlite3.connect('mass_shooting_us.sqlite')
    cur = conn.cursor()
    lst = cur.execute(query).fetchall()
    conn.close()
    return lst

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/heatmap')
def heatmap_select():
    return render_template('heatmap_select.html')

@app.route('/heatmap/result', methods=['POST'])
def heatmap_result():

    year_heatmap = request.form['year_heatmap']
    q = f'''SELECT c.code, d.state, count(d.id), sum(injured), sum(dead), sum(total)
    FROM mass_shooting_us d join us_code c on c.state_name = d.state
    WHERE year = {year_heatmap} group by state'''
    result_heatmap = get_data(q)

    df_1= pd.DataFrame(result_heatmap, columns = ['code', 'state', 'count', 'injured', 'dead', 'total'])
    df_1['injured'] = df_1['injured'].astype(int)
    df_1['dead'] = df_1['dead'].astype(int)
    df_1['total'] = df_1['total'].astype(int)

    for col in df_1.columns:
        df_1[col] = df_1[col].astype(str)

    df_1['text'] = df_1['state'] + '<br>' + \
        'total ' + df_1['total'] + '<br>' + \
        'dead ' + df_1['dead'] + ' injured ' + df_1['injured'] + '<br>'

    fig = go.Figure(data=go.Choropleth(
        locations=df_1['code'],
        z=df_1['count'].astype(int).round(0),
        locationmode='USA-states',
        colorscale='Blues',
        autocolorscale=False,
        text=df_1['text'],
        marker_line_color='white',
        colorbar_title="# of incidents"
    ))

    fig.update_layout(
        title_text=f'The number of incidents across states in {year_heatmap} <br>(Hover for # the victims)',
        geo = dict(
            scope='usa',
            projection=go.layout.geo.Projection(type = 'albers usa'),
            showlakes=True, # lakes
            lakecolor='rgb(255, 255, 255)'),
    )
    div = fig.to_html(full_html=False)
    return render_template('heatmap_result.html', heatmap_div=div)

@app.route('/line')
def line_select():
    return render_template('line_select.html')

@app.route('/line/result', methods=['POST'])
def line_result():

    state_line = request.form['state_line']
    try:
        q = f'''SELECT state, year, sum(injured), sum(dead), sum(total) FROM mass_shooting_us where state = '{state_line}' COLLATE NOCASE group by year '''
        result_line = get_data(q)
    except:
        flash('Looks like you did not type the name of state properly!')
        return redirect('/line')

    if len(result_line) == 0 :
        flash('Looks like you did not type the name of state properly!')
        return redirect('/line')

    df_2= pd.DataFrame(result_line, columns = ['state', 'year', 'injured', 'dead', 'total'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=['2018', '2019', '2020', '2021'], y=df_2['injured'],
                        mode='lines+markers',
                        name='injured'))
    fig.add_trace(go.Scatter(x=['2018', '2019', '2020', '2021'], y=df_2['dead'],
                        mode='lines+markers',
                        name='dead'))
    fig.add_trace(go.Scatter(x=['2018', '2019', '2020', '2021'], y=df_2['total'],
                        mode='lines+markers', name='total',
                        line=dict(width=6)))

    fig.update_layout(title=f'The number of the victims in {state_line} over the last 3 years',
    xaxis_title='Year',
    yaxis_title='# of the victims',
        xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        showgrid=True,
        zeroline=True,
        showline=True,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
    ),
    autosize=True,
    margin=dict(
        autoexpand=True,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=True,
    plot_bgcolor='white',
    legend=dict(y=0.5, traceorder='reversed', font_size=16))

    div = fig.to_html(full_html=False)
    return render_template('line_result.html', line_div=div)


@app.route('/bar')
def bar_select():
    return render_template('bar_select.html')


@app.route('/bar/result', methods=['POST'])
def bar_result():
    state_bar = request.form['state_bar']
    try:
        q = f"SELECT city, sum(injured), sum(dead) FROM mass_shooting_us where state ='{state_bar}' COLLATE NOCASE group by city"
        result_bar = get_data(q)

    except:
        flash('Looks like you did not type the name of state properly!')
        return redirect('/bar')

    if len(result_bar) == 0 :
        flash('Looks like you did not type the name of state properly!')
        return redirect('/bar')

    df_3= pd.DataFrame(result_bar, columns = ['city', 'injured', 'dead'])
    fig = px.bar(df_3, x="city", y=["injured", "dead"], title=f'The number of the victims by cities in {state_bar} over the past 3 years',
    labels=dict(x="city", y="Total", color="Place"))
    fig.update_layout(xaxis={'categoryorder':'sum descending'})

    div = fig.to_html(full_html=False)
    return render_template('bar_result.html', bar_div=div)

@app.route('/table')
def table_select():
    return render_template('table_select.html')


@app.route('/table/result', methods=['POST'])
def table_result():

    year_table = request.form['year_table']
    q = f"SELECT date, state, city, injured, dead, total, description FROM mass_shooting_us where year = {year_table}"
    result_table = get_data(q)

    df_4= pd.DataFrame(result_table, columns = ['date', 'state', 'city', 'injured', 'dead', 'total', 'description'])

    fig = go.Figure(data=[go.Table(
        columnorder = [1, 2, 3, 4, 5, 6, 7],
        columnwidth = [80, 80, 80, 80, 80, 80, 200],
        header=dict(values=list(df_4.columns),
                    fill_color='royalblue',
                    font=dict(color='white', size=12),
                    line_color='royalblue',
                    align='center'),
        cells=dict(values=[df_4.date, df_4.state, df_4.city, df_4.injured, df_4.dead, df_4.total, df_4.description],
                fill_color='white',
                line_color='royalblue',
                align='left'))
    ])

    fig.update_layout(title=f'The list of US mass shootings in {year_table}')

    div = fig.to_html(full_html=False)
    return render_template('table_result.html', table_div=div)

if __name__ == '__main__':
    app.run(debug=True)