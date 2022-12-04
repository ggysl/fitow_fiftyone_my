import json
from shutil import copy

copy("/root/workspace/fitow_fiftyone/modified_source/stages.py", "/opt/conda/envs/fo/lib/python3.8/site-packages/fiftyone/core/stages.py")
copy("/root/workspace/fitow_fiftyone/modified_source/collections.py", "/opt/conda/envs/fo/lib/python3.8/site-packages/fiftyone/core/collections.py")
copy("/root/workspace/fitow_fiftyone/modified_source/utils.py", "/opt/conda/envs/fo/lib/python3.8/site-packages/fiftyone/core/utils.py")

with open("/root/.jupyter/nbconfig/notebook.json", "r", encoding="utf-8") as fp:
    notebook_dict = json.load(fp)
    notebook_dict["load_extensions"]["hinterland/hinterland"] = True
with open("/root/.jupyter/nbconfig/notebook.json", "w", encoding="utf-8") as fp:
    json.dump(notebook_dict, fp, indent=4)