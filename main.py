from settings import *
from csv_data_extraction_and_tasks_creation import DataExtractionTaskCreation
from auxiliary_functions import calculateTime, checkRunningJobs, checkCondorStatus
from local_testing import LocalTesting
from file_managment import FileManagement
from py_condor import Job


@calculateTime
def main() -> None:
    data: DataExtractionTaskCreation = DataExtractionTaskCreation(CSV_FILE, project_name=PROJECT_NAME, keyword=KEYWORD)
    tasks: list[str] = data.tasks

    if TEST_ON_LOCAL:
        LocalTesting(folder=FOLDER, g4m_executable=G4M_GLOBAL_EXE, tasks=tasks)

    if RUN_CONDOR:
        checkCondorStatus()

        files: FileManagement = FileManagement(FOLDER, PROJECT_NAME).archiveDefaultData()

        job0: Job = Job(f'{PROJECT_NAME}_0', EXECUTABLE_0, submit_folder=FOLDER / 'condor_test',
                        arguments=[x for x in tasks if int(x[-2:]) == 0],
                        should_transfer_files='YES', transfer_output_files=[Path('out')],
                        transfer_input_files=[files.defaultData, G4M_GLOBAL_EXE, FILE_ARCHIVER]).build().submit()
        print(job0)

        checkRunningJobs(user='denys', update_s=60)

        files.archiveBauData()

        job1: Job = Job(f'{PROJECT_NAME}_1', EXECUTABLE_1, submit_folder=FOLDER / 'condor_test',
                        arguments=[x for x in tasks if int(x[-2:]) == -1],
                        should_transfer_files='YES', transfer_output_files=[Path('out')],
                        transfer_input_files=[files.defaultData, files.bau_data_archive,
                                              G4M_GLOBAL_EXE, FILE_ARCHIVER]).build().submit()
        print(job1)


if __name__ == '__main__':
    main()
