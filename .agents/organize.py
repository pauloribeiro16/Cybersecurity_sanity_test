import os
import shutil

BASE_DIR = "/home/epmq/Desktop/Projects/Cybersecurity_sanity_test"

# Mapping: Folder -> List of absolute filenames (relative to root)
MAPPING = {
    "Scripts_Testing": [
        "Cybersecurity_inference_tester.py",
        "cybersecurity_sanity_tester.py",
        "cybersecurity_sanity_tester_CyberMetric.py",
        "Cybersecurity_santy_Teste_With_Context.py",
        "threat_model_tester.py",
        "api_rate_tester.py",
        "debug_aggregate.py"
    ],
    "Scripts_Analysis": [
        "aggregate_cybermetrics.py",
        "analyze_cyber_test_results.py",
        "analyze_cyber_test_results_CyberMetrics.py",
        "analyze_cyber_test_results_CyberMetrics_Mine.py",
        "analyze_cyber_test_results_modified.py",
        "evaluate_threat_Models.py"
    ],
    "Scripts_Utils": [
        "Script_add_option.py",
        "api_sanity_check.py"
    ],
    "Data_and_Logs": [
        "CyberMetrics_Analysis.xlsx",
        "Test_Summary_Report.xlsx",
        "Results.json",
        "Results_Teste_3.json",
        "ThreatModel_Tests.json",
        "uco_1_5.txt",
        "Testes"
    ],
    "Web_Views": [
        "dashboard.html"
    ]
}

# 1. Create Directories
for folder in MAPPING.keys():
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

moved_files = []

# 2. Move Files
for folder, files in MAPPING.items():
    for f in files:
        src = os.path.join(BASE_DIR, f)
        dst = os.path.join(BASE_DIR, folder, f)
        
        if os.path.exists(src):
            try:
                shutil.move(src, dst)
                moved_files.append(f"Moved {f} to {folder}/")
                print(f"[{folder}] Moved {f}")
            except Exception as e:
                print(f"Error moving {f}: {e}")
        else:
            print(f"Skipping {f} (doesn't exist in root)")

# 3. Fix Scripts with `__file__`
# Inside Scripts_Testing, they now need to look one directory higher.
test_folder = os.path.join(BASE_DIR, "Scripts_Testing")
files_to_adjust = [
    "cybersecurity_sanity_tester_CyberMetric.py",
    "Cybersecurity_inference_tester.py",
    "Cybersecurity_santy_Teste_With_Context.py",
    "threat_model_tester.py",
    "cybersecurity_sanity_tester.py"
]

target_content = "SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))"
# We match EXACT spacing from our grep
# content on line 25, 24, etc.
# grep showed: "SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))"

replacement_content = "SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))"

for f_name in files_to_adjust:
    file_path = os.path.join(test_folder, f_name)
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if target_content in content:
                content = content.replace(target_content, replacement_content)
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Adjusted SCRIPT_DIR in {f_name}")
            else:
                print(f"No match for SCRIPT_DIR in {f_name}")
        except Exception as e:
             print(f"Error adjusting {f_name}: {e}")
    else:
         print(f"Could not find {f_name} to adjust.")

# Create a summary output for the user
with open(os.path.join(BASE_DIR, "moved_files_summary.txt"), 'w') as f:
    f.write("# Summary of File Organization\n\n")
    for move in sorted(moved_files):
        f.write(f"- {move}\n")
    f.write("\n## Path Adjustments\n")
    f.write("Scripts in `Scripts_Testing/` have been updated to adjust `SCRIPT_DIR` with `dirname(dirname(__file__))` to retain path compliance with data folders.\n")

print("Finished fully.")
