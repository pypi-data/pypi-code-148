import pandas as pd
import MySQLRead


def get_caliper():
    query = ('SELECT * '
             'FROM caliper')
    return MySQLRead.get_table(query)

def get_first_scan_blocks(date):
    query = ("SELECT plot_code, pp.project_plot_scan_date, project_type,project_plot_id "
             "FROM project AS pr "
             "INNER JOIN project_plot AS pp ON pr.project_id = pp.project_id "
             "INNER JOIN plot AS p ON pp.plot_id = p.plot_id "
             "WHERE (project_ordinal_number != 0 AND project_plot_scan_date = %s AND project_type != 3 AND project_type !=4)")
    df_ys = MySQLRead.get_table(query, params=(date,)).dropna()

    query = ("SELECT p.plot_code, pp.project_plot_scan_date, pr.project_type, ca.project_plot_id ,ca.scan_date "
             "FROM caliper AS ca "
             "LEFT JOIN project_plot AS pp ON (pp.project_plot_id = ca.project_plot_id) "
             "INNER JOIN project AS pr ON pr.project_id = pp.project_id "
             "INNER JOIN plot AS p ON pp.plot_id = p.plot_id "
             "WHERE (pr.project_ordinal_number != 0 AND ca.scan_date = %s AND pr.project_type != 3 AND pr.project_type !=4)")

    df_caliper = MySQLRead.get_table(query, params=(date,))
    df_caliper["project_plot_scan_date"] = df_caliper["scan_date"]
    df_caliper.drop('scan_date', axis=1, inplace=True)

    df = pd.concat([df_ys, df_caliper], axis=0).sort_values(["project_type"], ascending=True, ignore_index=True)
    # priority to YS over caliper if tow records on the same date
    df = df.drop_duplicates(subset=['plot_code'], ignore_index=True, keep='first')
    return df


def get_projects():
    # TODO change according caliper scans - later on - automatic
    query = ("SELECT customer_code, project_code ,project_id ,project_ordinal_number, pt.value AS type "
             "FROM customer AS c "
             "INNER JOIN project AS pr ON c.customer_id = pr.customer_id "
             "INNER JOIN project_type AS pt ON pt.id = pr.project_type "
             "WHERE pr.project_type = 1 OR pr.project_type = 2 "
             "ORDER BY customer_code")

    return MySQLRead.get_table(query)


