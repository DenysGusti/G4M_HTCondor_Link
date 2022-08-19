from pathlib import Path

FOLDER: Path = Path(r'C:\Users\denys\PycharmProjects\GLOBIOM-G4M-link\G4M\Data\Default')

PROJECT_NAME: str = 'AEO2022_28042022'
VARIABLE: str = 'LandRent'
CSV_FILE: Path = FOLDER / f'GLOBIOM2G4M_output_{VARIABLE}_{PROJECT_NAME}.csv'

KEYWORD: str = 'FOR000'  # something that is in name of base scenarios but isn't in name of others
G4M_GLOBAL_EXE: Path = FOLDER / 'g4m_global_AEO2022_28042022.exe'

TEST_ON_LOCAL: bool = False
RUN_CONDOR: bool = True

# HTCondor

EXECUTABLE_0: Path = FOLDER / 'AEO2022_28042022_0.bat'
EXECUTABLE_1: Path = FOLDER / 'AEO2022_28042022_1.bat'
FILE_ARCHIVER: Path = FOLDER / '7za.exe'
