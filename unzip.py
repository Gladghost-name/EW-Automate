import zipfile
import os
from pathlib import Path
import platform

def _update_crc(self, data):
    pass


def is_directory(name):
    if name.endswith("/") or name.endswith("\\"):
        return True
    
    if "." not in os.path.basename(name):
        return True
    return False



def ExpandEWSXFile(filepath, output_dir):
    zipfile.ZipExtFile._update_crc = _update_crc # avoid stric crc validation.
    with zipfile.ZipFile(filepath, "r") as z:
        for file in z.namelist():
            out_path = os.path.join(output_dir, f"{file}")
            
            if is_directory(file):
                os.makedirs(out_path, exist_ok=True)
                continue

            os.makedirs(os.path.dirname(out_path), exist_ok=True)
            
            try:
                # solve platform migration issue with paths.
                out_file = os.path.normpath(file).replace("\\", "/") if platform.system() == "Darwin" else file 
                out_path = os.path.join(output_dir, f"{out_file}")
                with z.open(file) as source, open(out_path, "wb+") as target:
                    target.write(source.read())
            except Exception as e:
                print(f"Error extracting {file}: {e}")


def createEWSXFile(unzipped_dir_path, output_file):
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(unzipped_dir_path):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, unzipped_dir_path)
                z.write(full_path, rel_path)       
    print("Created: ", output_file)
        
        
# createEWSXFile("out", "NewSchedule.ewsx")
# ExpandEWSXFile("SampleSchedule.ewsx", "out")
# createEWSXFile("out", "MACOSCompiledEWSchedule.ewsx")