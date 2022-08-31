from pathlib import Path
from subprocess import run


class Merger:
    def __init__(self, *, project_name: str, merge_exe: Path, inpath: Path, outpath: Path, work_dir: Path,
                 tasks: list[str]):
        self.project_name = project_name
        self.merge_exe = merge_exe
        self.inpath = inpath
        self.outpath = outpath
        self.work_dir = work_dir
        self.tasks: list[str] = tasks

    def merge(self) -> 'Merger':
        if not self.outpath.exists():
            self.outpath.mkdir(parents=True)

        run(f'{self.merge_exe} {self.inpath} {self.outpath} {self.project_name} {" ".join(self.tasks)}',
            cwd=self.work_dir)
        return self

    def __str__(self) -> str:
        return f'{self.merge_exe} {self.inpath} {self.outpath} {self.project_name} {" ".join(self.tasks)}'
