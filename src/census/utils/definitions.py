import json

# load json dictionary from BirdNET to translate the species codes
taxonomy = json.load(open("../metadata/eBird_taxonomy_codes_2018.json", "r"))

