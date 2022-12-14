import pandas as pd

from pathlib import Path


class DataExtractionTaskCreation:
    """
    Preparing the input data and scenario list for running G4M
    """

    def __init__(self, csv_file: Path, *, project_name: str, keyword: str):
        self.csv_file: Path = csv_file
        self.project_name: str = project_name
        self.keyword: str = keyword  # something that is in base scenarios but isn't in others

        self.csv_dict: dict[str, dict[int, str | float]] = pd.read_csv(self.csv_file).to_dict()
        self._scenarios: list[list[str]] = self.extractScenarios()
        self._tasks: list[str] = self.formTasks()
        self._cpp_tasks: list[str] = self.formCppTasks()

    def extractScenarios(self) -> list[list[str]]:
        columns_names: list[str] = list(self.csv_dict.keys())[2:5]
        countries: dict[int, str] = list(self.csv_dict.values())[0]

        columns_data: list[list[str]] = [[self.csv_dict[x][i] for x in columns_names]
                                         for i in self.csv_dict[columns_names[0]].keys() if
                                         countries[i] == countries[0]]

        return columns_data

    def formTasks(self) -> list[str]:
        joined_scenarios: list[str] = ['_'.join(x) for x in self._scenarios]
        base_scenario: str = 'not found'

        tasks: list[str] = [
            ' '.join([self.project_name, *([base_scenario := scenario, base_scenario, '0'] if self.keyword in scenario
                                           else [base_scenario, scenario, '-1'])]) for scenario in joined_scenarios]
        tasks.sort(key=lambda x: int(x[-2:]), reverse=True)

        return tasks

    def formCppTasks(self) -> list[str]:
        tasks: list[str] = [
            ' '.join([jt_scenario, '__'.join(scen_list), '0'] if self.keyword in (jt_scenario := '_'.join(scen_list))
                     else [jt_scenario, '__'.join(scen_list), '-1']) for scen_list in self._scenarios]

        return tasks

    def __str__(self):
        return f'''DataExtractionTaskCreation:
                reading from {self.csv_file}
                
                project name: {self.project_name}
                
                distinguish key: {self.keyword}
                
                data:
                {self.csv_dict}
                
                scenarios: {self._scenarios}
                
                tasks: {self._tasks}
                
                cpp tasks: {self._cpp_tasks}
                '''

    @property
    def scenarios(self) -> list[list[str]]:
        return self._scenarios

    @scenarios.setter
    def scenarios(self, value) -> None:
        self._scenarios = value

    @property
    def tasks(self) -> list[str]:
        return self._tasks

    @tasks.setter
    def tasks(self, value) -> None:
        self._tasks = value

    @property
    def cpp_tasks(self) -> list[str]:
        return self._cpp_tasks

    @cpp_tasks.setter
    def cpp_tasks(self, value) -> None:
        self._cpp_tasks = value
