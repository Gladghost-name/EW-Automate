import json
import typing
import os
import posixpath
import zipfile
import tempfile
import unzip
import shutil

class EWSXFIle():
    def __init__(self):
        self.existing_file = None

    def save(self, filename: os.PathLike = None):
        with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as z:
            with tempfile.TemporaryDirectory() as temp_dir:
                # creating the media directory.
                if not self.existing_file:
                    os.mkdir(os.path.join(temp_dir, "media"))

                    # creating the database file
                    with open(os.path.join(temp_dir, "main.db"), "wb+") as f:
                        f.write(open("./sample_files/main.db", "rb+").read())
                else:
                    for dir in self.dirs_list:
                        os.makedirs(os.path.join(temp_dir, dir), exist_ok=True)
                    for file in self.files_list:
                        open(os.path.join(temp_dir, file[0]), "wb+").write(file[1])

                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, temp_dir)
                        z.write(full_path, rel_path)
        print(f"Successfully saved schedule in `{posixpath.abspath(filename)}` ✅")

    def from_file(self, filename):
        """expand from an already existing schedule file."""
        self.files_list = []
        self.dirs_list = []
        self.existing_file = filename
        with tempfile.TemporaryDirectory() as output_dir:
            unzip.ExpandEWSXFile(filename, output_dir)
            for root, dirs, files in os.walk(output_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, output_dir)
                    self.files_list.append((rel_path, open(full_path, "rb+").read()))
                
                for dir in dirs:
                    self.dirs_list.append(dir)
        return self
    
    def expand_to_dir(self, output_dir: str = "schedules"):
        os.makedirs(output_dir, exist_ok=True)
        with tempfile.TemporaryDirectory() as temp_dir:
            # creating the media directory.
            if not self.existing_file:
                os.mkdir(os.path.join(temp_dir, "media"))

                # creating the database file
                with open(os.path.join(temp_dir, "main.db"), "wb+") as f:
                    f.write(open("./sample_files/main.db", "rb+").read())
            else:
                for dir in self.dirs_list:
                    os.makedirs(os.path.join(temp_dir, dir), exist_ok=True)
                for file in self.files_list:
                    open(os.path.join(temp_dir, file[0]), "wb+").write(file[1])

            num = len(os.listdir(output_dir)) + 1
            schedule_path = os.path.join(output_dir, "schedule" + str(num))
            os.makedirs(schedule_path, exist_ok=True)
            for file in os.listdir(temp_dir):
                if unzip.is_directory(file):
                    dir_path = os.path.join(schedule_path, file)
                    os.mkdir(dir_path)
                    shutil.copytree(os.path.join(temp_dir, file), dir_path, dirs_exist_ok=True)
                else:
                    shutil.copy(os.path.join(temp_dir, file), schedule_path)
        print(f"schedule expanded into `{posixpath.abspath(os.path.join(output_dir, schedule_path))}` ✅")

    def structure(self) -> str:
        """Returns the structure of the schedule file after decompressing."""
        files_set = []
        dirs_set = []

        if self.existing_file:
            files_set = [x[0] for x in self.files_list]
            dirs_set = self.dirs_list
        else:
            dirs_set = ["media"]
            files_set = ["main.db"]

        
        explored = []
        struct = ""
        for f in dirs_set + files_set:
            if unzip.is_directory(f):
                struct += f + "/" + "\n"
                files = []
                for x in files_set:
                    if x.startswith(f):
                        files.append(x.strip("/" + f))
                        explored.append(x)
                if files:
                    struct += "    " + "\n    ".join(files) + "\n"
            else:
                if f not in explored:
                    struct += f
            explored.append(f)
        return struct


def Create():
    """Create a new Easy Worship 7 schedule file object."""
    return EWSXFIle()



schedule = Create().from_file("./NewSchedule.ewsx")
print(schedule.structure())

# schedule.save("data.ewsx")