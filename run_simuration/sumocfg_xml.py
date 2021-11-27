import os
import xml.etree.ElementTree as ET


SIMULATION_PROGRAM_PATH = os.path.join(os.environ['HOME'], 
                        'Documents/21_大学書類/21_研究関連/research/bin/simuration_program')
print(SIMULATION_PROGRAM_PATH)
os.path.exists(SIMULATION_PROGRAM_PATH)

def out_sumocfg_xml() -> None:
    configuration = ET.Element(
        'configuration',
        {
            "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-innstance",
            "xsi:noNamespaceSchemaLocation":
            "http://sumo.dlr.de/xsd/sumoConfiguration.xsd"})
    tree = ET.ElementTree(element=configuration)

    input = ET.SubElement(configuration, 'input')
    ET.SubElement(input, "net-file", {"value": "test_net.xml"})
    ET.SubElement(input, "route-files", {"value": "test_row.xml"})

    time = ET.SubElement(configuration, 'time')
    ET.SubElement(time, 'begin', {'value': '500'})
    ET.SubElement(time, 'end', {'value': '1500'})
    ET.SubElement(time, 'step-length', {'value': '1'})

    # gui_only = ET.SubElement(configuration, 'gui_only')
    # ET.SubElement(
    #    gui_only, 'gui_setting_file', {
    #        'value': 'test_settings.xml'})

    out_put = ET.SubElement(configuration, 'output')
    ET.SubElement(
        out_put, 'fcd-output', {
            'value': "acc_output.xml"})
    ET.SubElement(
        out_put, 'fcd-output.acceleration', {'value': 'true'})

    tree.write(f'{SIMULATION_PROGRAM_PATH}/test_sumocfg.xml',
               encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    out_sumocfg_xml()

