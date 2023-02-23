# Libraries:
import zipfile
import os


# unzips file root+zip_file to root+"temp"
def unzip(zip_file, extract_location):
  with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(extract_location)


# Return: Boolean exists, String root, String name, String extension
def file_meta(full_path):
  full_path_normalized = os.path.normcase(full_path.replace('\"', ''))
  exists = os.path.isfile(full_path_normalized)
  if not exists:
    return exists, None, None, None
  root_name, extension = os.path.splitext(full_path_normalized)
  root = root_name[:root_name.rfind("\\") + 1]
  name = root_name[root_name.rfind("\\") + 1:]

  return exists, root, name, extension
