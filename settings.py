from pathlib import Path

# G4M Project folder (where the g4m.exe and input data/folders are)
WORKING_DIRECTORY: Path = Path(r'C:\Users\denys\PycharmProjects\G4M_HTCondor_Link\data')
# WORKING_DIRECTORY: Path = Path(r'D:\MGusti\CurrentWork\GFM\georgPrgs\dima\DeforAforCCurves_growth\ManagementPlus\GUI'
#                                r'\progr_no_interpol\newAgeStruct\newInterfase_codeTest\data')
# Name of the scenario project
PROJECT_NAME: str = 'AEO2022_28042022'

# Keyword in the scenarios for finding the BAU (zero CO2 price) scenarios
# something that is in the names of BAU (zero CO2 price) scenarios but isn't in the names of the other scenarios
KEYWORD: str = 'FOR000'

# Name of the G4M executable
G4M_GLOBAL_EXE: Path = WORKING_DIRECTORY / 'g4m_global_AEO2022_28042022.exe'

# Do you run the model on local PC or on HTCondor?
TEST_ON_LOCAL: bool = False
RUN_CONDOR: bool = False

# HTCondor
# Names of the bat files used by HTCondor
SUBMIT_FOLDER: Path = WORKING_DIRECTORY / 'submit_folder'

EXECUTABLE_0: Path = WORKING_DIRECTORY / f'{PROJECT_NAME}_0.bat'
EXECUTABLE_1: Path = WORKING_DIRECTORY / f'{PROJECT_NAME}_1.bat'

FILE_ARCHIVER: Path = WORKING_DIRECTORY / '7za.exe'

SCENARIOS_DATA: Path = WORKING_DIRECTORY / 'data_all'
CONDOR_OUTPUT_FOLDER: Path = Path(r'out\cell')

# Name of GLOBIOM file variable from which the scenarios for running G4M are taken
VARIABLE: str = 'LandRent'
CSV_FILE: Path = SCENARIOS_DATA / f'data_{PROJECT_NAME}' / f'GLOBIOM2G4M_output_{VARIABLE}_{PROJECT_NAME}.csv'

# USER: str = 'gusti'
USER: str = 'denys'
UPDATE_TIME: int = 60

JOB_TEMPLATE: dict[str, str | int] = {
    'notification': 'Error',
    'job_machine_attrs': 'Machine',
    'job_machine_attrs_history_length': 5,
    'request_memory': '2GB',
    'request_cpus': 1,
    'request_disk': '1.5GB',
    'rank': 'mips',
    'periodic_hold': '(JobStatus == 7)',
    'periodic_release': '(NumJobStarts <= 10) && (HoldReasonCode != 1) && ((time() - EnteredCurrentStatus) > 300)',
    'job_lease_duration': 7200,
    'on_exit_remove': '(ExitBySignal == False) && (ExitCode == 0)',
    'on_exit_hold': '(NumJobStarts > 10) && (ExitCode != 0)'
}

MERGE_EXE: Path = WORKING_DIRECTORY / 'tableMerge_EPA_csv_linker_new.exe'
MERGE_OUT: Path = WORKING_DIRECTORY / 'merged'
