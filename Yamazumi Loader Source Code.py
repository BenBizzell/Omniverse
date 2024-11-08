import omni
import omni.ext
import omni.ui as ui
import omni.kit.commands
from pxr import Gf, Usd, UsdGeom, UsdShade, Sdf
import pandas as pd
import os

##Yamazumi Loader Demo

# Function to set vibility to invisible
def toggle_visibility_invisible(prim):
    visibility_attr = prim.GetAttribute('visibility')
    if not visibility_attr:
        visibility_attr = UsdGeom.Imageable(prim).CreateVisibilityAttr()
    visibility_attr.Set(UsdGeom.Tokens.invisible)

# Function to set visibility to inherited
def toggle_visibility_inherited(prim):
    visibility_attr = prim.GetAttribute('visibility')
    if not visibility_attr:
        visibility_attr = UsdGeom.Imageable(prim).CreateVisibilityAttr()
    visibility_attr.Set(UsdGeom.Tokens.inherited)

# Function to ensure parent prims and World are set to inherited
def parent_inherited(prim):
    while prim.GetPath() != "/World":
        prim = prim.GetParent()
        if prim:
            toggle_visibility_inherited(prim)
        else:
            break
    world_prim = stage.GetPrimAtPath("/World")
    if world_prim:
        toggle_visibility_inherited(world_prim)



# Get current stage
stage = omni.usd.get_context().get_stage()

# Read CSV
spawn_units_file_path = "REDACTED.csv"
process_sheet_file_path = "REDACTED.csv"
df_spawn_units = pd.read_csv(spawn_units_file_path)
df_process_sheet = pd.read_csv(process_sheet_file_path)

# Set path to reference USD file
usd_file_path = "REDACTED.usd"

# Iterate through each row in SpawnUnits
for index, row in df_spawn_units.iterrows():
    # Set prim path for the USD in Omniverse
    usd_path = f"/World/Geometry/DRYER_MODEL_{index}"
    # Define the prim type in Omniverse
    usd_prim = stage.DefinePrim(usd_path, "Xform")
    # Add the reference in Omniverse
    usd_prim.GetReferences().AddReference(usd_file_path)

    # TranslateXYZ
    xform = UsdGeom.Xformable(usd_prim)
    xform.AddTranslateOp().Set(Gf.Vec3f(row.iloc[2], row.iloc[3], row.iloc[4]))

    # RotateXYZ
    xform.AddRotateXYZOp().Set(Gf.Vec3f(row.iloc[5], row.iloc[6], row.iloc[7]))

    # ScaleXYZ
    xform.AddScaleOp().Set(Gf.Vec3f(row.iloc[8], row.iloc[9], row.iloc[10]))

    # Keep history of previous station parts
    station_parts_history = []

    # Set all prims in each model to invisible
    print (len(df_spawn_units.iloc[:, 0]))
    for i in range(len(df_spawn_units.iloc[:, 0])):
        reference_path = f"/World/Geometry/DRYER_MODEL_{i}"
        traverse_start = stage.GetPrimAtPath(reference_path)
        for prim in Usd.PrimRange(traverse_start):
            toggle_visibility_invisible(prim)

        # Create array for parts in each ProcessSheet column
        station_parts = set(df_process_sheet.iloc[:, i].str.strip())

        for prim in Usd.PrimRange(traverse_start):
            prim_name = prim.GetName()
            # Set prims from previous station to inherited       
            if prim_name in station_parts_history:
                toggle_visibility_inherited(prim)
                parent_inherited(prim)
            # Set prims and their parents in current station to inherited
            if prim_name in station_parts:
                station_parts_history.append(prim_name)
                toggle_visibility_inherited(prim)
                parent_inherited(prim)
