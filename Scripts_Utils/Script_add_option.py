import json
import os

def add_none_of_the_above_option(input_filepath: str):
    """
    Reads a single CyberMetric JSON file, adds 'E - None of the above' to each question,
    and saves the result to a new file.

    Args:
        input_filepath (str): The full path to the source JSON file.
    """
    # Define a safe output filename to avoid overwriting the original
    base, ext = os.path.splitext(input_filepath)
    output_filepath = f"{base}_modified.json"

    try:
        # Read the original JSON data
        with open(input_filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Verify the expected structure
        if 'questions' not in data or not isinstance(data['questions'], list):
            print("  -> Skipping: JSON file does not have the expected structure (missing 'questions' list).")
            return

        # The core logic: Iterate and modify
        questions_processed = 0
        for question in data['questions']:
            if 'answers' in question and isinstance(question['answers'], dict):
                question['answers']['E'] = "None of the above"
                questions_processed += 1
        
        # Write the modified data to the new file
        with open(output_filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        print(f"  -> Success: Processed {questions_processed} questions.")
        print(f"  -> Saved modified file to: {os.path.basename(output_filepath)}")

    except json.JSONDecodeError:
        print(f"  -> Skipping: The file is not a valid JSON file.")
    except Exception as e:
        print(f"  -> An unexpected error occurred: {e}")

# --- Main execution block ---
if __name__ == "__main__":
    # The name of the directory you want to process
    TARGET_DIRECTORY = "Json_CyberMetrics"
    
    print(f"Starting batch process for directory: '{TARGET_DIRECTORY}'\n")

    # --- 1. Check if the target directory exists ---
    if not os.path.isdir(TARGET_DIRECTORY):
        print(f"Error: Directory '{TARGET_DIRECTORY}' not found.")
        print("Please make sure this script is in the same parent folder as the 'Json_Cybermetrics' directory.")
    else:
        # --- 2. Find all .json files in the directory ---
        json_files_to_process = [
            f for f in os.listdir(TARGET_DIRECTORY) if f.endswith('.json')
        ]

        if not json_files_to_process:
            print(f"No .json files found in '{TARGET_DIRECTORY}'.")
        else:
            print(f"Found {len(json_files_to_process)} JSON file(s) to process.\n")
            
            # --- 3. Loop through each file and process it ---
            for filename in json_files_to_process:
                full_filepath = os.path.join(TARGET_DIRECTORY, filename)
                print(f"--- Processing: {filename} ---")
                add_none_of_the_above_option(full_filepath)
                print("-" * (18 + len(filename)) + "\n")
            
            print("Batch process complete.")