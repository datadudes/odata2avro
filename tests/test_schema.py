from odata2avro.main import parse_schema


def test_schema_parsing():
    with open("tests/example_schema.xml", "r") as test_schema:
        xml_str = test_schema.read()
        schema = parse_schema(xml_str)
        assert schema == {
            'Vermogen': 'Edm.Int16',
            'Aantalcilinders': 'Edm.Int16',
            'BPM': 'Edm.Int32',
            'Eerstekleur': 'Edm.String',
            'Zuinigheidslabel': 'Edm.String'
        }
