import os
import json
import re
import pandas as pd
from collections import defaultdict

# --- CONFIGURATIONS ---
RESULTS_ROOT_DIR = "ResultsCyberMetrics"
OUTPUT_EXCEL_FILE = "CyberMetrics_Analysis.xlsx"
MANUAL_EVAL_KEY = "manual_overall_evaluation"

def find_and_map_results(root_dir: str) -> dict:
    """Finds all result files and maps them into a nested dictionary."""
    mapped_results = defaultdict(lambda: defaultdict(dict))
    if not os.path.isdir(root_dir):
        print(f"Error: Results directory '{root_dir}' not found.")
        return {}

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".json") and filename.startswith("CyberMetric_"):
                parts = dirpath.split(os.sep)
                if len(parts) < 3: continue
                
                model_family, model_params = parts[-2], parts[-1]
                model_name = f"{model_family}:{model_params}"

                num_questions_match = re.search(r'CyberMetric_(\d+)_', filename)
                if not num_questions_match: continue
                question_set = f"{num_questions_match.group(1)}_questions"

                file_type = ""
                if "_modified" in filename.lower():
                    file_type = "TwoStep_Modified" if "_twostep" in filename.lower() else "Standard_Modified"
                else:
                    file_type = "TwoStep_Original" if "_twostep" in filename.lower() else "Standard_Original"
                
                mapped_results[model_name][question_set][file_type] = os.path.join(dirpath, filename)
                
    return mapped_results

def process_data_for_dashboard(mapped_results: dict) -> tuple:
    """Processes all data to create the specific DataFrames for the new dashboard layout."""
    
    # Lists to hold rows for each of the 4 main tables
    std_orig_rows, std_mod_rows, ts_orig_rows, ts_mod_rows = [], [], [], []
    raw_data_rows, summary_rows = [], [] # For the other sheets

    for model_name, question_sets in sorted(mapped_results.items()):
        for question_set, files in sorted(question_sets.items()):
            
            data = {}
            for file_type, path in files.items():
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        data[file_type] = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    data[file_type] = None

            # Get baseline accuracy (Standard Original)
            summary_std_orig = data.get("Standard_Original", {}).get("summary", {})
            baseline_acc = float(summary_std_orig.get("accuracy", "0%").replace('%', ''))

            # --- Process each of the 4 test types ---
            
            # 1. Standard Original
            std_orig_rows.append({"Model": model_name, "Question Set": "Original", "Correct": baseline_acc})

            # 2. Standard Modified
            summary_std_mod = data.get("Standard_Modified", {}).get("summary", {})
            if summary_std_mod:
                acc_std_mod = float(summary_std_mod.get("accuracy", "0%").replace('%', ''))
                var_std_mod = baseline_acc - acc_std_mod
                
                # Calculate "E" chosen percentage
                details = data.get("Standard_Modified", {}).get("details", {}).get(model_name, {})
                e_count = sum(1 for q in details.values() if q.get("extracted_answer") == "E")
                e_perc = (e_count / len(details) * 100) if details else 0
                std_mod_rows.append({"Model": model_name, "Question Set": "Modified", "Correct": acc_std_mod, "Var": var_std_mod, "E_Chosen_%": e_perc})

            # 3. Two-Step Original
            summary_ts_orig = data.get("TwoStep_Original", {}).get("summary", {})
            if summary_ts_orig:
                acc_ts_orig = float(summary_ts_orig.get("option_mapping_accuracy", "0%").replace('%', ''))
                var_ts_orig = baseline_acc - acc_ts_orig
                ts_orig_rows.append({"Model": model_name, "Question Set": "Original_two", "Correct": acc_ts_orig, "Var": var_ts_orig})

            # 4. Two-Step Modified
            summary_ts_mod = data.get("TwoStep_Modified", {}).get("summary", {})
            if summary_ts_mod:
                acc_ts_mod = float(summary_ts_mod.get("option_mapping_accuracy", "0%").replace('%', ''))
                var_ts_mod = baseline_acc - acc_ts_mod

                details = data.get("TwoStep_Modified", {}).get("details", {}).get(model_name, {})
                e_count = sum(1 for q in details.values() if q.get("step2_selected_option") == "E")
                e_perc = (e_count / len(details) * 100) if details else 0
                ts_mod_rows.append({"Model": model_name, "Question Set": "Modified_two", "Correct": acc_ts_mod, "Var": var_ts_mod, "E_Chosen_%": e_perc})

            # --- Populate Raw Data and Summary (for other sheets) ---
            # (This logic can be added here if needed, similar to the previous script)

    return (
        pd.DataFrame(std_orig_rows), pd.DataFrame(std_mod_rows),
        pd.DataFrame(ts_orig_rows), pd.DataFrame(ts_mod_rows)
    )


