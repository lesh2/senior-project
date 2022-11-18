import calculations

def main():
    print('DATA FOR SAA')
    calculations.calculate_stats('SAA')
    print('DATA FOR MIAC:')
    calculations.calculate_stats('MIAC')
    print('DATA FOR WIAC:')
    calculations.calculate_stats('WIAC')
    print('DATA FOR NWC:')
    calculations.calculate_stats('NWC')
    print('DATA FOR CCIW:')
    calculations.calculate_stats('CCIW')

main()
