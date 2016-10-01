#!/usr/bin/env python3

from concept_map import ConceptMap


class CsvMap:

    def __init__(self, filename):
        import csv
        ## Parse csv into Python object
        d = {}
        with open(filename) as f:
            _ = f.readline()
            keyword = None
            for i in csv.reader(f):
                if i[0]:
                    keyword = i[0]
                    d[keyword] = []
                else:
                    d[keyword].append(i)

        ## read entries from Python object to construct a map
        self.name = d['Concept map name:'][0][1]
        self.question = d['Focus Question:'][0][1]

        self.attribute = {}  # (concept1, link, concept2): (supplied, correct, important, present-string, absent-string)
        
        self.map = ConceptMap()
        self.map.add_concepts(i[1] for i in d['Concepts:'])
        self.map.add_links(i[1] for i in d['Links:'])
        
        b = lambda x: True if x.lower() == 'yes' else False
        for i in d['Propositions:']:
            self.map.add_proposition((i[1], i[2], i[3]))
            # # # # (concept1, link, concept2) = (supplied, correct, important, present-string, absent-string)
            self.attribute[(i[1], i[2], i[3])] = (b(i[4]), b(i[5]), b(i[6]), i[7], i[8])

    def __repr__(self):
        l = []
        l.append('Name: ' + str(self.name))
        l.append(str(self.question))
        l.append(repr(self.map))
        return '\n'.join(l)


def outer_join(table1, col1, table2, col2):
    ret = []
    for i in table1:
        for j in table2:
            if i[col1] == j[col2]:
                ret.append(i + j)
    return ret

class CxlMap:

    def __init__(self, filename):
        
        ## Parse CmapTools exported cxl file into concet map object
        import xml.etree.ElementTree as ET
        m = ET.parse(filename).getroot().find('{http://cmap.ihmc.us/xml/cmap/}map')

        concepts = {}
        links = {}
        
        self.map = ConceptMap()
        for i in m.find('{http://cmap.ihmc.us/xml/cmap/}concept-list'):
            concepts[i.attrib['id']] = i.attrib['label']
            self.map.add_concept(i.attrib['label'])
            
        for i in m.find('{http://cmap.ihmc.us/xml/cmap/}linking-phrase-list'):
            links[i.attrib['id']] = i.attrib['label']
            self.map.add_link(i.attrib['label'])

        connections = []
        for i in m.find('{http://cmap.ihmc.us/xml/cmap/}connection-list'):
            connections.append((i.attrib['from-id'], i.attrib['to-id']))
        connections = outer_join(connections, 1, connections, 0)

        for i in connections:
            if i[0] in links:
                continue
            self.map.add_proposition((concepts[i[0]], links[i[1]], concepts[i[3]]))
            
    def __repr__(self):
        return repr(self.map)

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 3:
        print('Usage:\n\tpython parsers.py map.csv map.cxl')
        exit()

    csv = CsvMap(sys.argv[1])
    print('# csv map #')
    print(csv)
    print()
    
    cxl = CxlMap(sys.argv[2])
    print('# cxl map #')
    print(cxl)
    print()

