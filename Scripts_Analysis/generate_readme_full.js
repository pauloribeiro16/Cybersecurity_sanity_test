const fs = require('fs');
const path = require('path');

const SPLIT_DIR = path.join(__dirname, '../Web_Views/datasets_split');
const README_FILE = path.join(__dirname, '../README.md');

if (!fs.existsSync(SPLIT_DIR)) {
    console.error("Directory not found: " + SPLIT_DIR);
    process.exit(1);
}

const files = fs.readdirSync(SPLIT_DIR).filter(f => f.endsWith('.json'));

let markdownContent = "\n\n## 📊 Benchmark Datasets (Cleaned)\n\n";

// --- 1. GENERATE SUMMARY TABLE (STANDARD MODE) ---
markdownContent += "### 🏆 Overall Summary (Standard Mode)\n\n";
markdownContent += "| Model | 80Q | 500Q | 2000Q | 10000Q |\n";
markdownContent += "| :--- | :--- | :--- | :--- | :--- |\n";

// Map to hold: ModelName -> { "80": acc, "500": acc, "2000": acc, "10000": acc }
const summaryMap = {};

const standardSizes = ["80", "500", "2000", "10000"];

standardSizes.forEach(size => {
    const fileName = `standard_${size}.json`;
    const filePath = path.join(SPLIT_DIR, fileName);
    if (fs.existsSync(filePath)) {
        const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        data.forEach(d => {
            const modelLabel = `${d.family} (${d.params})`;
            if (!summaryMap[modelLabel]) {
                summaryMap[modelLabel] = { "80": "-", "500": "-", "2000": "-", "10000": "-" };
            }
            summaryMap[modelLabel][size] = `**${d.accuracy.toFixed(1)}%**`;
        });
    }
});

// Sort models by 80Q accuracy DESC
const sortedModels = Object.keys(summaryMap).sort((a,b) => {
    const accA = parseFloat(summaryMap[a]["80"].replace(/[^\d.]/g, '')) || 0;
    const accB = parseFloat(summaryMap[b]["80"].replace(/[^\d.]/g, '')) || 0;
    return accB - accA;
});

sortedModels.forEach(model => {
    markdownContent += `| ${model} | ${summaryMap[model]["80"]} | ${summaryMap[model]["500"]} | ${summaryMap[model]["2000"]} | ${summaryMap[model]["10000"]} |\n`;
});

markdownContent += "\n\n---\n\n### 🔬 Detailed Scaling Breakdowns\n\n";

// --- 2. GENERATE DETAILED DATSETS TABLES (Previous Logic) ---
const categories = {
    "standard": "🥇 Standard Mode",
    "twostep": "🥈 Two-Step Mode",
    "probabilistic": "🎲 Probabilistic Mode"
};

for (const [prefix, title] of Object.entries(categories)) {
    markdownContent += `#### ${title}\n\n`;
    
    const catFiles = files.filter(f => f.startsWith(prefix)).sort((a,b) => {
        const sizeA = parseInt(a.match(/_(\d+)\.json/)[1]);
        const sizeB = parseInt(b.match(/_(\d+)\.json/)[1]);
        return sizeA - sizeB;
    });

    catFiles.forEach(file => {
        const filePath = path.join(SPLIT_DIR, file);
        const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        const sizeLabel = file.match(/_(\d+)\.json/)[1];

        markdownContent += `##### 📦 Size ${sizeLabel} (${data.length} items)\n\n`;
        markdownContent += "| Model Family | Params | Mode | Accuracy |\n";
        markdownContent += "| :--- | :--- | :--- | :--- |\n";

        data.sort((a,b) => b.accuracy - a.accuracy);

        data.forEach(d => {
            markdownContent += `| ${d.family} | ${d.params} | ${d.mode} | **${d.accuracy.toFixed(1)}%** |\n`;
        });

        markdownContent += "\n";
    });
}

// Read and append
let readmeContent = fs.readFileSync(README_FILE, 'utf-8');

// Safeguard against old anchors
if (readmeContent.includes("## 📊 All Benchmark Datasets")) {
    readmeContent = readmeContent.split("## 📊 All Benchmark Datasets")[0];
}
if (readmeContent.includes("## 📊 Benchmark Datasets (Cleaned)")) {
    readmeContent = readmeContent.split("## 📊 Benchmark Datasets (Cleaned)")[0];
}

fs.writeFileSync(README_FILE, readmeContent.trim() + markdownContent);
console.log("Re-generated README.md with summary table at head.");
