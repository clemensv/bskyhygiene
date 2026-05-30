p = chr(124)  # pipe char
script_lines = []
script_lines.append("import json, sys")
script_lines.append("from azure.kusto.data import KustoClient, KustoConnectionStringBuilder")
script_lines.append("from azure.identity import DefaultAzureCredential")
script_lines.append("")
print("generator stub ok")
