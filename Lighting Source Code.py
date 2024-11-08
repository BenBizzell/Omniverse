import omni
import omni.ext
import omni.ui as ui
import omni.kit.commands
import omni.kit.pipapi
from pxr import Gf, Usd, UsdGeom, Sdf
omni.kit.pipapi.install("pandas")
import pandas as pd
import os

# Functions and vars are available to other extension as usual in python: `example.python_ext.some_public_function(x)`
def some_public_function(x: int):
    print("[convert.to.omni] some_public_function was called with x: ", x)
    return x ** x

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class ConvertToOmniExtension(omni.ext.IExt):
    # ext_id is current extension id. It can be used with extension manager to query additional information, like where
    # this extension is located on filesystem.
    def on_startup(self, ext_id):
        print("[convert.to.omni] convert to omni startup")

        self._window = ui.Window("CSV to Omni", width=150, height=150)
        with self._window.frame:
            with ui.VStack():
                #label = ui.Label("")

                def on_click():
                    file_path = 'Z:\\George Tait\\Ben Omniverse\\import_lights.csv'
                    df = pd.read_csv(file_path)
                    for index, row in df.iterrows():
                        RectLight_index = f'RectLight_{index}'
                        if row.iloc[0]=='RectLight':
                            #Create Prim
                            omni.kit.commands.execute('CreatePrimWithDefaultXform',
                                prim_type='RectLight',
                                attributes={'inputs:width': 100.0, 'inputs:height': 100.0, 'inputs:intensity': 150000.0},
                                prim_path=f'/World/{RectLight_index}',
                                select_new_prim=True)
                            #Translate
                            omni.kit.commands.execute('ChangeProperty',
                                prop_path=f'/World/{RectLight_index}.xformOp:translate',
                                value=Gf.Vec3f(float(row.iloc[1]), float(row.iloc[2]), float(row.iloc[3])),
                                prev=None)
                            #Rotate
                            omni.kit.commands.execute('ChangeProperty',
                                prop_path=f'/World/{RectLight_index}.xformOp:rotateXYZ',
                                value=Gf.Vec3d(0.0, 0, 180.0),
                                prev=None)



                    # stage = omni.usd.get_context().get_stage()

                    # df = pd.read_csv(file_path)

                    # for index, row in df.iterrows():
                        
                    #     #Reference USD
                    #     usd_file = row.iloc[0]
                    #     usd_path = os.path.join("C:\\Users\\240126022\\Desktop", f"{usd_file}.usd")
                    #     prim_path = f"/World/{usd_file}_{index}"
                    #     prim = stage.DefinePrim(prim_path, "Xform")
                    #     prim.GetReferences().AddReference(usd_path)

                    #     # Get the bounding box of the asset
                    #     bbox_cache = UsdGeom.BBoxCache(Usd.TimeCode.Default(), [UsdGeom.Tokens.default_])
                    #     bbox = bbox_cache.ComputeWorldBound(prim)
                    #     min_point = bbox.GetRange().GetMin()

                    #     # Calculate the pivot offset to move the origin to the bottom corner
                    #     pivot_offset = Gf.Vec3d(min_point[0], min_point[1], min_point[2])

                    #     # Apply the pivot offset to the root prim
                    #     xform = UsdGeom.Xformable(prim)
                    #     xform.AddXformOp(UsdGeom.XformOp.TypeTranslate, UsdGeom.XformOp.PrecisionDouble).Set(pivot_offset)

                    #     #Translate XYZ
                    #     xform = UsdGeom.Xformable(prim)
                    #     xform.AddTranslateOp().Set(Gf.Vec3f(row.iloc[1], row.iloc[2], row.iloc[3]))

                    #     #Rotate XYZ
                    #     xform.AddRotateXYZOp().Set(Gf.Vec3f(row.iloc[4], row.iloc[5], row.iloc[6]))

                    #     #Scale XYZ
                    #     xform.AddScaleOp().Set(Gf.Vec3f(row.iloc[7], row.iloc[8], row.iloc[9]))



                    #Add RectLight
                    # Total Resulting Lights Generated is grid_width * grid_height
                    # Y-axis up in Omniverse
                    # grid_width = 60     # Number of Lights along X-axis
                    # grid_length = 30    # Number of Lights along Z-axis
                    # spacing = 100

                    # # Iterate X-axis
                    # for i in range(grid_width):
                    #     # Iterate Z-axis
                    #     for j in range(grid_length):
                    #         omni.kit.commands.execute('CreatePrimWithDefaultXform',
                    #             prim_type='RectLight',
                    #             attributes={'inputs:width': 100.0, 'inputs:height': 100.0, 'inputs:intensity': 15000.0},
                    #             prim_path=f'/World/RectLight',
                    #             select_new_prim=True)

                    #         translation = Gf.Vec3f(i * spacing, 0, j * spacing) 
                                        
                    #         #Translate XYZ
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/RectLight.xformOp:translate',
                    #             value=translation,
                    #             prev=None)

                    #         #Rotate XYZ
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/RectLight.xformOp:rotateXYZ',
                    #             value=Gf.Vec3d(270, 0, 0),
                    #             prev=None)



                    # df = pd.read_csv(file_path)
                    # for index, row in df.iterrows():
                    #     RectLight_index = f'RectLight_{index}'
                    #     if row.iloc[0]=='RectLight':
                    #         #Create Prim
                    #         omni.kit.commands.execute('CreatePrimWithDefaultXform',
                    #             prim_type='RectLight',
                    #             attributes={'inputs:width': 100.0, 'inputs:height': 100.0, 'inputs:intensity': 15000.0},
                    #             prim_path=f'/World/{RectLight_index}',
                    #             select_new_prim=True)
                    #         #Translate
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/{RectLight_index}.xformOp:translate',
                    #             value=Gf.Vec3f(float(row.iloc[1]), float(row.iloc[2]), float(row.iloc[3])),
                    #             prev=None)
                    #         #Height
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/{RectLight_index}.inputs:height',
                    #             value=float(row.iloc[4]),
                    #             prev=100.0)
                    #         #Width
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/{RectLight_index}.inputs:width',
                    #             value=float(row.iloc[5]),
                    #             prev=100.0)
                    #         #Rotate
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/{RectLight_index}.xformOp:rotateXYZ',
                    #             value=Gf.Vec3d(float(row.iloc[6]), float(row.iloc[7]), float(row.iloc[8])),
                    #             prev=None)
                    #         #Scale
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/{RectLight_index}.xformOp:scale',
                    #             value=Gf.Vec3d(float(row.iloc[9]), float(row.iloc[10]), float(row.iloc[11])),
                    #             prev=(1, 1, 1))
                    #         #Intensity
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/{RectLight_index}.inputs:intensity',
                    #             value=float(row.iloc[12]),
                    #             prev=15000.0)
                    #         #Exposure
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/{RectLight_index}.inputs:exposure',
                    #             value=float(row.iloc[13]),
                    #             prev=None)




                    #Add RectLight
                    # Total Resulting Lights Generated is grid_width * grid_height
                    # Y-axis up in Omniverse
                    # grid_width = 60     # Number of Lights along X-axis
                    # grid_length = 30    # Number of Lights along Z-axis
                    # spacing = 100

                    # # Iterate X-axis
                    # for i in range(grid_width):
                    #     # Iterate Z-axis
                    #     for j in range(grid_length):
                    #         omni.kit.commands.execute('CreatePrimWithDefaultXform',
                    #             prim_type='RectLight',
                    #             attributes={'inputs:width': 100.0, 'inputs:height': 100.0, 'inputs:intensity': 15000.0},
                    #             prim_path=f'/World/RectLight',
                    #             select_new_prim=True)

                    #         translation = Gf.Vec3f(i * spacing, 0, j * spacing) 
                                        
                    #         #Translate XYZ
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/RectLight.xformOp:translate',
                    #             value=translation,
                    #             prev=None)

                    #         #Rotate XYZ
                    #         omni.kit.commands.execute('ChangeProperty',
                    #             prop_path=f'/World/RectLight.xformOp:rotateXYZ',
                    #             value=Gf.Vec3d(270, 0, 0),
                    #             prev=None)

                with ui.HStack():
                    ui.Button("Spawn Items", clicked_fn=on_click)

    def on_shutdown(self):
        print("[convert.to.omni] convert to omni shutdown")