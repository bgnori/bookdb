
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

#  if filetype == 'schemata':
#    test_schemata[ leaf_name ] = payload

# schema_names = test_schemata.keys()
# for schema_name in schema_names:
# schema_test_spec = test_schemata[ schema_name ]

#rx.learn_type(schema_test_spec['composedtype']['uri'],
#rx.add_prefix(schema_test_spec['composedtype']['prefix'][0],
#schema = rx.make_schema(schema_test_spec["schema"])

# schema = rx.make_schema(yaml.load(open("schema.yaml")))
# from
# http://stackoverflow.com/questions/6311738/create-a-model-from-yaml-json-on-the-fly

#result = schema.check( test_data[source][entry] )
import Rx
import yaml

rx = Rx.Factory({ "register_core_types": True });

for t in rx.type_registry:
  print t

meta = """{
    "type": "//any",
    "of": [
      {
        "type"    : "//rec",
        "required": { "type": "//str" },
        "rest"    : "//any"
        },
      "//str",
      ]
    }"""

with file('rx-schema.yaml') as f:
  schema = rx.make_schema(yaml.load(meta))
  print schema.check(meta)#f.read())


