import os
import json
import pandas as pd
import re

RESULTS_DIR = "ResultsCyberMetrics"
OUTPUT_MD = "Results_Summary_Dashboard_Debug.md"

def parse_filename_info(filename):
    is_modified = "Yes" if "_Modified" in filename or "_modified" in filename else "No"
    test_mode = "Two-Step" if "_TwoStep" in filename else "Probabilistic" if "_Probabilistic" in filename else "Standard"
    match = re.search(r'CyberMetric_(\d+)', filename)
    num_questions = match.group(1) if match else "Unknown"
    return num_questions, is_modified, test_mode

def aggregate():
    data = []
    if not os.path.exists(RESULTS_DIR):
        print(f"Directory {RESULTS_DIR} not found.")
        return
        
    count = 0
    for root, dirs, files in os.walk(RESULTS_DIR):
        for file in files:
            if file.endswith(".json"):
                count += 1
                file_path = os.path.join(root, file)
                print(f"[{count}] Parsing {file_path}...")
                
                rel_path = os.path.relpath(file_path, RESULTS_DIR)
                path_parts = rel_path.split(os.sep)
                if len(path_parts) >= 3:
                    model_family = path_parts[0]
                    model_params = path_parts[1]
                else:
                    model_family = "Unknown"
                    model_params = "Unknown"
                    
                num_questions, is_modified, test_mode = parse_filename_info(file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        result_dict = json.load(f)
                    summary = result_dict.get("summary", {})
                    
                    accuracy = "N/A"
                    if "accuracy" in summary:
                        accuracy = str(summary["accuracy"]).replace('%', '')
                    elif "accuracy_top_choice_percent" in summary:
                        accuracy = summary["accuracy_top_choice_percent"]
                        
                    total_time = summary.get("total_time_seconds", "N/A")
                    
                    data.append({
                        "Model Family": model_family,
                        "Params": model_params,
                        "Model Name": f"{model_family}:{model_params}",
                        "Dataset": f"CyberMetric-{num_questions}",
                        "Questions": int(num_questions) if num_questions.isdigit() else 0,
                        "Modified": is_modified,
                        "Mode": test_mode,
                        "Accuracy (%)": float(accuracy) if accuracy != "N/A" and accuracy else 0.0,
                        "Total Time (s)": float(total_time) if total_time != "N/A" and total_time else 0.0
                    })
                except Exception as e:
                     print(f"Error parsing {file_path}: {e}")

    print(f"Total files parsed: {count}")
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = aggregate()
    if not df.empty:
        print(df.head())
    else:
        print("No data collected.")
