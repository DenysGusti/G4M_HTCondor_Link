#include <iostream>
#include <string>
#include <vector>
#include <array>
#include <format>

#include "./g4m_GUI_elements/IntToStr.cpp"
#include "./g4m_GUI_elements/tableData.cpp" // Elements for preparing output for GDataView

int main(const int argc, const char *argv[]) {
    const string inPath = argv[1], outPath = argv[2], suffix = argv[3];

    const size_t N_Scenarios = (argc - 4) / 3;
    vector<tuple<string, string, int> > scenarios;

    scenarios.reserve(N_Scenarios);
    for (size_t i = 0; i < N_Scenarios; ++i)
        scenarios.emplace_back(argv[4 + 3 * i], argv[5 + 3 * i], stoi(argv[6 + 3 * i]));

    cout << "Scenarios:\n";
    for (const auto &[scenario, scenario_names, co2_price]: scenarios)
        cout << scenario << ' ' << scenario_names << ' ' << co2_price << '\n';
    cout << "\nNumber of scenarios: " << scenarios.size() << "\n\n";

    const array<string, 2> tableTypes = {"tabs_gui", "tabs_reg_gui"}; // country or region table
    for (tableData tableObj0; const auto &tableType: tableTypes) {
        for (string tableName; const auto &[scenario, scenario_names, co2_price]: scenarios) {
            // C++20 python formatting, for now added in MSVC (2022) https://en.cppreference.com/w/cpp/compiler_support
            tableName = format("{}/{}_{}_{}{}.gdc", inPath, tableType, suffix, scenario, !co2_price ? "_Pco2_0" : "");
            cout << tableName << '\n';

            tableData tableObj(tableName);
            tableObj.updateDimEl("Scenario", 0, scenario_names);
            tableObj0.append(tableObj, 0);
        }
        tableObj0.SaveToFileCSV(outPath, tableType + suffix + "final", true);
        tableObj0.clear();
        cout << "\n---------------------------------------------------------------\n\n";
    }
    cout << "***************************************************************\n" << endl;
    return 0;
}