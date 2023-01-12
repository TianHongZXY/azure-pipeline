# upload-data.py
from azureml.core import Workspace, Datastore
from azureml.core import Dataset
from azureml.data.datapath import DataPath

ws = Workspace(
    subscription_id="521f9448-5428-4a47-b228-f34801eaaa26",
    resource_group="aicode",
    workspace_name="aicode"
)
# ws = Workspace.from_config()
# datastore = ws.get_default_datastore()
datastore = Datastore(ws, "workspaceblobstore")
Dataset.File.upload_directory(src_dir='/home/zhuxinyu/codes/ReAct/data', 
                              target=DataPath(datastore, "hotpotqa1")
                             )