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

field_rename_for_table = {
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


def run(site_id='defaultsite', emcnetdir="./", loglevel="WARNING", debug=False, maxrecords=672):
    emcnetdir = emcnetdir.rstrip('/') + '/'

    # Use a stylesheet
    # external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    # Step 1. Launch the application
    # app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
    app = dash.Dash(__name__, url_base_pathname='/emcnet/')
    app.logger.setLevel(loglevel.upper())

    # Step 2. Import the dataset
    def load_data(specified_site_id = site_id):
        t = Timer(name="load data from " + emcnetdir + "emcnet.sqlite3" + "...",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        site_db_full_path = emcnetdir + f"{specified_site_id}.sqlite3"
        app.logger.debug(f"in {os.getcwd()}")
        app.logger.debug(f"attempting to open {site_db_full_path}")
        if os.path.exists(site_db_full_path):
            con = sqlite3.connect(site_db_full_path)
            database_type = DatabaseType.SITE
            # member = Color.RED
            app.logger.info(f"Opening server database {site_db_full_path}")
        else:
            server_db_full_path = emcnetdir + f"emcnet.sqlite3"
            app.logger.debug(f"attempting to open {server_db_full_path}")
            if os.path.exists(server_db_full_path):
                con = sqlite3.connect(server_db_full_path)
                database_type = DatabaseType.SERVER
                app.logger.info(f"Opening server database {server_db_full_path}")
            else:
                app.logger.error(f"No database found ({site_db_full_path} or {server_db_full_path})")
                raise FileNotFoundError(f"No database found ({site_db_full_path} or {server_db_full_path})")
        # try:
        #     con = sqlite3.connect(database_path + f"{specified_site_id}.sqlite3")
        # except pd.io.sql.DatabaseError:
        #     try:
        #         con = sqlite3.connect(database_path + "emcnet.sqlite3")
        #     except pd.io.sql.DatabaseError:
        #         app.logger.error(f"No database found ({specified_site_id}.sqlite3 or emcnet.sqlite3)")
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
            table_interval = 'interval_' + specified_site_id
            table_now = 'now_' + specified_site_id
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

        # check to see if we have enough data to plot
        if len(df_interval) < 3:
            app.logger.error(f"Database does not contain enough data points to plot")
            raise LoadDataException(f"Database does not contain enough data points to plot")

        t = Timer(name="localize timespamps",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        df_interval['Date'] = pd.to_datetime(df_interval['ts'], unit='s')
        df_interval.set_index('Date', inplace=True)
        tzlocal = datetime.datetime.now().astimezone().tzinfo
        df_interval.index = df_interval.index.tz_localize('UTC').tz_convert(tzlocal)
        t.stop()

        t = Timer(name="mark data gaps",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        df_interval_gapsmarked = interval.mark_gaps_boi(df_interval)
        batt_power_avg = df_interval_gapsmarked['P_avg']
        batt_voltage_first = df_interval_gapsmarked['V_first']
        pv_batt_current_avg = df_interval_gapsmarked['batteryCurrent_avg']
        pv_batt_voltage_first = df_interval_gapsmarked['batteryVoltage_first']
        pv_batt_voltage_avg = df_interval_gapsmarked['batteryVoltage_avg']
        if batt_power_avg.dtype != 'float64':
            batt_power_avg.fillna(np.NAN, inplace=True)
        if pv_batt_voltage_first.dtype != 'float64':
            pv_batt_voltage_first.fillna(np.NAN, inplace=True)
        if pv_batt_current_avg.dtype != 'float64':
            pv_batt_current_avg.fillna(np.NAN, inplace=True)
        if pv_batt_voltage_first.dtype != 'float64':
            pv_batt_voltage_first.fillna(np.NAN, inplace=True)
        if pv_batt_voltage_avg.dtype != 'float64':
            pv_batt_voltage_avg.fillna(np.NAN, inplace=True)
        (t_plot_p, p_plot_pv) = interval.to_plottable_interval_vectors_boi(
            -pv_batt_current_avg * pv_batt_voltage_avg / 1e6)
        t.stop()

        t = Timer(name="make interval data show as constant over intervals",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        (t_plot_p, p_plot_net) = interval.to_plottable_interval_vectors_boi(batt_power_avg)
        (t_plot_p, p_plot_pv) = interval.to_plottable_interval_vectors_boi(
            -pv_batt_current_avg * pv_batt_voltage_avg / 1e6)
        t.stop()

        t = Timer(name="prepare battery state data",
                  text="{name}: {milliseconds:.1f}ms", logger=app.logger.info)
        t.start()
        # (t_plot_v, v_load) = interval.to_plottable_interval_timeseries_boi(df_interval_gapsmarked['V_first'])
        # (t_plot_v, v_vmppt) = interval.to_plottable_interval_timeseries_boi(df_interval_gapsmarked['batteryVoltage_first'] / 1e3)
        t_plot_v = df_interval_gapsmarked.index
        v_load = batt_voltage_first.values
        v_vmppt = pv_batt_voltage_first.values / 1e3
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
    def generate_site_layout(specified_site_id):
        # dict_now_ina226, dict_now_vmppt, vmppt_t_plot, vmppt_p_plot, ina226_t_plot, ina226_p_plot, \
        # ina226_t_instant, ina226_v_instant = load_data()
        try:
            dict_now, df_interval, t_plot_p, p_plot_net, p_plot_pv, t_plot_v, v_load, v_vmppt \
                = load_data(specified_site_id)
        except FileNotFoundError:
            return html.Div(html.H1(f"ERROR - no database for site {specified_site_id}"))
        except LoadDataException:
            return html.Div(html.H1(f"ERROR loading data for site {specified_site_id}"))
        else:
            fig_power, fig_state = setup_figs(t_plot_p, p_plot_net, p_plot_pv, t_plot_v, v_load, v_vmppt)
            return html.Div([
                # adding a header and a paragraph
                html.Div([
                    html.H1(f"Electrical System Monitor"),
                    html.H2(f"Site: {specified_site_id}"),
                    html.Div(id='pname')
                    # html.P("Learning Dash is so interesting!!")
                ], ),
                # adding a plot
                dcc.Graph(id='plot_power', figure=fig_power),
                dcc.Graph(id='plot_state', figure=fig_state),
                generate_datatable('MOST RECENT DATA', dict_now, fieldtypes_now, rename_dict=field_rename_for_table,
                                   convert=convertlist),
            ])

    # Create a Dash layout
    def generate_my_page_layout():
        return html.Div([
            # represents the URL bar, doesn't render anything
            dcc.Location(id='url', refresh=False),
            # content will be rendered in this element
            html.Div(id='render-for-specific-site')])

    # Add callback functions
    @app.callback(dash.dependencies.Output('render-for-specific-site', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
    def display_page(pathname):
        # default site ID is set either by environment variable or on the command line
        # but can be over-ridden by the URL
        site_id_to_use = site_id
        if isinstance(pathname, str):
            pathname_splitted = str(pathname).lstrip('/').rstrip('/').split('/')
            if len(pathname_splitted) == 2:
                # override the site ID - use the site_id from the URL
                site_id_to_use = pathname_splitted[-1]
        return html.Div([
            generate_site_layout(site_id_to_use)
    ])

    app.title = "EMCNet"
    app.layout = generate_my_page_layout

    # Run the server
    if not debug:
        app.run_server(host='0.0.0.0')


def main():
    # set the default path to the EMCNET directory - from the environment if set
    emcnetdir = os.getenv("EMCNETDIR", './').rstrip('/')
    load_dotenv(emcnetdir + '/config.env', override=True)
    # read command-line arguments and override environment variables if given
    parser = argparse.ArgumentParser(description='EMCNet Dashboard')
    parser.add_argument('--site_id', type=str, default=os.getenv("SITE_ID", 'defaultsiteid'), help='Site ID')
    parser.add_argument('--emcnetdir', dest='emcnetdir', default=emcnetdir, help='Path to emcnet files')
    parser.add_argument('--maxrecords', dest='maxrecords', type=int, default=os.getenv("MAX_PLOT_RECORDS", 672),
                        help='Maximum records to plot')
    parser.add_argument('--loglevel', help='logging level one of [DEBUG, INFO, WARNING, ERROR, CRITICAL]',
                        default=os.getenv("EMCNET_LOG_LEVEL", 'INFO'))

    args = parser.parse_args()
    # logging.basicConfig(level=args.loglevel.upper())
    print("EMCNet Dashboard")
    run(site_id=args.site_id, emcnetdir=args.emcnetdir, loglevel=args.loglevel, debug=False,
        maxrecords=args.maxrecords)


# Step 6. Add the server clause
if __name__ == '__main__':
    main()
