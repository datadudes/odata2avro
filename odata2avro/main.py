import urllib2
import json
import sys
from xml.etree import ElementTree

def download_as_json(url):
    print("Downloading: " + url)
    response = urllib2.urlopen(url)
    data = response.read()
    json_data = json.loads(data)
    return json_data


def get_total_count(url):
    data = download_as_json(url + '&$format=json&$inlinecount=allpages&$top=0')
    return data['d']['__count']


def parse_schema(xml):
    """
    Extract schema from xml given as string.
    Returns a dict in form {field_name: field_type}, where field_type
    is one of OData primitive types.

    See http://www.odata.org/documentation/odata-version-2-0/json-format
    """
    ns = '{http://www.w3.org/2005/Atom}'
    ns_m = '{http://schemas.microsoft.com/ado/2007/08/dataservices/metadata}'
    ns_ds = '{http://schemas.microsoft.com/ado/2007/08/dataservices}'
    root = ElementTree.fromstring(xml)
    schema = root.find(ns + 'entry').find(ns + 'content')\
        .find(ns_m + 'properties')

    name_of = lambda e: e.tag[len(ns_ds):]
    type_of = lambda e: e.attrib.get(ns_m+'type', 'Edm.String')

    return {name_of(e): type_of(e) for e in schema}
