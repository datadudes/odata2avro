import json
from xml.etree import ElementTree
from avro.datafile import DataFileReader
from avro.io import DatumReader
from odata2avro.main import parse_schema, schema_to_avsc, get_records_from, main


TEST_SCHEMA = {
    'Vermogen': 'Edm.Int16',
    'Aantalcilinders': 'Edm.Double',
    'BPM': 'Edm.Int32',
    'Eerstekleur': 'Edm.String',
    'Zuinigheidslabel': 'Edm.String',
    'Groen': 'Edm.Boolean'
}

TEST_AVRO_SCHEMA = {
    "namespace": "odata.avro",
    "type": "record",
    "name": "Record",
    "fields": [
        {"name": "Aantalcilinders",  "type": ["double", "null"]},
        {"name": "BPM", "type": ["int", "null"]},
        {"name": "Eerstekleur", "type": ["string", "null"]},
        {"name": "Groen", "type": ["boolean", "null"]},
        {"name": "Vermogen", "type": ["int", "null"]},
        {"name": "Zuinigheidslabel", "type": ["string", "null"]}
    ]
}


TEST_RECORDS = [{
    'Vermogen': None,
    'Aantalcilinders': 4.5,
    'BPM': None,
    'Eerstekleur': "GRIJS",
    'Zuinigheidslabel': None,
    'Groen': False,
}, {
    'Vermogen': 10,
    'Aantalcilinders': 5.1,
    'BPM': None,
    'Eerstekleur': 'GRIJS2',
    'Zuinigheidslabel': 'Test',
    'Groen': True
}]


def test_schema_parsing():
    with open("tests/data.xml", "r") as test_schema:
        xml_str = test_schema.read()
        xml_tree = ElementTree.fromstring(xml_str)
        schema = parse_schema(xml_tree)
        assert schema == TEST_SCHEMA


def test_schema_to_avsc():
    assert schema_to_avsc(TEST_SCHEMA) == TEST_AVRO_SCHEMA


def test_get_records_from_xml():
    with open("tests/data.xml", "r") as test_schema:
        xml_str = test_schema.read()
        xml_tree = ElementTree.fromstring(xml_str)
        records = [r for r in get_records_from(xml_tree)]
        assert records == TEST_RECORDS


def test_main(tmpdir):
    avro_schema = tmpdir.dirname + '/data-test.avsc'
    avro_file = tmpdir.dirname + '/data-test.avro'

    main('tests/data.xml', avro_schema, avro_file)

    with open(avro_schema, "r") as f:
        assert json.loads(f.read()) == TEST_AVRO_SCHEMA

    with open(avro_file, "r") as f:
        reader = DataFileReader(f, DatumReader())
        records = [r for r in reader]
        reader.close()
        assert records == TEST_RECORDS
