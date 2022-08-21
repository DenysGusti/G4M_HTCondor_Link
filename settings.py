from pathlib import Path

# G4M Project folder (where the g4m.exe and input data/folders are)
WORKING_DIRECTORY: Path = Path(r'C:\Users\denys\PycharmProjects\G4M_HTCondor_Link\data')

# Name of the scenario project
PROJECT_NAME: str = 'AEO2022_28042022'

# Name of GLOBIOM file variable from which the scenarios for running G4M are taken
VARIABLE: str = 'LandRent'
CSV_FILE: Path = WORKING_DIRECTORY / f'GLOBIOM2G4M_output_{VARIABLE}_{PROJECT_NAME}.csv'

# Keyword in the scenarios for finding the BAU (zero CO2 price) scenarios
KEYWORD: str = 'FOR000'  # something that is in name of base scenarios but isn't in name of others

# Name of the G4M executable
G4M_GLOBAL_EXE: Path = WORKING_DIRECTORY / 'g4m_global_AEO2022_28042022.exe'

# Do you run the model on local PC or on HTCondor?
TEST_ON_LOCAL: bool = False
RUN_CONDOR: bool = True

# HTCondor
# Names of the bat files used by HTCondor
SUBMIT_FOLDER: Path = WORKING_DIRECTORY / 'submit_folder'

EXECUTABLE_0: Path = Path(f'{PROJECT_NAME}_0.bat')
EXECUTABLE_1: Path = Path(f'{PROJECT_NAME}_1.bat')

FILE_ARCHIVER: Path = WORKING_DIRECTORY / '7za.exe'

SCENARIOS_DATA: Path = WORKING_DIRECTORY / 'data_files'
CONDOR_OUTPUT_FOLDER: Path = Path(r'out\cell')
