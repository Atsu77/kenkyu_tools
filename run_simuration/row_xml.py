import os
import xml.etree.ElementTree as ET


SIMULATION_PROGRAM_PATH = os.path.join(os.environ['HOME'], 
                        'Documents/21_大学書類/21_研究関連/research/bin/simuration_program')
print(SIMULATION_PROGRAM_PATH)

def out_row_xml(departPos: int, departLane: int) -> None:
    routes = ET.Element('routes')
    tree = ET.ElementTree(element=routes)
    ET.SubElement(routes,
                  'vType',
                  {'id': 'Car',
                   "length": "3.3",
                   "width": "1.4",
                   "vClass": "passenger",
                   "maxSpeed": '26.3889'})
    ET.SubElement(routes,
                  'vType',
                  {'id': "Obstacle",
                   'color': '1,1,0',
                   'length': "1",
                   'width': "1",
                   'maxSpeed': "0.00000001",
                   'lcStrategic': '0',
                   'lcCooperative': '0',
                   'lcKeepRight': '0',
                   'vClass': "passenger"})

    flow = ET.SubElement(routes,
                         'flow',
                         {'id': "car",
                          'type': 'Car',
                          'begin': "0",
                          'end': "3000",
                          'probability': '1',
                          'departLane': 'random'})
    ET.SubElement(flow, 'route', {'edges': 'gneE1'})

    flow = ET.SubElement(routes,
                         'flow',
                         {"id": "obs",
                          "type": 'Obstacle',
                          "color": "1,1,1",
                          "begin": "0",
                          "end": "3500",
                          "departPos": f'{departPos}',
                          "period": "250",
                          "departLane": f'{departLane}'})
    ET.SubElement(flow, 'route', {'edges': 'gneE1'})

    tree.write(f'{SIMULATION_PROGRAM_PATH}/test_row.xml',
               encoding='utf-8', xml_declaration=True)

