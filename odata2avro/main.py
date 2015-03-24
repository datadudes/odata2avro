import collections
import json
from xml.etree import ElementTree

import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
import click


NS = '{http://www.w3.org/2005/Atom}'
NS_M = '{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}'
NS_DS = '{http://schemas.microsoft.com/ado/2007/08/dataservices}'

ENTRY_PROPERTIES_XPATH = './{entry}/{content}/{properties}'.format(
    entry=NS+'entry', content=NS+'content', properties=NS_M+'properties')

ODATA_TO_AVRO_TYPE = {
    'Edm.Binary': 'string',
    'Edm.Boolean': 'boolean',
    'Edm.Byte': 'int',
    'Edm.DateTime': 'string',
    'Edm.Decimal': 'double',
    'Edm.Double': 'double',
    'Edm.Guid': 'string',
    'Edm.Int16': 'int',
    'Edm.Int32': 'int',
    'Edm.Int64': 'int',
    'Edm.SByte': 'int',
    'Edm.Single': 'string',
    'Edm.String': 'string',
    'Edm.Time': 'string',
    'Edm.DateTimeOffset': 'string'
}


class ODataProperty():
    def __init__(self, xml_elem):
        self.elem = xml_elem

    def name(self):
        return self.elem.tag[len(NS_DS):]

    def type(self):
        return self.elem.attrib.get(NS_M+'type', 'Edm.String')

    def value(self):
        if self.is_null():
            return None

        avro_type = ODATA_TO_AVRO_TYPE[self.type()]
        val = self.elem.text
        if avro_type == 'string':
            return val
        elif avro_type == 'int':
            return int(val)
        elif avro_type == 'double':
            return float(val)
        elif avro_type == 'boolean':
            return True if val == 'true' else False
        else:
            assert False, "Unknown AVRO type '{0}'".format(avro_type)

    def is_null(self):
        return self.elem.attrib.get(NS_M+'null', 'false') == 'true'


def parse_schema(xml_tree):
    """
    Read schema of OData objects from xml. Returns a dict in form
    {field_name: field_type}, where field_type is one of OData primitive types.
    See http://www.odata.org/documentation/odata-version-2-0/json-format
    """
    schema = xml_tree.find(ENTRY_PROPERTIES_XPATH)
    return {e.name(): e.type() for e in map(ODataProperty, schema)}


def schema_to_avsc(schema):
    """ Convert schema given as dict {field_name:field_type} to Avro schema. """
    schema_sorted = collections.OrderedDict(sorted(schema.items()))
    return {
        "namespace": "odata.avro",
        "type": "record",
        "name": "Record",
        "fields": [
            {"name": name,  "type": [ODATA_TO_AVRO_TYPE[type_], 'null']}
            for name, type_ in schema_sorted.iteritems()
        ]
    }


def get_records_from(xml_tree):
    """
    Convert xml OData entries into a list of dictionaries
    """
    entry_properties_list = xml_tree.findall(ENTRY_PROPERTIES_XPATH)
    for entry_properties in entry_properties_list:
        properties = map(ODataProperty, entry_properties)
        record = {p.name(): p.value() for p in properties}
        yield record


def save_avro_schema(avsc, output_file):
    with open(output_file, 'w') as outfile:
        json.dump(avsc, outfile)


def save_xml_to_avro(xml_tree, avsc, output_file):
    schema = avro.schema.parse(json.dumps(avsc))
    with open(output_file, 'w') as output_file:
        writer = DataFileWriter(output_file, DatumWriter(), schema)
        for record in get_records_from(xml_tree):
            writer.append(record)
        writer.close()


def main(xml_file, avro_schema, avro_file):
    with open(xml_file, 'r') as f:
        xml_as_string = f.read()
        xml_tree = ElementTree.fromstring(xml_as_string)
        schema = parse_schema(xml_tree)
        avsc = schema_to_avsc(schema)
        save_avro_schema(avsc, avro_schema)
        save_xml_to_avro(xml_tree, avsc, avro_file)


@click.command()
@click.argument('input_odata_xml_file', type=click.Path(exists=True))
@click.argument('output_avro_schema', type=click.Path())
@click.argument('output_avro_file', type=click.Path())
def cli(input_odata_xml_file, output_avro_schema, output_avro_file):
    main(input_odata_xml_file, output_avro_schema, output_avro_file)
