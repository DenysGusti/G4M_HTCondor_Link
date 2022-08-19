from pathlib import Path
from datetime import datetime
from subprocess import run
from shutil import move

from auxiliary_functions import calculateTime


class LocalTesting:
    def __init__(self, folder: Path, g4m_executable: Path, tasks: list[str]):
        self.folder: Path = folder
        self.g4m_executable: Path = g4m_executable
        self.tasks: list[str] = tasks

        for task in self.tasks:
            print(task)
            self.runScenario(task.split())

            if task[-1] == '0':
                self.moveFiles(task.split())

    @calculateTime
    def runScenario(self, words: list[str]) -> None:
        output_file: Path = self.folder / 'testruns' / f'test_g4m_{words[0]}_{words[2]}_{datetime.now():%d%m%Y}.txt'
        with open(output_file, 'w') as file:
            print([self.g4m_executable, *words], ' '.join([str(self.g4m_executable), *words]), sep='\n')
            run([self.g4m_executable, *words], stdout=file)

    def moveFiles(self, words: list[str]) -> None:
        for x in ['biomass_bau', 'NPVbau']:
            move(self.folder / 'out' / f'{x}_{words[0]}_{words[2]}.bin', self.folder / f'{x}_{words[0]}_{words[2]}.bin')
