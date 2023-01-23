# %%
import sys
sys.path.insert(0, r"E:/github/wvangerwen/hhnk-threedi-tools")
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import os

import hhnk_research_tools as hrt
import hhnk_threedi_tools.core.api.upload_model.upload as upload

INFILTRATION_COLS = [
    "infiltration_rate",
    "infiltration_rate_file",
    "infiltration_surface_option",
    "max_infiltration_capacity_file",
    "display_name",
]

RASTER_FILES = [
    "dem_file",
    "frict_coef_file",
    "infiltration_rate_file",
    "max_infiltration_capacity_file",
]

class ModelSchematisations:
    def __init__(self, folder, modelsettings_path):
        self.folder = folder
        self.settings_loaded = False


        if os.path.exists(modelsettings_path):
            self.settings_df = pd.read_excel(modelsettings_path, engine="openpyxl")
            self.settings_df = self.settings_df[self.settings_df['name'].notna()]
            self.settings_df.set_index("name", drop=False, inplace=True)
            self.settings_loaded = True
        else:
            self.settings_df = None

        if self.folder.model.settings_default.exists:
            self.settings_default_series = pd.read_excel(
                self.folder.model.settings_default.path, engine="openpyxl"
            ).iloc[
                0
            ]  # Series, only has one row.
        else:
            self.settings_default_series = None
            self.settings_loaded = False

            
        self.folder.model.set_modelsplitter_paths()


        if self.settings_loaded:
            self._sanity_check()

    def _sanity_check(self):
        """Sanity check settings tables"""
        inter = self.settings_df.keys().intersection(
            self.settings_default_series.keys()
        )
        if len(inter) > 0:
            print(
                f"""Er staan kolommen zowel in de defaut als in de andere modelsettings.
        Dat lijkt me een slecht plan. Kolommen: {inter.values}"""
            )

    def get_revision_info(self, name, api_key):
        upload.threedi.set_api_key(api_key)
        name=name        
        row = self.settings_df.loc[name]
        schema_folder = os.path.join(str(self.folder.model))
        if not os.path.exists(schema_folder + "\\revisions"):
            os.makedirs(schema_folder + "\\revisions")
            count = len(os.listdir(str(self.folder.model)+"\\revisions"))
            return str("Latest local revision:      rev" + str(count))

        schematisation = row["schematisation_name"]
        threedimodel = upload.threedi.api.threedimodels_list(revision__schematisation__name=schematisation)

        if threedimodel.results == []:
            return str("No previous model(s) available for: " + schematisation)
    
        if threedimodel.results != []:
            schema_id = threedimodel.to_dict()['results'][0]['schematisation_id']
            latest_revision = upload.threedi.api.schematisations_latest_revision(schema_id)
            rev_model = threedimodel.to_dict()['results'][0]['name']
            return str("Latest model revision:      " + rev_model + " - " + latest_revision.commit_message)


    def create_schematisation(self, name):
        """Create a schematisation based on the modelsettings.
        Some schematisations (0d1d_test) have some extra changed that are not
        only the globalsettings"""
        row = self.settings_df.loc[name].copy()

        schema_name = self.folder.model._add_modelpath(name)

        # Copy the files that are in the global settings.
        # This menas rasters that are not defined are not added to the schematisation.
        schema_base = self.folder.model.schema_base
        schema_new = getattr(self.folder.model, f"schema_{name}")

        # Write the sqlite and rasters to new folders.

        # Copy sqlite
        src = schema_base.database.path
        dst = os.path.join(schema_new.path, schema_base.database.pl.name)
        shutil.copyfile(src=src, dst=dst)

        schema_new.rasters.create(parents=False)
        # Copy rasters that are defined in the settings file
        for raster_file in RASTER_FILES:
            if not pd.isnull(row[raster_file]):
                src = os.path.join(schema_base.path, row[raster_file])
                if os.path.exists(src):
                    dst = os.path.join(schema_new.path, row[raster_file])
                    shutil.copyfile(src=src, dst=dst)
                else:
                    # TODO raise error?
                    print(f"Couldnt find raster:\t{row[raster_file]}")

        database_path_base = schema_base.database.path
        database_path_new = schema_new.database.path

        # Edit the SQLITE
        table_names = ["v2_global_settings", "v2_simple_infiltration"]
        for table_name in table_names:
            print(f"\tUpdate {table_name}")
            # Set the id in the v2_simple_iniltration to the id defined in global settings.
            if table_name == "v2_simple_infiltration":
                row["id"] = row["simple_infiltration_settings_id"]
            else:
                row["id"] = 1

            # Clear the table
            hrt.execute_sql_changes(
                query=f"""DELETE FROM {table_name}""", database=database_path_new
            )

            # Create new value and column pairs. The new values are used from the settings.xlsx file.
            # Dont create v2_simple infiltration if the id is not defined
            if not pd.isnull(row["id"]):
                df_table = hrt.sqlite_table_to_df(
                    database_path=database_path_new, table_name=table_name
                )
                columns = []
                values = []
                for key in df_table.keys():
                    columns.append(key)
                    if key in row:
                        value = row[key]
                    elif key in self.settings_default_series:
                        value = self.settings_default_series[key]
                    else:
                        value = None
                        print(f"Column {key} not defined")
                    if pd.isnull(value):
                        value = None

                    # Exceptions
                    # startdate is interpreted as timestamp by pandas but we only need YYYY-MM-DD format.
                    if key == "start_date":
                        try:
                            value = str(value)[:10]
                        except:
                            pass
                    values.append(value)

                # Make sure None is interpreted as NULL by sqlite.
                columns = tuple(columns)
                values = str(tuple(values)).replace("None", "NULL")

                # Prepare insert query
                query = f"""INSERT INTO {table_name} {columns}
                VALUES {values}"""

                # Insert new row
                hrt.execute_sql_changes(query, database=database_path_new)

        # Additional model changes for different model types
        if row["name"] == "0d1d_test":
            # Set every channel to isolated
            hrt.execute_sql_changes(
                query="UPDATE v2_channel SET calculation_type=101",
                database=database_path_new,
            )

            # Set controlled weirs to 10x width because we dont use controlled strcutures in hyd test.
            # To get the weir with we use the base database, so we cant accidentally run this twice.
            controlled_weirs_selection_query = f"""
                SELECT
                v2_weir.cross_section_definition_id as cross_def_id,
                v2_weir.code as weir_code,
                v2_weir.id as id,
                v2_cross_section_definition.width as width
                FROM v2_weir
                INNER JOIN v2_cross_section_definition ON v2_weir.cross_section_definition_id = v2_cross_section_definition.id
                INNER JOIN v2_control_table ON v2_weir.id = v2_control_table.target_id
                """
            controlled_weirs_df = hrt.execute_sql_selection(
                controlled_weirs_selection_query, database_path=database_path_base
            )

            controlled_weirs_df.insert(
                controlled_weirs_df.columns.get_loc("width") + 1,
                "width_new",
                controlled_weirs_df["width"].apply(lambda x: round((float(x) * 10), 3)),
            )

            query = hrt.sql_create_update_case_statement(
                df=controlled_weirs_df,
                layer="v2_cross_section_definition",
                df_id_col="cross_def_id",
                db_id_col="id",
                old_val_col="width",
                new_val_col="width_new",
            )

            hrt.execute_sql_changes(query=query, database=database_path_new)

    def upload_schematisation(self, name, commit_message, api_key):             
        """
        possible raster_names
        [ dem_file, equilibrium_infiltration_rate_file, frict_coef_file,
        initial_groundwater_level_file, initial_waterlevel_file, groundwater_hydro_connectivity_file,
        groundwater_impervious_layer_level_file, infiltration_decay_period_file, initial_infiltration_rate_file,
        leakage_file, phreatic_storage_capacity_file, hydraulic_conductivity_file, porosity_file, infiltration_rate_file,
        max_infiltration_capacity_file, interception_file ]
        """
        revision_parent_folder = self.folder.model.revisions.path

        count = len(os.listdir(revision_parent_folder))
        revision_folder = os.path.join(revision_parent_folder, f"rev_{count+1}")
        if not os.path.exists(revision_folder):
            os.makedirs(revision_folder)

        row = self.settings_df.loc[name]
        schema_new = getattr(self.folder.model, f"schema_{name}")
        schema_str = str(schema_new)
        target_file = str(self.folder.model) + "\\revisions\\rev" + str(count+1) + "_" + str(commit_message)
        shutil.copytree(schema_str, target_file)

        upload.threedi.set_api_key(api_key)

        raster_names = {
            "dem_file": schema_new.rasters.dem.path_if_exists,
            "frict_coef_file": schema_new.rasters.friction.path_if_exists,
            "infiltration_rate_file": schema_new.rasters.infiltration.path_if_exists,
            "max_infiltration_capacity_file": schema_new.rasters.storage.path_if_exists,
        }

        sqlite_path = schema_new.database.path
        schematisation_name = row["schematisation_name"]
        tags = [schematisation_name, self.folder.name]
        # organisation_uuid="48dac75bef8a42ebbb52e8f89bbdb9f2"

        upload.upload_and_process(
            schematisation_name=schematisation_name,
            sqlite_path=sqlite_path,
            raster_paths=raster_names,
            schematisation_create_tags=tags,
            commit_message=commit_message,
        )

