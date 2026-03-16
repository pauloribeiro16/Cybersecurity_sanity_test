const fs = require('fs');
const path = require('path');

const OUTPUT_FILE = path.join(__dirname, '../Web_Views/preloaded_data.js');

let loadedData = [];

function parseAndPush(json, fullPath, filename) {
    const firstKey = Object.keys(json)[0];
    let isFormatB = false;
    if (firstKey && typeof json[firstKey] === 'object' && !json.summary) {
        const innerValues = Object.values(json[firstKey]);
        isFormatB = innerValues.some(v => v && typeof v === 'object' && !Array.isArray(v) && (v.evaluation || v.prompt));
    }

    if (isFormatB) {
        Object.keys(json).forEach(modelKey => {
            const modelData = json[modelKey];
            if (typeof modelData !== 'object' || Array.isArray(modelData)) return;

            const questionKeys = Object.keys(modelData);
            const isValid = questionKeys.some(k => modelData[k] && typeof modelData[k] === 'object' && (modelData[k].evaluation || modelData[k].prompt));
            if (!isValid) return;

            const total = questionKeys.length;
            if (total === 0 || total === 7) return; // Skip empty or CM-7

            let correct = 0;
            questionKeys.forEach(qKey => {
                const q = modelData[qKey];
                if (q && (q.evaluation === "Correct" || q.evaluation === "correct")) correct++;
            });

            const accuracy = (correct / total) * 100;
            let modelFamily = modelKey;
            let modelParams = "Unknown";
            if (modelKey.includes(':')) {
                const pts = modelKey.split(':');
                modelFamily = pts[0];
                modelParams = pts[1];
            }

            let mode = "Standard";
            if (fullPath.includes('TwoStep') || fullPath.includes('Two-Step')) mode = "Two-Step";
            else if (fullPath.includes('Probabilistic')) mode = "Probabilistic";

            loadedData.push({
                family: modelFamily,
                params: modelParams,
                dataset: `CM-${total}`,
                size: total,
                mode: mode,
                modified: fullPath.toLowerCase().includes('modified') ? "Yes" : "No",
                accuracy: accuracy,
                time: 0 
            });
        });
    } else {
        let modelFamily = "Unknown";
        let modelParams = "Unknown";
        
        if (fullPath) {
            const parts = fullPath.split(path.sep);
            const revParts = [...parts].reverse();
            if (revParts.length > 2) {
                modelParams = revParts[1]; // Index 0: filename, 1: params, 2: family
                modelFamily = revParts[2] || "Unknown";
            }
        }

        let isModified = filename.includes('_Modified') || filename.includes('_modified') ? "Yes" : "No";
        let mode = "Standard";
        if (filename.includes('_TwoStep')) mode = "Two-Step";
        else if (filename.includes('_Probabilistic')) mode = "Probabilistic";

        let accuracy = 0;
        let totalQuestions = 0;
        let correctCount = 0;

        const summary = json.summary;
        if (summary) {
            if (summary.accuracy) accuracy = parseFloat(summary.accuracy.toString().replace('%', ''));
            else if (summary.accuracy_top_choice_percent) accuracy = parseFloat(summary.accuracy_top_choice_percent.toString());
            else if (summary.option_mapping_accuracy) accuracy = parseFloat(summary.option_mapping_accuracy.toString().replace('%', ''));
        } else {
            let searchObj = json;
            if (json.details) {
                const insideDetails = Object.values(json.details)[0];
                if (insideDetails && typeof insideDetails === 'object') searchObj = insideDetails;
            }
            
            Object.keys(searchObj).forEach(qKey => {
                const q = searchObj[qKey];
                if (q && typeof q === 'object' && !Array.isArray(q) && (q.evaluation || q.prompt || q.is_highest_prob_correct !== undefined || q.is_option_correct !== undefined)) {
                    totalQuestions++;
                    const ev = q.evaluation || q.manual_overall_evaluation;
                    if (ev === "Correct" || ev === "correct") correctCount++;
                    else if (q.is_highest_prob_correct === true || q.is_option_correct === true) correctCount++;
                }
            });
            if (totalQuestions > 0) accuracy = (correctCount / totalQuestions) * 100;
        }

        const sizeMatch = filename.match(/CyberMetric_(\d+)/);
        let numQuestions = sizeMatch ? sizeMatch[1] : "Unknown";
        let sizeVal = parseInt(numQuestions) || 0;
        if (sizeVal === 0 && totalQuestions > 0) {
            sizeVal = totalQuestions;
            numQuestions = totalQuestions.toString();
        }

        if (sizeVal === 7) return; // Skip CM-7

        let time = summary && summary.total_time_seconds ? parseFloat(summary.total_time_seconds) : 0;

        loadedData.push({
            family: modelFamily,
            params: modelParams,
            dataset: `CM-${numQuestions}`,
            size: sizeVal,
            mode: mode,
            modified: isModified,
            accuracy: accuracy,
            time: time
        });
    }
}

function traverseDir(dir) {
    if (!fs.existsSync(dir)) return;
    const items = fs.readdirSync(dir);
    items.forEach(item => {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
            traverseDir(fullPath);
        } else if (item.endsWith('.json')) {
            try {
                const content = fs.readFileSync(fullPath, 'utf-8');
                const json = JSON.parse(content);
                const relPath = path.relative(path.join(__dirname, '..'), fullPath);
                parseAndPush(json, relPath, item);
            } catch (e) {}
        }
    });
}

// Clear loaded data from any previous runs just in case
loadedData = [];

// Traverse Target directory
traverseDir(path.join(__dirname, '../ResultsCyberMetrics'));

// Traverse workspace depth dirs as well
const WORKSPACE_DIRS = ['Testes_With_Context', 'Testes_With_Partial_Context', 'Testes_Without_Context'];
WORKSPACE_DIRS.forEach(wdir => {
    traverseDir(path.join(__dirname, '..', wdir));
});

console.log(`Aggregated ${loadedData.length} entries.`);

// Write file
const outputText = `const PRELOADED_DATA = ${JSON.stringify(loadedData, null, 2)};`;
fs.writeFileSync(OUTPUT_FILE, outputText);
console.log(`Saved loaded datasets to ${OUTPUT_FILE}`);
