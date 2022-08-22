from settings import *
from csv_data_extraction_and_tasks_creation import DataExtractionTaskCreation
from auxiliary_functions import calculateTime, checkRunningJobs, checkCondorStatus
from local_testing import LocalTesting
from file_managment import FileManagement
from py_condor import Job
from bat_creation import BatCreator


@calculateTime
def main() -> None:
    data: DataExtractionTaskCreation = DataExtractionTaskCreation(CSV_FILE, project_name=PROJECT_NAME, keyword=KEYWORD)
    tasks: list[str] = data.tasks

    if TEST_ON_LOCAL:
        LocalTesting(folder=WORKING_DIRECTORY, g4m_executable=G4M_GLOBAL_EXE, tasks=tasks)

    if RUN_CONDOR:
        checkCondorStatus()

        files: FileManagement = FileManagement(PROJECT_NAME, SCENARIOS_DATA, WORKING_DIRECTORY / CONDOR_OUTPUT_FOLDER,
                                               cwd=WORKING_DIRECTORY).archiveDefaultData()

        bat_0: BatCreator = BatCreator(file_name=EXECUTABLE_0, output_folder=CONDOR_OUTPUT_FOLDER,
                                       file_archiver=FILE_ARCHIVER.name,
                                       archives=[files.defaultData],
                                       executable=G4M_GLOBAL_EXE.name).create_bat()
        print(bat_0)

        job_0: Job = Job(f'{PROJECT_NAME}_0', EXECUTABLE_0.name, submit_folder=SUBMIT_FOLDER,
                         arguments=[x for x in tasks if int(x[-2:]) == 0],
                         should_transfer_files='YES', transfer_output_files=['out'],
                         transfer_input_files=[files.defaultData, G4M_GLOBAL_EXE.name, FILE_ARCHIVER.name],
                         notification='Error', job_machine_attrs='Machine', job_machine_attrs_history_length=5,
                         request_memory='2GB', request_cpus=1, request_disk='1.5GB', rank='mips',
                         periodic_hold='(JobStatus == 7)',
                         periodic_release='(NumJobStarts <= 10) && (HoldReasonCode != 1) &&'
                                          '((time() - EnteredCurrentStatus) > 300)',
                         job_lease_duration=7200, on_exit_remove='(ExitBySignal == False) && (ExitCode == 0)',
                         on_exit_hold='(NumJobStarts > 10) && (ExitCode != 0)').build().submit(cwd=WORKING_DIRECTORY)
        print(job_0)

        checkRunningJobs(user='denys', update_s=60)

        files.archiveBauData()

        bat_1: BatCreator = BatCreator(file_name=EXECUTABLE_1, output_folder=CONDOR_OUTPUT_FOLDER,
                                       file_archiver=FILE_ARCHIVER.name,
                                       archives=[files.defaultData, files.bauData],
                                       executable=G4M_GLOBAL_EXE.name).create_bat()
        print(bat_1)

        job_1: Job = Job(f'{PROJECT_NAME}_1', EXECUTABLE_1.name, submit_folder=SUBMIT_FOLDER,
                         arguments=[x for x in tasks if int(x[-2:]) == -1],
                         should_transfer_files='YES', transfer_output_files=['out'],
                         transfer_input_files=[files.defaultData, files.bauData, G4M_GLOBAL_EXE.name,
                                               FILE_ARCHIVER.name],
                         notification='Error', job_machine_attrs='Machine', job_machine_attrs_history_length=5,
                         request_memory='2GB', request_cpus=1, request_disk='1.5GB', rank='mips',
                         periodic_hold='(JobStatus == 7)',
                         periodic_release='(NumJobStarts <= 10) && (HoldReasonCode != 1) &&'
                                          '((time() - EnteredCurrentStatus) > 300)',
                         job_lease_duration=7200, on_exit_remove='(ExitBySignal == False) && (ExitCode == 0)',
                         on_exit_hold='(NumJobStarts > 10) && (ExitCode != 0)').build().submit(cwd=WORKING_DIRECTORY)
        print(job_1)


if __name__ == '__main__':
    main()
