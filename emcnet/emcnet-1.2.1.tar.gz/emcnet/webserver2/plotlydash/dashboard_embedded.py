import dash
import dash_core_components as dcc
import dash_html_components as html
# from dash.dependencies import Input, Output
import sqlite3
import datetime
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import time
import fieldday
from emcnet.device import vedirect_types as vedirect_types
from collections import OrderedDict
import fifeutil.interval as interval
import argparse
from codetiming import Timer
from dotenv import load_dotenv
import os
from enum import Enum

# log = logging.getLogger(__name__)

field_rename = {
    'V_first': 'V',
    'I_first': 'I',
    'P_first': 'P',
    'batteryVoltage_first': 'batteryVoltage',
    'panelVoltage_first': 'panelVoltage',
    'panelPower_first': 'panelPower',
    'batteryCurrent_first': 'batteryCurrent',
    'loadCurrent_first': 'loadCurrent',
    'load_first': 'load',
    'relayState_first': 'relayState',
    'yieldTotal_first': 'yieldTotal',
    'yieldToday_first': 'yieldToday',
    'maximumPowerToday_first': 'maximumPowerToday',
    'yieldYesterday_first': 'yieldYesterday',
    'maximumPowerYesterday_first': 'maximumPowerYesterday',
    'error_first': 'error',
    'mode_first': 'mode',
    'firmwareVersion_first': 'firmwareVersion',
    'productId_first': 'productId',
    'serialNumber_first': 'serialNumber',
    'daySequenceNumber_first': 'daySequenceNumber',
    'trackerMode_first': 'trackerMode'
}

fieldtypes_now = OrderedDict([
    ('V', (fieldday.FieldFloat, {'desc': 'Camper battery voltage', 'units': 'V', 'fmt': '.3f'})),
    ('I', (fieldday.FieldFloat, {'desc': 'Camper battery current consumption', "units": 'A', 'fmt': '.3f'})),
    ('P', (fieldday.FieldFloat, {'desc': 'Camper battery net power consumption', "units": 'W', 'fmt': '.1f'}))
])
# add the Victron types
fieldtypes_now.update(vedirect_types.fieldTypes)

# fieldtypes_interval = OrderedDict([
#     ('V_first', (fieldday.FieldFloat, {'desc': 'Camper voltage', 'units': 'V', 'fmt': '.3f'})),
#     ('P_avg', (fieldday.FieldFloat, {'desc': 'Camper net power', "units": 'W', 'fmt': '.1f'})),
#     ('batteryVoltage_avg',
#      (fieldday.FieldInt, {'desc': 'Main or channel 1 (battery) voltage', 'units': 'mV', 'fmt': 'd'})),
#     ('batteryCurrent_avg',
#      (fieldday.FieldInt, {'desc': 'Main or channel 1 battery current', 'units': 'mA', 'fmt': 'd'})),
# ])


def conv_float_mv_to_v(field):
    field.value = float(field.value) / 1000.0
    field.units = 'V'
    field.fmt = '.3f'


def conv_float_ma_to_a(field):
    field.value = float(field.value) / 1000.0
    field.units = 'A'
    field.fmt = '.3f'


def conv_float_01kwh_to_kwh(field):
    field.value = float(field.value) / 100.0
    field.units = 'kWh'
    field.fmt = '.2f'


convertlist = [[fieldday.FieldFloat, conv_float_mv_to_v, lambda x: x.units == 'mV'],
               [fieldday.FieldFloat, conv_float_ma_to_a, lambda x: x.units == 'mA'],
               [fieldday.FieldInt, conv_float_mv_to_v, lambda x: x.units == 'mV'],
               [fieldday.FieldInt, conv_float_ma_to_a, lambda x: x.units == 'mA'],
               [fieldday.FieldInt, conv_float_01kwh_to_kwh, lambda x: x.units == '0.01 kWh']]


def flatten_dict(d):
    d2 = d['data']
    d2['ts'] = d['ts']
    return d2


class DatabaseType(Enum):
    SITE = 1
    SERVER = 2


class LoadDataException(Exception):
    pass


