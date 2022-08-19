from pathlib import Path
from shutil import make_archive, copy

from auxiliary_functions import calculateTime


class FileManagement:
    def __init__(self, folder: Path, project_name: str):
        self.folder: Path = folder
        self.project_name: str = project_name

        self.data_folder: Path = self.folder / 'data'
        self.out_folder: Path = self.folder / 'out' / 'cell'

        self.default_data_archive: Path = self.data_folder / f'data_{self.project_name}.zip'
        self.bau_data_archive: Path = self.out_folder / f'bau_data_{self.project_name}.zip'

    @staticmethod
    def archive(files: list[Path], dst_folder: Path, archive: Path) -> None:
        tmp_folder: Path = dst_folder / 'tmp'

        try:
            tmp_folder.mkdir()
            for f in files:
                copy(f, tmp_folder)
            make_archive(str(archive).split('.')[0], archive.suffix[1:], tmp_folder)

        finally:
            for f in tmp_folder.iterdir():
                f.unlink()
            tmp_folder.rmdir()

    @calculateTime
    def archiveDefaultData(self) -> 'FileManagement':
        files: list[Path] = [f for d in self.data_folder.iterdir() if d.is_dir() for f in d.iterdir() if f.is_file()]
        print(*files, sep='\n')

        self.archive(files, self.data_folder, self.default_data_archive)

        return self

    @calculateTime
    def archiveBauData(self) -> 'FileManagement':
        files: list[Path] = [f for f in self.out_folder.iterdir() if f.is_file() and f.suffix == '.bin']
        print(*files, sep='\n')

        self.archive(files, self.out_folder, self.bau_data_archive)

        return self

    @property
    def defaultData(self) -> Path:
        return self.default_data_archive

    @property
    def bauData(self) -> Path:
        return self.bau_data_archive
