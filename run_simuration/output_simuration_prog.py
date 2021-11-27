import os

from row_xml import out_row_xml
from sumocfg_xml import out_sumocfg_xml

SIMULATION_PROGRAM_PATH = os.path.join(os.environ['HOME'], 
                        'Documents/21_大学書類/21_研究関連/research/bin/simuration_program')

SIMULATION_DATA_PATH = os.path.join(os.environ['HOME'], 
                        'Documents/21_大学書類/21_研究関連/research/work/data')

print(os.getcwd())

def main():
    out_sumocfg_xml()
    for index, pos in enumerate(range(10, 1000, 20)):
        for lane in range(3):
            out_row_xml(departPos=1000+pos, departLane=lane)
            os.system(f"sumo {SIMULATION_PROGRAM_PATH}/test_sumocfg.xml")
            os.system(f"python xml2csv.py --separator , \
                {SIMULATION_PROGRAM_PATH}/acc_output.xml \
                -o {SIMULATION_DATA_PATH}/acc_obs[{index+1}][{lane+1}].csv")


if __name__ == '__main__':
    main()
