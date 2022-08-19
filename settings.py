from pathlib import Path

# G4M Project folder (where the g4m.exe and input data/folders are)
FOLDER: Path = Path(r'C:\Users\denys\PycharmProjects\GLOBIOM-G4M-link\G4M\Data\Default')

# Name of the scenario project
PROJECT_NAME: str = 'AEO2022_28042022'

# Name of GLOBIOM file variable from which the scenarios for running G4M are taken
VARIABLE: str = 'LandRent'
CSV_FILE: Path = FOLDER / f'GLOBIOM2G4M_output_{VARIABLE}_{PROJECT_NAME}.csv'

# Keyword in the scenarios for finding the BAU (zero CO2 price) scenarios
KEYWORD: str = 'FOR000'  # something that is in name of base scenarios but isn't in name of others

# Name of the G4M executable
G4M_GLOBAL_EXE: Path = FOLDER / 'g4m_global_AEO2022_28042022.exe'

# Do you run the model on local PC or on HTCondor?
TEST_ON_LOCAL: bool = False
RUN_CONDOR: bool = True

# HTCondor
# Names of the bat files used by HTCondor
EXECUTABLE_0: Path = FOLDER / 'AEO2022_28042022_0.bat'
EXECUTABLE_1: Path = FOLDER / 'AEO2022_28042022_1.bat'
FILE_ARCHIVER: Path = FOLDER / '7za.exe'
