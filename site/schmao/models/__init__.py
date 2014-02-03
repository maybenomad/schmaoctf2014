import os

def _import_models():
  """
  Dynamically import all Flask-SQLAlchemy models from this 
  directory. Each file should contain exactly one model and
  should use the following naming convention: 
    'my_leet_model.py', 'class MyLeetModel()'
  """
  exports = []
  package_path = os.path.dirname(__file__)
  glob_vars, loc_vars = globals(), locals()

  for module_file in os.listdir(package_path):
    module_name, ext = module_file.split('.')

    if module_name[0] != '_' and ext == 'py':
      subpackage = '%s.models' % 'schmao'
      module = __import__(subpackage,
                          glob_vars, loc_vars,
                          [module_name])
      submodule = module.__dict__.get(module_name)
      model = submodule.__dict__.get(module_name.capitalize())
      model_name = module_name.capitalize()
      glob_vars.update({model_name: model})
      exports.append(model_name)

  return exports

if __name__ != '__main__':
    __all__ = _import_models()
