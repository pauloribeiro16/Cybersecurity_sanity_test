const fs = require('fs');
const path = require('path');

const SPLIT_DIR = path.join(__dirname, '../Web_Views/datasets_split');
const README_FILE = path.join(__dirname, '../README.md');

if (!fs.existsSync(SPLIT_DIR)) {
    console.error("Directory not found: " + SPLIT_DIR);
    process.exit(1);
}

const files = fs.readdirSync(SPLIT_DIR).filter(f => f.endsWith('.json'));

let markdownTables = "\n\n## 📊 All Benchmark Datasets (Cleaned)\n\n";

// Group files by prefix to organize headings
const categories = {
    "standard": "🥇 Standard Mode",
    "twostep": "🥈 Two-Step Mode",
    "probabilistic": "🎲 Probabilistic Mode"
};

for (const [prefix, title] of Object.entries(categories)) {
    markdownTables += `### ${title}\n\n`;
    
    // Find files matching this prefix
    const catFiles = files.filter(f => f.startsWith(prefix)).sort((a,b) => {
        // sort by size number e.g. 80, 500, 2000, 10000
        const sizeA = parseInt(a.match(/_(\d+)\.json/)[1]);
        const sizeB = parseInt(b.match(/_(\d+)\.json/)[1]);
        return sizeA - sizeB;
    });

    catFiles.forEach(file => {
        const filePath = path.join(SPLIT_DIR, file);
        const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
        const sizeLabel = file.match(/_(\d+)\.json/)[1];

        markdownTables += `#### 📦 Size ${sizeLabel} (${data.length} items)\n\n`;
        markdownTables += `| Model Family | Size | Mode | Accuracy |\n`;
        markdownTables += `| :--- | :--- | :--- | :--- |\n`;

        // Sort data by accuracy DESC
        data.sort((a,b) => b.accuracy - a.accuracy);

        data.forEach(d => {
            markdownTables += `| ${d.family} | ${d.size} | ${d.mode} | **${d.accuracy.toFixed(1)}%** |\n`;
        });

        markdownTables += "\n";
    });
}

// Append to README.md
let readmeContent = fs.readFileSync(README_FILE, 'utf-8');

// Remove any existing benchmark tables if script re-run (safety)
if (readmeContent.includes("## 📊 All Benchmark Datasets")) {
    readmeContent = readmeContent.split("## 📊 All Benchmark Datasets")[0];
}

fs.writeFileSync(README_FILE, readmeContent.trim() + markdownTables);
console.log("Appended tables to README.md successfully.");
