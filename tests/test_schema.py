from odata2avro.main import parse_schema, schema_to_avsc
from xml.etree import ElementTree


def test_schema_parsing():
    with open("tests/example_schema.xml", "r") as test_schema:
        xml_str = test_schema.read()
        xml_tree = ElementTree.fromstring(xml_str)
        schema = parse_schema(xml_tree)
        assert schema == {
            'Vermogen': 'Edm.Int16',
            'Aantalcilinders': 'Edm.Int16',
            'BPM': 'Edm.Int32',
            'Eerstekleur': 'Edm.String',
            'Zuinigheidslabel': 'Edm.String'
        }


def test_schema_to_avsc():
    schema = {
        'Vermogen': 'Edm.Int16',
        'Aantalcilinders': 'Edm.Int16',
        'BPM': 'Edm.Int32',
        'Eerstekleur': 'Edm.String',
        'Zuinigheidslabel': 'Edm.String'
    }
    assert schema_to_avsc(schema) == {
        "namespace": "odata.avro",
        "type": "record",
        "name": "Record",
        "fields": [
            {"name": "Aantalcilinders",  "type": ["int", "null"]},
            {"name": "BPM", "type": ["int", "null"]},
            {"name": "Eerstekleur", "type": ["string", "null"]},
            {"name": "Vermogen", "type": ["int", "null"]},
            {"name": "Zuinigheidslabel", "type": ["string", "null"]}
        ]
    }