def get_open_plots(project_id):
    # TODO change according caliper scans - later on - automatic

    query = (
        "SELECT pp.plot_id, p.project_season, pp.project_plot_scan_date FROM project AS p LEFT JOIN project_plot AS pp ON p.project_id = pp.project_id WHERE p.project_id = %s")

    query1 = ("SELECT scan1.project_plot_id ,plot_code,variety_name,"
              "scan1.project_plot_scan_date AS scan1_date,"
              "NULL AS scan2_date,"
              "scan1.project_plot_visual_fruit_size_medium AS scan1_avg_vis,"
              "NULL AS scan2_avg_vis,"
              "scan1.Visual_Size_Mod AS scan1_mod_vis,"
              "NULL AS scan2_mod_vis,"
              "scan1.Predicted_W  AS scan1_W_pred,"
              "NULL AS scan2_W_pred,"
              "NULL AS AccuWeight1ST2ND,"
              "NULL AS GrowthRate1ST2ND,"
              "AVG(cal.calibration_tree_fruit_count) AS ground_truth,"
              "scan1.AssumedPickingTime AS picking_time"
              " FROM (SELECT pp.project_plot_id,pr.project_code,pr.project_id,Visual_Size_Mod,project_season,Publish,"
              " plot_id,project_plot_scan_date,project_plot_visual_fruit_size_medium,Predicted_W, AssumedPickingTime"
              " FROM project AS pr INNER JOIN project_plot AS pp ON pr.project_id = pp.project_id"
              " WHERE pp.project_plot_id = %s) AS scan1 "
              " LEFT JOIN plot AS p ON p.plot_id = scan1.plot_id"
              " LEFT JOIN fruit_variety AS fv ON p.plot_fruit_variety= fv.variety_id"
              " LEFT JOIN calibration AS cal ON cal.plot_id = p.plot_id AND cal.project_id = scan1.project_id "
              # condition to find the open analysis plots
              # " WHERE (((scan1.Publish = 'Internal' OR scan1.Publish = 'NO') AND scan2.Publish IS NULL)"
              # " OR"
              # "(scan1.Publish = 'External' AND (scan2.Publish = 'Internal' OR scan2.Publish = 'NO')))"
              "GROUP BY scan1.project_plot_id ")

    # assuming 2nd scan has necceserly 1st scan
    query2 = ("SELECT "
              "scan2.project_plot_id ,plot_code,variety_name,"
              "scan1.project_plot_scan_date AS scan1_date,"
              "scan2.project_plot_scan_date AS scan2_date,"
              "scan1.project_plot_visual_fruit_size_medium AS scan1_avg_vis,"
              "scan2.project_plot_visual_fruit_size_medium AS scan2_avg_vis,"
              "scan1.Visual_Size_Mod AS scan1_mod_vis,"
              "scan2.Visual_Size_Mod AS scan2_mod_vis,"
              "scan1.Predicted_W  AS scan1_W_pred,"
              "scan2.Predicted_W  AS scan2_W_pred,"
              "1- (ABS(scan1.Predicted_W-scan2.Predicted_W)/scan2.Predicted_W) AS AccuWeight1ST2ND, "
              "(scan1.project_plot_visual_fruit_size_medium - scan2.project_plot_visual_fruit_size_medium)/DATEDIFF(scan1.project_plot_scan_date,scan2.project_plot_scan_date) AS GrowthRate1ST2ND, "
              "AVG(cal.calibration_tree_fruit_count) AS ground_truth,"
              "scan2.AssumedPickingTime AS picking_time"

              " FROM (SELECT pp.project_plot_id,pr.project_code,pr.project_id,Visual_Size_Mod,project_season,Publish,"
              " plot_id,project_plot_scan_date,project_plot_visual_fruit_size_medium,Predicted_W"
              " FROM project AS pr INNER JOIN project_plot AS pp ON pr.project_id = pp.project_id"
              " WHERE pp.project_plot_id = %s) AS scan1 "

              " INNER JOIN"

              "(SELECT pp.project_plot_id ,project_season,Publish,"
              " plot_id,project_plot_scan_date,project_plot_visual_fruit_size_medium,Visual_Size_Mod,Predicted_W,AssumedPickingTime"
              " FROM project AS pr INNER JOIN project_plot AS pp ON pr.project_id = pp.project_id"
              " WHERE (pp.project_plot_id = %s)) AS scan2"
              " ON scan1.plot_id = scan2.plot_id AND scan1.project_season = scan2.project_season "

              " INNER JOIN plot AS p ON p.plot_id = scan1.plot_id"
              " INNER JOIN fruit_variety AS fv ON p.plot_fruit_variety= fv.variety_id"
              " LEFT JOIN calibration AS cal ON cal.plot_id = p.plot_id AND cal.project_id = scan1.project_id "
              # condition to find the open analysis plots
              # " WHERE (((scan1.Publish = 'Internal' OR scan1.Publish = 'NO') AND scan2.Publish IS NULL)"
              # " OR"
              # "(scan1.Publish = 'External' AND (scan2.Publish = 'Internal' OR scan2.Publish = 'NO')))"
              "GROUP BY scan1.project_plot_id ")

    df = pd.DataFrame()
    for index, pp in MySQLRead.get_table(query, params=(project_id,)).iterrows():
        pp_ids = get_scans(pp['plot_id'], pp['project_season'], pp['project_plot_scan_date'])['project_plot_id']
        if len(pp_ids) == 2:
            # params in reversed order since later scan is on top
            plot = MySQLRead.get_table(query2, params=(pp_ids.loc[1], pp_ids.loc[0]))
            df = pd.concat([df, plot], axis=0)
        elif len(pp_ids) == 1:
            plot = MySQLRead.get_table(query1, params=(pp_ids.loc[0],))
            df = pd.concat([df, plot], axis=0)

    return df.reset_index()


def get_init_block(project_plot_id):
    query = (
        "SELECT p.plot_id ,pp.Packing_method, AssumedPickingTime,pr.project_code,c.customer_code,project_plot_scan_date ,plot_planting_year ,project_plot_visual_fruit_size_small ,"
        " project_plot_visual_fruit_size_medium ,project_plot_visual_fruit_size_large ,project_season ,"
        "plot_root_stock ,pr.customer_id AS customer_id ,plot_fruit_type ,plot_fruit_variety ,plot_soil ,plot_code,pr.project_type "
        " FROM project AS pr"
        " INNER JOIN project_plot AS pp ON pr.project_id = pp.project_id"
        " INNER JOIN plot AS p ON pp.plot_id = p.plot_id"
        " INNER JOIN customer AS c ON c.customer_id = pr.customer_id"
        " WHERE pp.project_plot_id = %s")
    return MySQLRead.get_table(query, params=(project_plot_id,))


