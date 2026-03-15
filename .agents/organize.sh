#!/bin/bash
BASE_DIR="/home/epmq/Desktop/Projects/Cybersecurity_sanity_test"
cd $BASE_DIR

# 1. Create Directories
mkdir -p Scripts_Testing Scripts_Analysis Scripts_Utils Data_and_Logs Web_Views

# 2. Move Files
# Scripts_Testing
for f in Cybersecurity_inference_tester.py cybersecurity_sanity_tester.py cybersecurity_sanity_tester_CyberMetric.py Cybersecurity_santy_Teste_With_Context.py threat_model_tester.py api_rate_tester.py debug_aggregate.py; do
    [ -f "$f" ] && mv "$f" Scripts_Testing/
done

# Scripts_Analysis
for f in aggregate_cybermetrics.py analyze_cyber_test_results.py analyze_cyber_test_results_CyberMetrics.py analyze_cyber_test_results_CyberMetrics_Mine.py analyze_cyber_test_results_modified.py evaluate_threat_Models.py; do
    [ -f "$f" ] && mv "$f" Scripts_Analysis/
done

# Scripts_Utils
for f in Script_add_option.py api_sanity_check.py; do
    [ -f "$f" ] && mv "$f" Scripts_Utils/
done

# Data_and_Logs
for f in CyberMetrics_Analysis.xlsx Test_Summary_Report.xlsx Results.json Results_Teste_3.json ThreatModel_Tests.json uco_1_5.txt Testes; do
    [ -f "$f" ] && mv "$f" Data_and_Logs/
done

# Web_Views
[ -f "dashboard.html" ] && mv dashboard.html Web_Views/

# 3. Adjust Paths in Scripts_Testing
sed -i 's|SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))|SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))|g' Scripts_Testing/*.py

# 4. Generate summary
echo "# File Organization Summary" > moved_files_summary.txt
echo "" >> moved_files_summary.txt
echo "Files have been grouped into:" >> moved_files_summary.txt
echo "- Scripts_Testing/ (Test Runners)" >> moved_files_summary.txt
echo "- Scripts_Analysis/ (Analyzers & Aggregators)" >> moved_files_summary.txt
echo "- Scripts_Utils/ (Helpers)" >> moved_files_summary.txt
echo "- Data_and_Logs/ (Flat Data files)" >> moved_files_summary.txt
echo "- Web_Views/ (HTML Dashboards)" >> moved_files_summary.txt
echo "" >> moved_files_summary.txt
echo "Static paths in Scripts_Testing/ have been adjusted for parent directory access." >> moved_files_summary.txt
