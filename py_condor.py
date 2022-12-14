from subprocess import run
from pathlib import Path
from datetime import datetime


class Job:
    """
    https://htcondor.readthedocs.io/en/latest/man-pages/condor_submit.html
    """

    def __init__(self, name: str, executable: Path | str, submit_folder: Path, *,
                 request_memory: int | str = None, request_disk: int | str = None, request_cpus: int = None,
                 universe: str = None, should_transfer_files: str = None, requirements: str = None, rank: str = None,
                 notification: str = None, when_to_transfer_output: str = None,
                 job_machine_attrs: str = None, job_machine_attrs_history_length: int = None,
                 periodic_hold: str = None, periodic_release: str = None, job_lease_duration: int = None,
                 on_exit_remove: str = None, on_exit_hold: str = None,
                 transfer_input_files: list[Path | str] = None, transfer_output_files: list[Path | str] = None,
                 arguments: list[str] = None, queue: int = None, **kwargs):
        self.name: str = name
        self.executable: Path | str = executable
        self.submit_folder: Path = submit_folder

        self.request_memory: int | str = request_memory
        self.request_disk: int | str = request_disk
        self.request_cpus: int = request_cpus

        self.universe: str = universe
        self.should_transfer_files: str = should_transfer_files
        self.requirements: str = requirements
        self.rank: str = rank
        self.notification: str = notification
        self.when_to_transfer_output: str = when_to_transfer_output

        self.job_machine_attrs: str = job_machine_attrs
        self.job_machine_attrs_history_length: int = job_machine_attrs_history_length
        self.periodic_hold: str = periodic_hold
        self.periodic_release: str = periodic_release
        self.job_lease_duration: int = job_lease_duration
        self.on_exit_remove: str = on_exit_remove
        self.on_exit_hold: str = on_exit_hold

        self.transfer_input_files: list[Path | str] = transfer_input_files
        self.transfer_output_files: list[Path | str] = transfer_output_files
        self.arguments: list[str] = arguments
        self.queue: int = queue

        self.lines: list[str] = []
        self.submit_file: Path = Path()

        print('Not processed arguments: ', kwargs)
        self.kwargs: dict = kwargs

    def build(self) -> 'Job':
        files_name: str = f'{self.name}_{datetime.now():%d%m%Y}.$(Cluster).$(Process)'
        self.lines += [f'{x} = {self.submit_folder / x / f"{files_name}.{x[:3]}"}' for x in ['output', 'log', 'error']]

        if not self.submit_folder.exists():
            self.submit_folder.mkdir(parents=True)
        for x in ['output', 'log', 'error']:
            if not (subdir := self.submit_folder / x).exists():
                subdir.mkdir()

        self.lines.append('')
        submit_attrs: list[str] = ['executable', 'request_memory', 'request_disk', 'request_cpus', 'universe',
                                   'should_transfer_files', 'requirements', 'rank', 'notification',
                                   'when_to_transfer_output', 'job_machine_attrs', 'job_machine_attrs_history_length',
                                   'periodic_hold', 'job_lease_duration', 'on_exit_remove', 'on_exit_hold',
                                   'transfer_input_files', 'transfer_output_files']
        self.lines += [f'{x} = {", ".join(str(y) for y in arg) if isinstance(arg := getattr(self, x), list) else arg}'
                       for x in submit_attrs if getattr(self, x)]
        # unprocessed arguments
        self.lines += [f'{key} = {", ".join(str(y) for y in value) if isinstance(value, list) else value}'
                       for key, value in self.kwargs.items()]

        delim: str = '\n\t'
        self.lines.append(f'\nqueue {self.queue if self.queue else 1} args from (\n\t{delim.join(self.arguments)}\n)')

        self.submit_file = self.submit_folder / f'{self.name}.job' if self.submit_folder else Path(f'{self.name}.job')

        with open(self.submit_file, 'w') as file:
            file.write('\n'.join(self.lines))

        return self

    def submit(self, cwd: Path) -> 'Job':
        run(['condor_submit', self.submit_file], cwd=cwd)
        return self

    def __str__(self):
        return f'\nJob file name:\n{self.submit_file}\nJob description:\n' + '\n'.join(self.lines)