def create_excel_report(dfs: tuple):
    """Writes the DataFrames to a styled Excel file with the new dashboard layout."""
    df_std_orig, df_std_mod, df_ts_orig, df_ts_mod = dfs
    
    with pd.ExcelWriter(OUTPUT_EXCEL_FILE, engine='openpyxl') as writer:
        
        # --- Sheet 1: Comparative Dashboard ---
        ws = writer.book.create_sheet("Comparative_Dashboard", 0)
        writer.sheets["Comparative_Dashboard"] = ws

        # --- Define layout positions ---
        pos = {
            "std_orig": {"start_row": 1, "start_col": 1, "df": df_std_orig},
            "std_mod":  {"start_row": 1, "start_col": 7, "df": df_std_mod},
            "ts_orig":  {"start_row": len(df_std_orig) + 4, "start_col": 1, "df": df_ts_orig},
            "ts_mod":   {"start_row": len(df_std_orig) + 4, "start_col": 7, "df": df_ts_mod}
        }
        
        from openpyxl.formatting.rule import ColorScaleRule
        # Green-Yellow-Red scale: Good (negative var) -> Neutral -> Bad (positive var)
        var_color_scale = ColorScaleRule(start_type='num', start_value=-10, start_color='63BE7B',
                                         mid_type='num', mid_value=0, mid_color='FFFFFF',
                                         end_type='num', end_value=15, end_color='F8696B')

        for name, p in pos.items():
            df = p['df']
            if df.empty: continue
            
            # Write main table
            df.to_excel(writer, sheet_name="Comparative_Dashboard", 
                        startrow=p['start_row'], startcol=p['start_col']-1, index=False)
            
            # Apply conditional formatting to 'Var' column if it exists
            if 'Var' in df.columns:
                var_col_letter = chr(ord('A') + p['start_col'] + df.columns.get_loc('Var') - 1)
                cell_range = f"{var_col_letter}{p['start_row']+2}:{var_col_letter}{p['start_row']+len(df)+1}"
                ws.conditional_formatting.add(cell_range, var_color_scale)

            # Write ranking tables
            df_sorted = df.sort_values(by="Correct", ascending=False).reset_index(drop=True)
            split_point = (len(df_sorted) + 1) // 2
            df_rank1 = df_sorted.iloc[:split_point][['Model', 'Correct']]
            df_rank2 = df_sorted.iloc[split_point:].reset_index(drop=True)[['Model', 'Correct']]

            rank_col_start = p['start_col'] + len(df.columns) + 1
            df_rank1.to_excel(writer, sheet_name="Comparative_Dashboard", 
                              startrow=p['start_row'], startcol=rank_col_start-1, index=False)
            df_rank2.to_excel(writer, sheet_name="Comparative_Dashboard", 
                              startrow=p['start_row'], startcol=rank_col_start+2-1, index=False)
        
        # Set column widths for better readability
        for col_letter in ['A', 'B', 'C', 'D', 'E', 'G', 'H', 'I', 'J', 'K', 'M', 'N', 'O', 'P']:
             ws.column_dimensions[col_letter].width = 15
        
        # Note: Deep Dive and Summary sheets can be added here if full raw data is needed.
        # This implementation focuses on creating the requested dashboard.

    print(f"\nAnalysis complete. New dashboard saved to '{OUTPUT_EXCEL_FILE}'")


if __name__ == "__main__":
    print("Starting analysis of CyberMetric results...")
    mapped_files = find_and_map_results(RESULTS_ROOT_DIR)
    
    if not mapped_files:
        print("No result files found to analyze.")
    else:
        print(f"Found results for {len(mapped_files)} models. Processing...")
        all_dfs = process_data_for_dashboard(mapped_files)
        create_excel_report(all_dfs)