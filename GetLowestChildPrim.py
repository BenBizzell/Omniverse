def get_lowest_child_prims(prim):
    """
    Recursively find all lowest child prims in the hierarchy.
    A lowest child prim is defined as a prim with no children.
    """
    if not prim.GetChildren():
        return [prim]

    lowest_prims = []
    for child in prim.GetChildren():
        lowest_prims.extend(get_lowest_child_prims(child))

    return lowest_prims

def export_prims_to_csv(prims, file_path):
    """
    Export the names of the given prims to a CSV file.
    """
    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Prim Name'])
            for prim in prims:
                prim_name = prim.GetPath().name
                # Check if the prim name starts with "Mesh" or "Shader"
                if prim_name.startswith("Mesh"):
                    print(f"Exporting parent prim: {prim_name}")
                # Check if the prim name starts with "MABE"
                if prim_name.startswith("MABE"):
                    print(f"Exporting prim: {prim_name}")
                writer.writerow([prim_name])
        print(f"CSV file successfully written to {file_path}")
    except Exception as e:
        print(f"Failed to write CSV file: {e}")

def main():
    # Get the current stage
    stage = omni.usd.get_context().get_stage()
    if not stage:
        print("No stage loaded.")
        return

    # Get the /World prim
    world_prim = stage.GetPrimAtPath('/World')
    if not world_prim:
        print("No /World prim found.")
        return

    # Get all lowest child prims under /World
    lowest_child_prims = get_lowest_child_prims(world_prim)

    # Check if any prims were found
    if not lowest_child_prims:
        print("No lowest child prims found under /World.")
        return

    # Specify the CSV file path
    csv_file_path = os.path.abspath("EXPORT.csv")

    # Export the names of the lowest child prims to a CSV file
    export_prims_to_csv(lowest_child_prims, csv_file_path)


main()
