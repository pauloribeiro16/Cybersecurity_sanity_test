const fs = require('fs');
const path = require('path');

const PRELOADED_FILE = path.join(__dirname, '../Web_Views/preloaded_data.js');
const OUTPUT_DIR = __dirname;

const fileContent = fs.readFileSync(PRELOADED_FILE, 'utf-8');
const arrayStr = fileContent.replace('const PRELOADED_DATA = ', '').replace(/;$/, '');
const data = JSON.parse(arrayStr);

function buildBatches(rowsData, prefix) {
    let chunks = [];
    let currentChunk = [];
    let batchSize = 100;

    rowsData.forEach(d => {
        currentChunk.push({
            "type": "table_row",
            "table_row": {
                "cells": [
                    [{ "type": "text", "text": { "content": d.family } }],
                    [{ "type": "text", "text": { "content": String(d.size) } }],
                    [{ "type": "text", "text": { "content": d.mode } }],
                    [{ "type": "text", "text": { "content": `${d.accuracy.toFixed(1)}%` } }]
                ]
            }
        });

        if (currentChunk.length >= batchSize) {
            chunks.push(currentChunk);
            currentChunk = [];
        }
    });
    if (currentChunk.length > 0) chunks.push(currentChunk);

    fs.writeFileSync(path.join(OUTPUT_DIR, `${prefix}_batches.json`), JSON.stringify(chunks, null, 2));
    console.log(`Saved ${prefix}_batches.json with ${chunks.length} batches.`);
}

const standard = data.filter(d => d.mode === 'Standard').sort((a,b) => b.accuracy - a.accuracy);
const twostep = data.filter(d => d.mode === 'Two-Step').sort((a,b) => b.accuracy - a.accuracy);
const prob = data.filter(d => d.mode === 'Probabilistic').sort((a,b) => b.accuracy - a.accuracy);

buildBatches(standard, "standard");
buildBatches(twostep, "twostep");
buildBatches(prob, "probabilistic");
