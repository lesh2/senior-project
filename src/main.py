import calculations
import databasenames as names
def main():
   # print('DATA FOR SAA')
   # calculations.calculate_stats('SAA')
   # print('DATA FOR MIAC:')
   # calculations.calculate_stats('MIAC')
   # print('DATA FOR WIAC:')
   # calculations.calculate_stats('WIAC')
   # print('DATA FOR NWC:')
   # calculations.calculate_stats('NWC')
   # print('DATA FOR CCIW:')
   # calculations.calculate_stats('CCIW')
   # print('DATA FOR OAC:')
   # calculations.calculate_stats('OAC')
   # print('DATA FOR ASC:')
   # calculations.calculate_stats('ASC')
   # print('DATA FOR E8:')
   # calculations.calculate_stats('E8')
    print('DATA FOR ALL CONFERENCES:')
    calculations.calculate_stats('ALL', names.adjusted)

main()