#%%

# def get_revision_info(revision__schematisation__name):
#     threedimodel = upload.threedi.api.threedimodels_list(revision__schematisation__name)
#     if threedimodel.results == []:
#         return "no previous model(s) available"
    
#     else:
#         schema_id = threedimodel.to_dict()['results'][0]['schematisation_id']
#         latest_revision = upload.threedi.api.schematisations_latest_revision(schema_id)
#         rev_model = threedimodel.to_dict()['results'][0]['name']
#         return "previous model revision: " + rev_model + " " + latest_revision.commit_message 

        
# %%

if __name__ == "__main__":
    from hhnk_threedi_tools.core.folders import Folders

    # path = r"E:\02.modellen\model_test_v2"
    path = r"\\corp.hhnk.nl\data\Hydrologen_data\Data\02.modellen\heiloo_geen_gemaal"
    folder = Folders(path)
    name = "1d2d_glg"

    self = ModelSchematisations(
        folder=folder, modelsettings_path=folder.model.settings.path
    )
    self.create_schematisation(name=name)
    self.upload_schematisation(
        name=name,
        commit_message="Load Model. Pump capacity 466 l/sec",
        api_key="aDFMXSfR.XdXc1MaWXYtA3DIXxrgzXzH1u4Lnfe7N",
    )
    # %%
    upload.threedi.set_api_key("")
    #upload.threedi.api.threedimodels_list?