def init_dashboard(server):
    # set the default path to the EMCNET directory - from the environment if set
    emcnetdir = os.getenv("EMCNETDIR", '../').rstrip('/')
    load_dotenv(emcnetdir + '/config.env', override=True)
    # site_id=os.getenv("SITE_ID", 'defaultsiteid')
    site_id='bigbird'
    maxrecords=int(os.getenv("MAX_PLOT_RECORDS", 672))
    loglevel=os.getenv("EMCNET_LOG_LEVEL", 'INFO')

    """Create a Plotly Dash dashboard."""
    app = dash.Dash(
        server=server,
        routes_pathname_prefix="/dashapp/",
        external_stylesheets=[
            "/static/dist/css/styles.css",
            "https://fonts.googleapis.com/css?family=Lato",
        ],
    )

    # Use a stylesheet
    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    # Step 1. Launch the application
    # app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app = dash.Dash(__name__)
    app.logger.setLevel(loglevel.upper())

    # Step 2. Import the dataset
    def load_data():
        t = Timer(name="load data from " + emcnetdir + "/emcnet.sqlite3" + "...",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        site_db_full_path = emcnetdir + f"/{site_id}.sqlite3"
        app.logger.debug(f"in {os.getcwd()}")
        app.logger.debug(f"attempting to open {site_db_full_path}")
        if os.path.exists(site_db_full_path):
            con = sqlite3.connect(site_db_full_path)
            database_type = DatabaseType.SITE
            # member = Color.RED
            app.logger.info(f"Opening server database {site_db_full_path}")
        else:
            server_db_full_path = emcnetdir + f"/emcnet.sqlite3"
            app.logger.debug(f"attempting to open {server_db_full_path}")
            if os.path.exists(server_db_full_path):
                con = sqlite3.connect(server_db_full_path)
                database_type = DatabaseType.SERVER
                app.logger.info(f"Opening server database {server_db_full_path}")
            else:
                app.logger.error(f"No database found ({site_db_full_path} or {server_db_full_path})")
                raise FileNotFoundError(f"No database found ({site_db_full_path} or {server_db_full_path})")
        # try:
        #     con = sqlite3.connect(database_path + f"{site_id}.sqlite3")
        # except pd.io.sql.DatabaseError:
        #     try:
        #         con = sqlite3.connect(database_path + "emcnet.sqlite3")
        #     except pd.io.sql.DatabaseError:
        #         app.logger.error(f"No database found ({site_id}.sqlite3 or emcnet.sqlite3)")
        #         return
        #     else:
        #         site_database = False
        # else:
        #     site_database = True

        # read last maxrecords the fastest way possible.
        # See https://stackoverflow.com/questions/14018394/android-sqlite-query-getting-latest-10-records
        if database_type == DatabaseType.SITE:
            table_interval = 'interval'
            table_now = 'now'
        else:
            table_interval = 'interval_' + site_id
            table_now = 'now_' + site_id
        try:
            df_interval = pd.read_sql_query(f"SELECT * from {table_interval} LIMIT {maxrecords:d}"
                                            f" OFFSET (SELECT COUNT(*) FROM {table_interval})-{maxrecords:d}", con)
        except pd.io.sql.DatabaseError:
            app.logger.error(f"Could not read data from table {table_interval}")
            raise LoadDataException(f"Could not read data from table {table_interval}")
        try:
            df_now = pd.read_sql_query(f"SELECT * from {table_now}", con)
        except pd.io.sql.DatabaseError:
            app.logger.debug(f"Table {table_now} not found - using last interval data record")
            dict_now = df_interval.to_dict('records')[-1]
        else:
            dict_now = dict()
            for index, row in df_now.iterrows():
                dict_now[row['key']] = row['value']
        con.close()
        t.stop()

        t = Timer(name="localize timespamps",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        df_interval['Date'] = pd.to_datetime(df_interval['ts'], unit='s')
        df_interval.set_index('Date', inplace=True)
        tzlocal = datetime.datetime.now().astimezone().tzinfo
        df_interval.index = df_interval.index.tz_localize('UTC').tz_convert(tzlocal)
        t.stop()

        # t = Timer(name="sort time series dataframe",
        #           text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        # t.start()
        # # sort the dataframe because our SQL query returned the records in descending order
        # df_interval.sort_index(inplace=True)
        # t.stop()

        t = Timer(name="mark data gaps",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        df_interval_gapsmarked = interval.mark_gaps_boi(df_interval)
        t.stop()

        t = Timer(name="make interval data show as constant over intervals",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        (t_plot_p, p_plot_net) = interval.to_plottable_interval_timeseries_boi(df_interval_gapsmarked['P_avg'])
        (t_plot_p, p_plot_pv) = interval.to_plottable_interval_timeseries_boi(
            -df_interval_gapsmarked['batteryCurrent_avg'] * df_interval_gapsmarked['batteryVoltage_avg'] / 1e6)
        t.stop()

        t = Timer(name="prepare battery state data",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        # (t_plot_v, v_load) = interval.to_plottable_interval_timeseries_boi(df_interval_gapsmarked['V_first'])
        # (t_plot_v, v_vmppt) = interval.to_plottable_interval_timeseries_boi(df_interval_gapsmarked['batteryVoltage_first'] / 1e3)
        t_plot_v = df_interval_gapsmarked.index
        v_load = df_interval_gapsmarked['V_first'].values
        v_vmppt = df_interval_gapsmarked['batteryVoltage_first'].values / 1e3
        t.stop()

        return dict_now, df_interval, t_plot_p, p_plot_net, p_plot_pv, t_plot_v, v_load, v_vmppt

    # Step 3. Create a plotly figure
    # trace_1 = go.Scatter(x=df.index, y=df['Voltage_V'],
    #                      name='Voltage (V)',
    #                      line=dict(width=2,
    #                                 color='rgb(229, 151, 50)'))
    # trace_1 = go.Scatter(x=df.index, y=df['Voltage_V'], name='Voltage (V)', secondary_y=False)
    # trace_2 = go.Scatter(x=df.index, y=df['Current_mA'] / 1000, name='Current (A)', secondary_y=True)
    # layout = go.Layout(title='Battery State',
    #                    hovermode='closest')
    # fig = go.Figure(data=[trace_1, trace_2], layout=layout)
    def setup_figs(t_plot_p, p_plot_net, p_plot_pv, t_plot_v, v_load, v_vmppt):
        t = Timer(name="set up figures",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        fig_power = make_subplots()
        fig_power.add_trace(go.Scatter(x=t_plot_p, y=p_plot_pv, name='PV (W)'))
        fig_power.add_trace(go.Scatter(x=t_plot_p, y=p_plot_net, name='Net Power (W)'))
        fig_power.update_layout(
            {"title_text": "System Power"}
        )
        fig_power.update_xaxes(range=[np.amin(t_plot_p), np.amax(t_plot_p)])
        fig_power.update_yaxes(title_text="Power (W)")
        fig_power.update_layout(legend=dict(x=0, y=1.1), legend_orientation="h")
        #
        fig_state = make_subplots()
        fig_state.add_trace(go.Scatter(x=t_plot_v, y=v_load, name='Voltage at Load Dist. (V)'))
        fig_state.add_trace(go.Scatter(x=t_plot_v, y=v_vmppt, name='Voltage at VMPPT (V)'))
        fig_state.update_layout(
            {"title_text": "Battery State"}
        )
        fig_state.update_xaxes(range=[np.amin(t_plot_v), np.amax(t_plot_v)])
        fig_state.update_yaxes(title_text="Voltage (V)", range=[11.0, 15.0])
        fig_state.update_layout(legend=dict(x=0, y=1.1), legend_orientation="h")
        t.stop()
        return fig_power, fig_state

    def generate_table(d, fieldtypes_dict, renamefields_dict=None, convert=None):
        t = Timer(name="generate tables",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        d = fieldday.FieldSet(d, rename_dict=renamefields_dict, field_types=fieldtypes_dict)
        if convert is not None:
            d.modify_types(convert)
        d.pop('ts', '')
        rows = []
        for key in fieldtypes_dict:
            if key in d:
                rows.append(html.Tr([
                    html.Th(key, scope="row",
                            style={"background-color": "#E5ECF6",
                                   "border": "1px solid black",
                                   "padding": "5px"}),
                    html.Td((str(d[key]).split(': ')[-1]),
                            style={"border": "1px solid black",
                                   "padding": "5px"})]
                ))
        t.stop()
        return html.Table(rows, style={"border-collapse": "collapse",
                                       "border": "border: 1px solid black",
                                       "padding": "5px"})

    def generate_ts(dict_now):
        ts = dict_now['ts']
        tstring = "Local Time: " + time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime(ts))
        return html.Div(tstring)

    def generate_datatable(title, dict_now, fieldtypes_dict, rename_dict=None,
                           convert=None):
        return html.Div([
            html.H2(title),
            generate_ts(dict_now),
            generate_table(dict_now, fieldtypes_dict, renamefields_dict=rename_dict, convert=convert)
        ])

    # Create a Dash layout
    def generate_my_page_layout():
        # dict_now_ina226, dict_now_vmppt, vmppt_t_plot, vmppt_p_plot, ina226_t_plot, ina226_p_plot, \
        # ina226_t_instant, ina226_v_instant = load_data()
        try:
            dict_now, df_interval, t_plot_p, p_plot_net, p_plot_pv, t_plot_v, v_load, v_vmppt = load_data()
        except FileNotFoundError:
            return html.Div(html.H1(f"ERROR - no database for site {site_id}"))
        except LoadDataException:
            return html.Div(html.H1(f"ERROR loading data for site {site_id}"))
        else:
            fig_power, fig_state = setup_figs(t_plot_p, p_plot_net, p_plot_pv, t_plot_v, v_load, v_vmppt)
            return html.Div([
                # adding a header and a paragraph
                html.Div([
                    html.H1(f"Electrical System Monitor, Site: {site_id}"),
                    # html.P("Learning Dash is so interesting!!")
                ], ),
                # adding a plot
                dcc.Graph(id='plot_power', figure=fig_power),
                dcc.Graph(id='plot_state', figure=fig_state),
                generate_datatable('MOST RECENT DATA', dict_now, fieldtypes_now, rename_dict=field_rename,
                                   convert=convertlist),
            ])

    app.layout = generate_my_page_layout

    # Add callback functions

    # Return a reference to the server
    return app.server

