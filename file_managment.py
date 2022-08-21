from pathlib import Path
from shutil import make_archive, copy

from auxiliary_functions import calculateTime


class FileManagement:
    def __init__(self, project_name: str, data_folder: Path, out_folder: Path):
        self.project_name: str = project_name

        self.data_folder: Path = data_folder  # input data folder
        self.out_folder: Path = out_folder  # output data folder

        if not self.out_folder.exists():
            self.out_folder.mkdir(parents=True)

        self.default_data_archive: Path = self.data_folder / f'data_{self.project_name}.zip'  # zipping the input data
        self.bau_data_archive: Path = self.out_folder / f'bau_data_{self.project_name}.zip'  # zipping the BAU data

        print(self.default_data_archive, self.bau_data_archive)

    @staticmethod
    def archive(files: list[Path], dst_folder: Path, archive: Path) -> None:
        tmp_folder: Path = dst_folder / 'tmp'
        print('compressing files:', *files, sep='\n')

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

        self.archive(files, self.data_folder, self.default_data_archive)

        return self

    @calculateTime
    def archiveBauData(self) -> 'FileManagement':
        files: list[Path] = [f for f in self.out_folder.iterdir() if f.is_file() and f.suffix == '.bin']

        if not files:
            raise Exception('bauData was not found!')

        self.archive(files, self.out_folder, self.bau_data_archive)

        return self

    @property
    def defaultData(self) -> str:
        return self.default_data_archive.name

    @property
    def bauData(self) -> str:
        return self.bau_data_archive.name
