const fs = require('fs');
const path = require('path');

const PRELOADED_FILE = path.join(__dirname, '../Web_Views/preloaded_data.js');
const OUTPUT_FILE = path.join(__dirname, '../notion_blocks.json');

// Read preloaded_data
const fileContent = fs.readFileSync(PRELOADED_FILE, 'utf-8');
const arrayStr = fileContent.replace('const PRELOADED_DATA = ', '').replace(/;$/, '');
const data = JSON.parse(arrayStr);

let blocks = [];

// 1. KPI Bullet Card
blocks.push({
    "object": "block",
    "type": "callout",
    "callout": {
        "rich_text": [
            { "type": "text", "text": { "content": "📊 Total Result Files Summarized: " + data.length + "\n🏆 Peak Accuracy Recorded: " + Math.max(...data.map(d=>d.accuracy)).toFixed(1) + "%" } }
        ],
        "icon": { "type": "emoji", "emoji": "📊" },
        "color": "blue_background"
    }
});

function createTableBlock(title, rowsData) {
    let header = {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "rich_text": [{ "type": "text", "text": { "content": title } }]
        }
    };
    
    let table = {
        "object": "block",
        "type": "table",
        "table": {
            "table_width": 4,
            "has_column_header": true,
            "has_row_header": false,
            "children": [
                {
                    "type": "table_row",
                    "table_row": {
                        "cells": [
                            [{ "type": "text", "text": { "content": "Model Family" } }],
                            [{ "type": "text", "text": { "content": "Size" } }],
                            [{ "type": "text", "text": { "content": "Mode" } }],
                            [{ "type": "text", "text": { "content": "Accuracy (%)" } }]
                        ]
                    }
                }
            ]
        }
    };

    // Slice top 10
    rowsData.slice(0, 10).forEach(d => {
        table.table.children.push({
            "type": "table_row",
            "table_row": {
                "cells": [
                    [{ "type": "text", "text": { "content": `${d.family}` } }],
                    [{ "type": "text", "text": { "content": String(d.size) } }],
                    [{ "type": "text", "text": { "content": d.mode } }],
                    [{ "type": "text", "text": { "content": `${d.accuracy.toFixed(1)}%` } }]
                ]
            }
        });
    });

    return [header, table];
}

const standard = data.filter(d => d.mode === 'Standard').sort((a,b) => b.accuracy - a.accuracy);
const twostep = data.filter(d => d.mode === 'Two-Step').sort((a,b) => b.accuracy - a.accuracy);
const prob = data.filter(d => d.mode === 'Probabilistic').sort((a,b) => b.accuracy - a.accuracy);

blocks.push(...createTableBlock("🥇 Standard Mode Leaderboard (Top 10)", standard));
blocks.push(...createTableBlock("🥈 Two-Step Mode Leaderboard (Top 10)", twostep));
blocks.push(...createTableBlock("🎲 Probabilistic Mode Leaderboard (Top 10)", prob));

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(blocks, null, 2));
console.log(`Saved notion_blocks.json with ${blocks.length} blocks.`);
