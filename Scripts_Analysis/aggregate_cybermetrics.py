import os
import json
import pandas as pd
import re

RESULTS_DIR = "ResultsCyberMetrics"
OUTPUT_MD = "Results_Summary_Dashboard.md"
OUTPUT_CSV = "Results_Summary_Data.csv"

def parse_filename_info(filename):
    """
    Extracts info from filename like CyberMetric_80_Results_Modified_Probabilistic.json
    Returns (num_questions, is_modified, test_mode)
    """
    # Defaults
    is_modified = "No"
    test_mode = "Standard"
    
    if "_Modified" in filename or "_modified" in filename:
        is_modified = "Yes"
        
    if "_TwoStep" in filename:
        test_mode = "Two-Step"
    elif "_Probabilistic" in filename:
        test_mode = "Probabilistic"
        
    # Extract number of questions
    match = re.search(r'CyberMetric_(\d+)', filename)
    num_questions = match.group(1) if match else "Unknown"
    
    return num_questions, is_modified, test_mode

def aggregate_results():
    data = []
    
    if not os.path.exists(RESULTS_DIR):
        print(f"Directory {RESULTS_DIR} not found.")
        return
        
    for root, dirs, files in os.walk(RESULTS_DIR):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                
                # Split path to get model family and params
                # Expected: ResultsCyberMetrics/family/params/file.json
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
                    
                    # Extract Accuracy
                    accuracy = "N/A"
                    if "accuracy" in summary: # Standard/Two-Step
                        accuracy = summary["accuracy"].replace('%', '')
                    elif "accuracy_top_choice_percent" in summary: # Probabilistic
                        accuracy = summary["accuracy_top_choice_percent"]
                    elif "option_mapping_accuracy" in summary: # Some Two-Step variants might use this
                        accuracy = summary["option_mapping_accuracy"].replace('%', '')
                        
                    # Extract Time
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

    return pd.DataFrame(data)

def generate_markdown_report(df):
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write("# Cybersecurity Knowledge Tester - Results Dashboard\n\n")
        f.write(f"Generated on: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}\n\n")
        
        # --- VIEW 1: Standard Scaling Benchmark ---
        f.write("## 📌 View 1: Standard Scaling Benchmark\n")
        f.write("This view compares models across standard dataset sizes (80, 500, 2000, 10000) WITHOUT modifications.\n\n")
        
        standard_df = df[(df['Modified'] == 'No') & (df['Mode'] == 'Standard')]
        if not standard_df.empty:
            pivot_std = standard_df.pivot_table(
                index="Model Name", 
                columns="Dataset", 
                values="Accuracy (%)", 
                aggfunc='mean'
            ).reset_index()
            
            # Sort full model names logically if possible, or just alphabetically
            pivot_std = pivot_std.sort_values(by="Model Name")
            
            f.write(pivot_std.to_markdown(index=False))
            f.write("\n\n")
        else:
            f.write("*No data rows found matching Standard Benchmarks.*\n\n")
            
        # --- VIEW 2: 80 Questions Variation Benchmark ---
        f.write("## 📌 View 2: 80-Question Variation Benchmark\n")
        f.write("This view compares the performance on the 80 question dataset across all test modes and modifications.\n\n")
        
        var_80_df = df[df['Questions'] == 80]
        if not var_80_df.empty:
            pivot_var = var_80_df.pivot_table(
                index="Model Name",
                columns=["Modified", "Mode"],
                values="Accuracy (%)",
                aggfunc='mean'
            ).reset_index()
            
            # Flatten multi-index columns for nicer rendering
            if isinstance(pivot_var.columns, pd.MultiIndex):
                columns = [col[0] if not col[1] else f"{col[1]} (Mod: {col[0]})" for col in pivot_var.columns]
                pivot_var.columns = columns
                
            f.write(pivot_var.to_markdown(index=False))
            f.write("\n\n")
        else:
            f.write("*No data rows found matching 80-question tests.*\n\n")
            
        # --- GENERAL LEADERBOARD ---
        f.write("## 🏆 Overall Top Performers (by Accuracy)\n")
        leaderboard = df.sort_values(by="Accuracy (%)", ascending=False).head(10)
        f.write(leaderboard[["Model Name", "Dataset", "Mode", "Accuracy (%)", "Total Time (s)"]].to_markdown(index=False))
        f.write("\n")

def main():
    print("Aggregating results across all models...")
    df = aggregate_results()
    
    if df.empty:
        print("No results found to aggregate.")
        return
        
    print(f"Found {len(df)} result entries.")
    
    # Save to CSV
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved consolidated data to {OUTPUT_CSV}")
    
    # Generate MD Report
    generate_markdown_report(df)
    print(f"Generated dashboard report at {OUTPUT_MD}")

if __name__ == "__main__":
    main()
