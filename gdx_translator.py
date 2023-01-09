import gdxpds
import pandas as pd
from pathlib import Path
import logging


class GDXTranslator:
    def __init__(self, gdx_path: Path | str, csv_output_folder: Path | str, project_name: str):
        self.gdx_path: Path = gdx_path
        self.csv_output_folder: Path = csv_output_folder
        self.project_name: str = project_name

        self.dataframes = gdxpds.to_dataframes(self.gdx_path)
        self.default_columns_dict: dict[str, tuple[list[str], list[int]]] = {
            'G4Mm_SupplyResidues': (['REGION', 'G4MmItem', 'G4MmLogs', 'SCEN1', 'SCEN3', 'SCEN2'],
                                    [2, 0, 1, 3, 4, 5]),
            'G4Mm_SupplyWood': (['REGION', 'G4MmItem', 'G4MmLogs', 'SCEN1', 'SCEN3', 'SCEN2'],
                                [2, 0, 1, 3, 4, 5]),
            'G4Mm_Wood_price': (['REGION', 'G4MmItem', 'G4MmLogs', 'SCEN1', 'SCEN3', 'SCEN2'],
                                [2, 0, 1, 3, 4, 5]),
            'G4Mm_LandRent': (['REGION', 'LC_TYPE', 'SCEN1', 'SCEN3', 'SCEN2'],
                              [1, 0, 2, 3, 4]),
            'G4Mm_CO2PRICE': (['REGION', 'SCEN1', 'SCEN3', 'SCEN2'],
                              [0, 1, 2, 3])}

        self.symbol_name: str | None = None
        self.df_table: list[list] | None = None
        self.data: dict[str | int, list[str | float]] | None = None
        self.processSymbolNames()

    def processSymbolNames(self) -> None:
        for self.symbol_name in self.dataframes.keys():
            if self.default_columns_dict.get(self.symbol_name):
                self.getData().processData().createFile()
            else:
                print(f"{self.symbol_name} isn't handled yet")

    def __str__(self):
        return f'gdx path: {self.gdx_path}\ncsv output folder: {self.csv_output_folder}\n' \
               f'symbol names: {", ".join(self.dataframes.keys())}'

    def getData(self) -> 'GDXTranslator':
        def renamer(x: str, i: list[int] = [0]) -> int:
            """turns * * * * * to 0 1 2 3 4 5"""
            i[0] += 1
            return i[0]

        df_list = list(self.dataframes[self.symbol_name].rename(columns=renamer).to_dict().values())
        self.df_table = [list(column.values()) for column in df_list]
        return self

    def processData(self) -> 'GDXTranslator':
        default_columns, default_permutation = self.default_columns_dict[self.symbol_name]
        years: list[int] = [int(year) for year in sorted(set(self.df_table[len(default_columns)]))]

        self.data = {col: [] for col in [*default_columns, *years]}

        cur_year_idx: int = 0
        cur_scen: str = ''
        n: int = len(default_columns)

        for i in range(len(self.df_table[0])):

            if cur_scen != self.df_table[n - 1][i]:
                cur_scen = self.df_table[n - 1][i]

                for j, col in zip(default_permutation, default_columns):
                    self.data[col].append(self.df_table[j][i])

            while years[cur_year_idx] != int(self.df_table[n][i]):
                self.data[years[cur_year_idx]].append(0.)
                cur_year_idx = (cur_year_idx + 1) % len(years)

            self.data[years[cur_year_idx]].append(self.df_table[n + 1][i])
            cur_year_idx = (cur_year_idx + 1) % len(years)

        return self

    def createFile(self) -> 'GDXTranslator':
        try:
            if not self.csv_output_folder.exists():
                self.csv_output_folder.mkdir(parents=True)
            pd.DataFrame(data=self.data).to_csv(
                self.csv_output_folder / f'GLOBIOM2G4M_output_{self.symbol_name.split("_")[1]}_{self.project_name}.csv',
                index=False)
        except PermissionError:
            logging.exception('\n\nClose destination csv file!\n\n')
        finally:
            return self
