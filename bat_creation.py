from pathlib import Path


class BatCreator:
    def __init__(self, file_name: Path | str, output_folder: Path | str, file_archiver: Path | str,
                 archives: list[Path | str], executable: Path | str):
        self.file_name: Path | str = file_name
        self.output_folder: Path | str = output_folder
        self.file_archiver: Path | str = file_archiver
        self.archives: list[Path | str] = archives
        self.executable: Path | str = executable

        self.lines: list[str] = ['set /A errno=0\n',
                                 f'md {self.output_folder}\n',
                                 *[f'{self.file_archiver} x {a} -y > NUL' for a in self.archives],
                                 '\ndir\n',
                                 '@echo arguments 1: %1 2: %2 3: %3 4: %4\n',
                                 f'{self.executable} %1 %2 %3 %4\n',
                                 'if %errorlevel% neq 0 set /A errno=%errorlevel%\n',
                                 'del *.txt',
                                 'del *.ini',
                                 'del simu.bin',
                                 '\nexit /B %errno%\n']

    def create_bat(self) -> 'BatCreator':
        with open(self.file_name, 'w') as file:
            file.write('\n'.join(self.lines))

        return self

    def __str__(self) -> str:
        return f'\nBat file:\t{self.file_name}\nLines:\n' + '\n'.join(self.lines)
