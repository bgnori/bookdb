

import Rx


rx = Rx.Factory({ "register_core_types": True });


#rx.learn_type(schema_test_spec['composedtype']['uri'],
#rx.add_prefix(schema_test_spec['composedtype']['prefix'][0],
#schema = rx.make_schema(schema_test_spec["schema"])
#result = schema.check( test_data[source][entry] )



"""
  if filename == 'spec/index.json': continue
  payload = json.loads(file(filename).read())

  #filename == "spec/schemata/???.json"
  #filename == "spec/data/???.json"
  parts = filename.split('/')
  parts.pop(0)

  leaf_name = '/'.join(parts[1:])
  #leaf_name == schemata/???.json
  #leaf_name == data/???.json
  leaf_name = re.sub('\.json$', '', leaf_name)
  #leaf_name == schemata/???
  #leaf_name == data/???

  filetype = parts.pop(0)
  #== schema or data

  if filetype == 'schemata':
    test_schemata[ leaf_name ] = payload
  elif filetype == 'data':
    test_data[ leaf_name ] = {}
"""


with file('rx-schema.yaml') as f:

  schema = rx.make_schema('meta')
  schema.check(f.read())



