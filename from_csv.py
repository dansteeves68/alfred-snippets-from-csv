#!/usr/bin/env python3
"""Create *.alfredsnippets bundles from CSV files
Thanks to https://github.com/zoenglinghou/alfred-emoji/blob/master/main.py"""

import csv
import json
import os
import shutil
import tempfile
import uuid
from glob import glob


class snippets_from_csv(object):
    def __init__(self, csv_file, src_dir, src_files):
        self.csvfile = csv_file
        self.src_dir = os.path.abspath(src_dir)
        self.bname = self.csvfile.split(".")[0]
        self.src_files = src_files
        self.products_path = tempfile.mkdtemp()

    def write_snippets(self):
        with open(os.path.join(self.src_dir, csv_file), "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                uid = str(uuid.uuid4()).upper()
                row["uid"] = uid
                row["dontautoexpand"] = False
                snippet = {"alfredsnippet": row}
                filename = os.path.join(
                    self.products_path, row.get("name") + " [" + uid + "].json"
                )
                with open(filename, "w") as fp:
                    json.dump(snippet, fp)

    def add_plist(self):
        plist = self.bname + ".plist"
        if plist in src_files:
            shutil.copyfile(
                os.path.join(self.src_dir, plist),
                os.path.join(self.products_path, "info.plist"),
            )

    def prepare_file(self):
        bname = "./" + self.bname
        shutil.make_archive(bname, "zip", self.products_path)
        os.rename(bname + ".zip", bname + ".alfredsnippets")

    def main(self):
        self.write_snippets()
        self.add_plist()
        self.prepare_file()
        shutil.rmtree(self.products_path)


if __name__ == "__main__":
    src_dir = os.path.abspath("./src")
    src_files = os.listdir(src_dir)
    csv_files = [a for a in src_files if ".csv" in a]
    for csv_file in csv_files:
        from_csv = snippets_from_csv(csv_file, src_dir, src_files)
        from_csv.main()