def get_scans(plot_id, year, upper_date):
    query = ("SELECT * "
             " FROM customer as c "
             " INNER JOIN project AS pr ON c.customer_id = pr.customer_id"
             " INNER JOIN (SELECT project_plot_scan_date, project_id,plot_id,Packing_method,ModelID,project_plot_id FROM project_plot) AS pp ON pr.project_id = pp.project_id"
             " INNER JOIN plot AS p ON pp.plot_id = p.plot_id"
             " LEFT JOIN packing_metadata AS pm ON pp.Packing_method = pm.packingId"
             " WHERE (p.plot_id = %s AND project_season = %s AND project_type < 3 AND project_ordinal_number!=0 AND pp.project_plot_scan_date <= DATE(%s))")

    scans_ys = MySQLRead.get_table(query, params=(plot_id, year, f"\'{upper_date}\'"))

    query = ("SELECT * "
             "FROM caliper AS ca "
             "LEFT JOIN  (SELECT project_plot_scan_date, project_id,plot_id,Packing_method,ModelID,project_plot_id FROM project_plot) AS pp ON (pp.project_plot_id = ca.project_plot_id) "
             "INNER JOIN project AS pr ON pr.project_id = pp.project_id "
             "INNER JOIN customer as c ON c.customer_id = pr.customer_id "
             "LEFT JOIN packing_metadata AS pm ON pp.Packing_method = pm.packingId "
             "INNER JOIN plot AS p ON pp.plot_id = p.plot_id "
             "WHERE (p.plot_id = %s AND project_season = %s AND (project_type=5 OR project_type=6) AND project_ordinal_number!=0 AND ca.scan_date <= DATE(%s))")

    scans_caliper = MySQLRead.get_table(query, params=(plot_id, year, f"\'{upper_date}\'"))
    if not scans_caliper.empty:
        scans_caliper["project_plot_scan_date"] = scans_caliper["scan_date"]
        scans_caliper["project_plot_visual_fruit_size_medium"] = scans_caliper["average_size"]
        scans_caliper.drop(['scan_date', 'sample_size', 'average_size'], axis=1, inplace=True)

        scans = pd.concat([scans_ys, scans_caliper], axis=0).sort_values(["project_type"], ascending=False,
                                                                         ignore_index=True)
    else:
        scans = scans_ys
    # priority to YS over caliper if tow records on the same date
    scans = scans.drop_duplicates(subset=['plot_code', 'project_plot_scan_date'], ignore_index=True,
                                  keep='first').sort_values(["project_plot_scan_date"], ascending=False,
                                                            ignore_index=True)

    # return all scans with its
    return scans


def get_historical_packout(code, year):
    query = ("SELECT *  "
             "FROM packout AS pk "
             "INNER JOIN plot AS p ON p.plot_id = pk.plot_id "
             "WHERE (p.plot_code = %s AND pk.season = %s) ")

    return MySQLRead.get_table(query, params=(code, year))


def get_customer_info(id, col):
    query = "SELECT * FROM customer WHERE customer_id = %s"
    return MySQLRead.get_table(query, params=(id,))[col].iloc[0] if id != None else ''

def get_picking_date_by_fruit_variety(id):
    query = "SELECT * FROM fruit_variety WHERE variety_name = %s"
    return MySQLRead.get_table(query, params=(id))


def get_plot_coordinates(pp_id):
    query = ("SELECT p.plot_coordinates "
             "FROM plot AS p "
             "INNER JOIN project_plot AS pp ON pp.plot_id=p.plot_id "
             "WHERE pp.project_plot_id=%s ")
    return MySQLRead.get_table(query, params=(pp_id,))


def get_fruit_type(id):
    query = "SELECT value FROM fruit_type WHERE fruit_id = %s"
    return MySQLRead.get_table(query, params=(id,))['value'].iloc[0] if id != None else ''


def get_fruit_variety(id):
    query = "SELECT variety_name, agronomy_name FROM fruit_variety WHERE variety_id = %s"
    return MySQLRead.get_table(query, params=(int(id),))['variety_name'].iloc[0] if id != None else ''


def get_soil_type(id):
    query = "SELECT * FROM soil_type WHERE id = %s"
    return MySQLRead.get_table(query, params=(id,))['value'].iloc[0] if id != None and id != 0 else ''


def get_rootstock_type(id):
    query = "SELECT * FROM rootstock_type WHERE rootstock_id = %s"
    return MySQLRead.get_table(query, params=(id,))['value'].iloc[0] if id != None else ''


def get_dfs():
    query1 = ('SELECT * FROM countries')
    query2 = "SELECT * FROM fruit_variety"
    return MySQLRead.get_table(query1), MySQLRead.get_table(query2)


if __name__ == '__main__':
    import settings

    settings.init()

    # init_combobox = get_first_scan_blocks('"2022-08-02T00:00:00.000Z"')
    # temp = get_scans(2543,2023,"2022-08-02T00:00:00.000Z")
    # temp = get_init_block(4689)
    c = 1
