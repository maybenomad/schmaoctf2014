import os

def _import_controllers():
  """
  Dynamically import all modules containing controllers. 
  Unlike models, these are not injected into the global
  environment upon import. 
  """
  exports = []
  package_path = os.path.dirname(__file__)

  for module_file in os.listdir(package_path):
    if module_file[0] != '_' and module_file[-3:] == '.py':
      exports.append(module_file[:-3])

  return exports

if __name__ != '__main__':
    __all__ = _import_controllers()
