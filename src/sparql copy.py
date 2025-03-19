# SPARQL Libraries
import json
import xml.etree.ElementTree as ET
from SPARQLWrapper import SPARQLWrapper, POST, DIGEST, JSON

# Setup SPARQL Endpoint for GraphDB in Cloud
endpoint_url = "http://127.0.0.1:7200/repositories/dstv_nc_ontology"
endpoint_update_url = ("http://127.0.0.1:7200/repositories/dstv_nc_ontology/statements")

###########################################################
######### Basic SPARQL Methods                #############
###########################################################
sparql = SPARQLWrapper(endpoint=endpoint_url, updateEndpoint=endpoint_update_url)
sparql.setMethod(POST)
sparql.setReturnFormat(JSON)


def sparql_update(query):
    global sparql
    print("SPARQL Statement")
    print(query)
    sparql.setQuery(query)
    sparql.query()


def sparql_json_request(query):
    global sparql
    print("SPARQL Request")
    print(query)
    sparql.setQuery(query)
    ret = sparql.query()
    dictionary = ret.convert()
    return dictionary

#####################################################################
##           EXTRACT AS-PLAN DATA FROM DSTV-NC FILE                ##
#####################################################################

plan_data = "/Users/hejunjie/Documents/RWTH/Thesis/dstv_console/dstv_test.nc"

# Parse the XML file
tree = ET.parse(plan_data)  # Replace 'your_file.xml' with your actual file path
root = tree.getroot()

# Find all hljob elements
hljobs = root.findall(".//hljob")

# Extract and print the diameter values
for hljob in hljobs:
    diameter = hljob.get('diameter')
    print(f"Diameter: {diameter}")



#####################################################################
##           QUERY AS-BUILD DATA FROM INBUILT METROLOGY            ##
#####################################################################

metrology_data = "/Users/hejunjie/Documents/RWTH/Thesis/dstv_console/ibeam.json"

# Open and load the JSON file
with open(metrology_data, 'r') as measurement:
    asbuilt_data = json.load(measurement)

measuredLength = float(asbuilt_data["IBeam"]["length"]["value"])

print(f"The measured length of the I-Beam is {measuredLength}.")

deviation = measuredLength - planLength

print(f"The deviation  of the I-Beam length is {deviation}.")
#####################################################################
##           INSERT AS-PLAN DATA INTO DSTV ONTOLOGY                ##
#####################################################################

# Format the SPARQL INSERT query with the extracted value

query = f"""
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dstv: <http://w3id.org/dstv#>

INSERT DATA {{
    dstv:CutProcess09 a dstv:LengthSaw ;
               dstv:hasPlannedLength "{planLength}"^^xsd:float ;
               dstv:hasMeasuredLength "{measuredLength}"^^xsd:float ;
               dstv:hasDeviationValue "{deviation}"^^xsd:float ;.
    dstv:CutProcess07 a dstv:WebCut ;
               dstv:length "{planLength}"^^xsd:float .
}}
"""

sparql_update(query)