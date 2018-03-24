
import os
import json
#from jinja2 import Environment, PackageLoader, Template
from jinja2 import Environment, FileSystemLoader

#template = env.get_template('example.json')

def generate_maintenance_json():
  THIS_DIR = os.path.dirname(os.path.abspath(__file__))

  j2_env = Environment(loader=FileSystemLoader(THIS_DIR),
                         trim_blocks=True)

  payload = j2_env.get_template('example.json').render(
        index_number='5'
    )

  return payload


#print template.render(index_number='5')
