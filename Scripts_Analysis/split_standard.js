const fs = require('fs');
const path = require('path');

const PRELOADED_FILE = path.join(__dirname, '../Web_Views/preloaded_data.js');
const OUTPUT_DIR = path.join(__dirname, '../Web_Views/datasets_split');

// Create output directory if not exists
if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// Read preloaded data
const fileContent = fs.readFileSync(PRELOADED_FILE, 'utf-8');
const arrayStr = fileContent.replace('const PRELOADED_DATA = ', '').replace(/;$/, '');
const data = JSON.parse(arrayStr);

// Modes to process
const modes = ['Standard', 'Two-Step', 'Probabilistic'];

modes.forEach(mode => {
    // Filter by mode
    const modeData = data.filter(d => d.mode === mode);

    // Buckets
    let buckets = {
        "80": [],
        "500": [],
        "2000": [],
        "10000": []
    };

    modeData.forEach(d => {
        const size = d.size;
        if (size <= 80) {
            buckets["80"].push(d);
        } else if (size <= 500) {
            buckets["500"].push(d);
        } else if (size <= 2000) {
            buckets["2000"].push(d);
        } else {
            buckets["10000"].push(d);
        }
    });

    const prefix = mode.toLowerCase().replace('-', '');

    // Write outputs
    for (const [key, rows] of Object.entries(buckets)) {
        if (rows.length === 0) continue; // Skip empty buckets
        const filePath = path.join(OUTPUT_DIR, `${prefix}_${key}.json`);
        fs.writeFileSync(filePath, JSON.stringify(rows, null, 2));
        console.log(`Saved ${prefix}_${key}.json with ${rows.length} rows.`);
    }
});