# %%

# # Check beschikbare modellen
# threedimodels = upload.threedi.api.threedimodels_list(revision__schematisation__name=schematisation.name)
# models = threedimodels.to_dict()['results']#[0]['id']
# if len(models)> 2:
#     cont = input("Remove oldest threedi model? [y/n]")
#     if cont=='y':
#         upload.threedi.api.threedimodels_delete(id=models[-1]['id'])


# upload.threedi.api.schematisations_revisions_create_threedimodel(id=41937, 
#                 schematisation_pk=5746)

# # %%



#     # Schematisatie maken als die nog niet bestaat
# schematisation = upload.get_or_create_schematisation(
#         schematisation_name="model_test_v2__0d1d_test", tags=["model_test_v2__0d1d_test", "model_test_v2"]
#     )
    


#     # Nieuwe (lege) revisie aanmaken
# revision = upload.threedi.api.schematisations_revisions_list( 
#         schematisation.id)



# # %%

# upload.create_threedimodel(schematisation, revision)

# # %%

# schematisation.id

# threedimodels = upload.threedi.api.threedimodels_list(revision__schematisation__name=schematisation.name)
# threedischema = upload.threedi.api.schematisations_list()
# schema = threedischema.to_dict()['results']
# i = schema.count()
# x = 0
# schema_list = []
# #models = threedimodels.to_dict()['results']#[0]['id']
# while x < 800:
#     a = threedischema.to_dict()['results'][x]['id']
#     schema_list.append(a)
#     x = x + 1 
    

# if len(models)> 2:
#     cont = input("Remove oldest threedi model? [y/n]")
#     if cont=='y':
#         upload.threedi.api.threedimodels_delete(id=models[-1]['id'])
    

# # %%

# %%
def create_threedimodel(
    schematisation,
    revision,
    max_retries_creation=60,
    wait_time_creation=5,
    max_retries_processing=60,
    wait_time_processing=60,
):
    threedimodel = None
    for i in range(max_retries_creation):
        try:
            threedimodel = threedi.api.schematisations_revisions_create_threedimodel(
                revision.id, schematisation.id
            )
            print(f"Creating threedimodel with id {threedimodel.id}...")
            break
        except ApiException:
            time.sleep(wait_time_creation)
            continue
    if threedimodel:
        for i in range(max_retries_processing):
            threedimodel = threedi.api.threedimodels_read(threedimodel.id)
            if threedimodel.is_valid:
                print(f"Succesfully created threedimodel with id {threedimodel.id}")
                break
            else:
                time.sleep(wait_time_processing)
        if not threedimodel.is_valid:
            print(
                f"Failed to sucessfully process threedimodel with id {threedimodel.id}"
            )
    else:
        print("Failed to create threedimodel")
    return threedimodel.id