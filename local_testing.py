from pathlib import Path
from datetime import datetime
from subprocess import run
from shutil import move

from auxiliary_functions import calculateTime


class LocalTesting:
    """
    Running G4M on local PC
    """

    def __init__(self, folder: Path, g4m_executable: Path, tasks: list[str]):
        self.folder: Path = folder
        self.g4m_executable: Path = g4m_executable
        self.tasks: list[str] = tasks

        self.tests_folder: Path = self.folder / 'testruns'
        self.out_folder: Path = self.folder / 'out' / 'cell'

        if not self.tests_folder.exists():
            self.tests_folder.mkdir(parents=True)
        if not self.out_folder.exists():
            self.out_folder.mkdir(parents=True)

        for task in self.tasks:
            print(task)
            self.runScenario(task.split())

            if task[-1] == '0':
                self.moveFiles(task.split())

    @calculateTime
    def runScenario(self, words: list[str]) -> None:
        output_file: Path = self.tests_folder / f'test_g4m_{words[0]}_{words[2]}_{datetime.now():%d%m%Y}.txt'
        with open(output_file, 'w') as file:
            print(' '.join([str(self.g4m_executable), *words]))
            run([self.g4m_executable, *words], stdout=file, cwd=self.folder)

    def moveFiles(self, words: list[str]) -> None:
        """
        Moving the BAU files created under zero CO2 price scenarios
        to the input data folder for running the non-zero CO2 price scenarios
        """
        for x in ['biomass_bau', 'NPVbau']:
            move(self.out_folder / f'{x}_{words[0]}_{words[2]}.bin', self.folder / f'{x}_{words[0]}_{words[2]}.bin')
