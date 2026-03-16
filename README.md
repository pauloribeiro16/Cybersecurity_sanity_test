# 🛡️ Cybersecurity Knowledge Tester (CyberMetric Edition)

Benchmark analysis and visualizer suite to evaluate Large Language Models (LLMs) on descriptive cybersecurity scaling datasets over isolated reasoning modes.

---

## 🎯 Aim of the Project
The core objective is to evaluate AI models on cybersecurity benchmarks (such as **CyberMetric**) using diverse evaluation methodologies to trace direct accuracy, logic validation, and reliability thresholds:
*   **Standard Mode**: Direct multiple-choice benchmarks (`Answer: [Letter]`).
*   **Two-Step Reasoning**: Generates free-text deduction before matching multiple-choice answers for deeper audit tracing.
*   **Probabilistic**: Model outputs weighted confidence distributions that must total index $100\%$.

---

## ⚙️ Configuration Setup
*   **Inference Engine**: [Ollama](http://localhost:11434)
*   **Timeout Boundaries**: `700 seconds` request cap
*   **Keep-Alive Target**: `5m` duration
*   **Source Folder Guidelines**: `Json_CyberMetrics/`
*   **Output Aggregates Pathing**: `ResultsCyberMetrics/`

---

## 📁 Workspace & Data Structure

### 📜 Analysis Scripts (`Scripts_Analysis/`)
*   `aggregate_to_js.js`: Traverses all results and packages aggregates instantly into `Web_Views/preloaded_data.js` (filters noise data like `CM-7`).
*   `split_standard.js`: Dynamically segments full scaling buckets by absolute sizes range sets thresholds.

### 🖼️ Frontend Visualizer (`Web_Views/`)
*   `dashboard.html`: Fully modular Multi-page layout dashboard covering isolated summaries with stacked dynamic charts updates.
*   `preloaded_data.js`: Core static injection containing sanitized scalable arrays variables.
*   `datasets_split/`: Segmented static outputs partitioned by question limits sizing:
    *   `standard_80.json`, `standard_500.json`, `standard_2000.json`, `standard_10000.json`
    *   `twostep_80.json`, `twostep_500.json`, `twostep_2000.json`, `twostep_10000.json`
    *   `probabilistic_80.json`

---

## 🚀 Enhancements Rolled Out (History)
1.  **Modern Dashboards UI**: Migrated layout into Sidebar views with Enlarged graphic layout outputs (min 650px cards).
2.  **Instant Preloads Variables Injection**: Extinguished heavy browser layout processing overlays through aggregated self-loads dependencies streams.
3.  **Filtered Scale Validation Rules**: Sanitized placeholder duplicate coefficients outputs indices (`CM-7` rules).
4.  **Sub-page Workspace Management**: Directly populated corresponding dashboards representations to high-impact external clients structures securely based rules.

## 📊 Benchmark Datasets (Cleaned)

### 🏆 Overall Summary (Standard Mode)

| Model | 80Q | 500Q | 2000Q | 10000Q |
| :--- | :--- | :--- | :--- | :--- |
| gpt-oss (20b) | **97.5%** | **91.0%** | **90.3%** | **86.7%** |
| glm-4.7-flash (latest) | **96.3%** | **93.8%** | **90.5%** | - |
| ministral-3 (latest) | **95.0%** | **88.8%** | - | **84.7%** |
| NVIDIA-Orchestrator-Cybersecurity-8B-Merged-GGUF (Q8_0) | **93.8%** | - | - | - |
| phi4 (14b) | **93.8%** | **91.8%** | **90.8%** | **87.0%** |
| granite4 (latest) | **92.5%** | **85.0%** | **82.2%** | - |
| qwen3 (8b) | **92.5%** | **90.0%** | **88.3%** | - |
| granite4 (tiny-h) | **91.3%** | **83.4%** | **80.6%** | **76.3%** |
| qwen3 (14b) | **90.0%** | **91.4%** | **90.1%** | - |
| rnj-1 (latest) | **90.0%** | - | - | - |
| qwen3 (1.7b) | **88.8%** | **82.2%** | **80.2%** | **78.0%** |
| gemma3n (e4b) | **86.3%** | **81.8%** | **81.6%** | **78.8%** |
| granite3.2 (8b) | **86.3%** | **86.0%** | **84.5%** | **81.1%** |
| gemma3n (e2b) | **83.8%** | **79.4%** | **78.5%** | **76.4%** |
| gemma3 (4b) | **81.3%** | **75.2%** | **75.2%** | **73.7%** |
| mistral (7b) | **81.3%** | **73.4%** | **71.6%** | **69.3%** |
| deepseek-r1 (7b) | **77.5%** | **77.2%** | **76.2%** | **73.7%** |
| granite3.3 (8b) | **75.0%** | **66.6%** | **69.1%** | **61.9%** |
| granite3.2 (2b) | **73.8%** | **76.0%** | **75.8%** | **73.8%** |
| llama3.2 (1b) | **68.8%** | **62.4%** | **60.6%** | **59.1%** |
| qwen3 (0.6b) | **66.3%** | **55.2%** | **60.7%** | **56.6%** |
| lfm2.5-thinking (latest) | **63.8%** | **57.8%** | - | - |
| qwen3 (4b) | **63.8%** | **50.0%** | **49.5%** | - |
| deepseek-r1 (1.5b) | **53.8%** | **56.8%** | **56.4%** | **54.6%** |
| gemma3 (1b) | **51.3%** | **59.6%** | **61.1%** | **59.1%** |
| LLaDA-8B-Instruct-GGUF (Q2_K) | **1.3%** | - | - | - |
| LLaDA-8B-Instruct-GGUF (Q8_0) | **0.0%** | - | - | - |


---

### 🔬 Detailed Scaling Breakdowns

#### 🥇 Standard Mode

##### 📦 Size 80 (46 items)

| Model Family | Params | Mode | Accuracy |
| :--- | :--- | :--- | :--- |
| gpt-oss | 20b | Standard | **98.8%** |
| gpt-oss | 20b | Standard | **97.5%** |
| glm-4.7-flash | latest | Standard | **96.3%** |
| ministral-3 | latest | Standard | **95.0%** |
| qwen3 | 14b | Standard | **95.0%** |
| qwen3 | 4b | Standard | **95.0%** |
| qwen3 | 8b | Standard | **95.0%** |
| NVIDIA-Orchestrator-Cybersecurity-8B-Merged-GGUF | Q8_0 | Standard | **93.8%** |
| phi4 | 14b | Standard | **93.8%** |
| granite4 | latest | Standard | **92.5%** |
| qwen3 | 8b | Standard | **92.5%** |
| granite4 | tiny-h | Standard | **91.3%** |
| qwen3 | 14b | Standard | **90.0%** |
| rnj-1 | latest | Standard | **90.0%** |
| qwen3 | 1.7b | Standard | **88.8%** |
| gemma3n | e2b | Standard | **86.3%** |
| gemma3n | e4b | Standard | **86.3%** |
| gemma3n | e4b | Standard | **86.3%** |
| granite3.2 | 8b | Standard | **86.3%** |
| granite3.2 | 8b | Standard | **86.3%** |
| deepseek-r1 | 7b | Standard | **83.8%** |
| gemma3n | e2b | Standard | **83.8%** |
| gemma3 | 4b | Standard | **81.3%** |
| granite4 | tiny-h | Standard | **81.3%** |
| mistral | 7b | Standard | **81.3%** |
| mistral | 7b | Standard | **80.0%** |
| deepseek-r1 | 7b | Standard | **77.5%** |
| gemma3 | 4b | Standard | **75.0%** |
| granite3.3 | 8b | Standard | **75.0%** |
| granite3.3 | 8b | Standard | **73.8%** |
| granite3.2 | 2b | Standard | **73.8%** |
| llama3.2 | 1b | Standard | **68.8%** |
| qwen3 | 0.6b | Standard | **66.3%** |
| lfm2.5-thinking | latest | Standard | **63.8%** |
| qwen3 | 4b | Standard | **63.8%** |
| gemma3 | 1b | Standard | **62.5%** |
| deepseek-r1 | 1.5b | Standard | **53.8%** |
| gemma3 | 1b | Standard | **51.3%** |
| llama3.2 | 1b | Standard | **22.5%** |
| LLaDA-8B-Instruct-GGUF | Q2_K | Standard | **1.3%** |
| deepseek-r1 | 1.5b | Standard | **0.0%** |
| LLaDA-8B-Instruct-GGUF | Q8_0 | Standard | **0.0%** |
| granite3.2 | 2b | Standard | **0.0%** |
| phi4 | 14b | Standard | **0.0%** |
| qwen3 | 0.6b | Standard | **0.0%** |
| qwen3 | 1.7b | Standard | **0.0%** |

##### 📦 Size 500 (24 items)

| Model Family | Params | Mode | Accuracy |
| :--- | :--- | :--- | :--- |
| glm-4.7-flash | latest | Standard | **93.8%** |
| phi4 | 14b | Standard | **91.8%** |
| qwen3 | 14b | Standard | **91.4%** |
| gpt-oss | 20b | Standard | **91.0%** |
| qwen3 | 8b | Standard | **90.0%** |
| ministral-3 | latest | Standard | **88.8%** |
| granite3.2 | 8b | Standard | **86.0%** |
| granite4 | latest | Standard | **85.0%** |
| granite4 | tiny-h | Standard | **83.4%** |
| granite4 | tiny-h | Standard | **83.4%** |
| qwen3 | 1.7b | Standard | **82.2%** |
| gemma3n | e4b | Standard | **81.8%** |
| gemma3n | e2b | Standard | **79.4%** |
| deepseek-r1 | 7b | Standard | **77.2%** |
| granite3.2 | 2b | Standard | **76.0%** |
| gemma3 | 4b | Standard | **75.2%** |
| mistral | 7b | Standard | **73.4%** |
| granite3.3 | 8b | Standard | **66.6%** |
| llama3.2 | 1b | Standard | **62.4%** |
| gemma3 | 1b | Standard | **59.6%** |
| lfm2.5-thinking | latest | Standard | **57.8%** |
| deepseek-r1 | 1.5b | Standard | **56.8%** |
| qwen3 | 0.6b | Standard | **55.2%** |
| qwen3 | 4b | Standard | **50.0%** |

##### 📦 Size 2000 (22 items)

| Model Family | Params | Mode | Accuracy |
| :--- | :--- | :--- | :--- |
| phi4 | 14b | Standard | **90.8%** |
| glm-4.7-flash | latest | Standard | **90.5%** |
| gpt-oss | 20b | Standard | **90.3%** |
| qwen3 | 14b | Standard | **90.1%** |
| qwen3 | 8b | Standard | **88.3%** |
| granite3.2 | 8b | Standard | **84.5%** |
| granite4 | latest | Standard | **82.2%** |
| gemma3n | e4b | Standard | **81.6%** |
| granite4 | tiny-h | Standard | **80.6%** |
| qwen3 | 1.7b | Standard | **80.2%** |
| gemma3n | e2b | Standard | **78.5%** |
| granite4 | tiny-h | Standard | **78.5%** |
| deepseek-r1 | 7b | Standard | **76.2%** |
| granite3.2 | 2b | Standard | **75.8%** |
| gemma3 | 4b | Standard | **75.2%** |
| mistral | 7b | Standard | **71.6%** |
| granite3.3 | 8b | Standard | **69.1%** |
| gemma3 | 1b | Standard | **61.1%** |
| qwen3 | 0.6b | Standard | **60.7%** |
| llama3.2 | 1b | Standard | **60.6%** |
| deepseek-r1 | 1.5b | Standard | **56.4%** |
| qwen3 | 4b | Standard | **49.5%** |

##### 📦 Size 10000 (18 items)

| Model Family | Params | Mode | Accuracy |
| :--- | :--- | :--- | :--- |
| phi4 | 14b | Standard | **87.0%** |
| gpt-oss | 20b | Standard | **86.7%** |
| ministral-3 | latest | Standard | **84.7%** |
| granite3.2 | 8b | Standard | **81.1%** |
| gemma3n | e4b | Standard | **78.8%** |
| qwen3 | 1.7b | Standard | **78.0%** |
| gemma3n | e2b | Standard | **76.4%** |
| granite4 | tiny-h | Standard | **76.4%** |
| granite4 | tiny-h | Standard | **76.3%** |
| granite3.2 | 2b | Standard | **73.8%** |
| gemma3 | 4b | Standard | **73.7%** |
| deepseek-r1 | 7b | Standard | **73.7%** |
| mistral | 7b | Standard | **69.3%** |
| granite3.3 | 8b | Standard | **61.9%** |
| gemma3 | 1b | Standard | **59.1%** |
| llama3.2 | 1b | Standard | **59.1%** |
| qwen3 | 0.6b | Standard | **56.6%** |
| deepseek-r1 | 1.5b | Standard | **54.6%** |

#### 🥈 Two-Step Mode

##### 📦 Size 80 (38 items)

| Model Family | Params | Mode | Accuracy |
| :--- | :--- | :--- | :--- |
| gpt-oss | 20b | Two-Step | **92.5%** |
| phi4 | 14b | Two-Step | **92.5%** |
| gpt-oss | 20b | Two-Step | **90.0%** |
| phi4 | 14b | Two-Step | **88.8%** |
| qwen3 | 14b | Two-Step | **88.8%** |
| granite4 | tiny-h | Two-Step | **87.5%** |
| qwen3 | 8b | Two-Step | **86.3%** |
| gemma3n | e4b | Two-Step | **83.8%** |
| granite3.2 | 8b | Two-Step | **83.8%** |
| gemma3n | e4b | Two-Step | **82.5%** |
| granite3.2 | 8b | Two-Step | **82.5%** |
| granite4 | tiny-h | Two-Step | **82.5%** |
| gemma3 | 4b | Two-Step | **81.3%** |
| gemma3 | 4b | Two-Step | **81.3%** |
| mistral | 7b | Two-Step | **81.3%** |
| qwen3 | 4b | Two-Step | **81.3%** |
| mistral | 7b | Two-Step | **80.0%** |
| qwen3 | 1.7b | Two-Step | **80.0%** |
| qwen3 | 8b | Two-Step | **80.0%** |
| gemma3n | e2b | Two-Step | **77.5%** |
| gemma3n | e2b | Two-Step | **75.0%** |
| qwen3 | 1.7b | Two-Step | **75.0%** |
| qwen3 | 14b | Two-Step | **75.0%** |
| granite3.2 | 2b | Two-Step | **72.5%** |
| granite3.2 | 2b | Two-Step | **71.3%** |
| deepseek-r1 | 7b | Two-Step | **70.0%** |
| granite3.3 | 8b | Two-Step | **68.8%** |
| deepseek-r1 | 7b | Two-Step | **67.5%** |
| granite3.3 | 8b | Two-Step | **61.3%** |
| qwen3 | 4b | Two-Step | **60.0%** |
| qwen3 | 0.6b | Two-Step | **57.5%** |
| qwen3 | 0.6b | Two-Step | **52.5%** |
| gemma3 | 1b | Two-Step | **51.3%** |
| deepseek-r1 | 1.5b | Two-Step | **50.0%** |
| gemma3 | 1b | Two-Step | **50.0%** |
| llama3.2 | 1b | Two-Step | **42.5%** |
| deepseek-r1 | 1.5b | Two-Step | **41.3%** |
| llama3.2 | 1b | Two-Step | **38.8%** |

##### 📦 Size 500 (2 items)

| Model Family | Params | Mode | Accuracy |
| :--- | :--- | :--- | :--- |
| granite4 | tiny-h | Two-Step | **78.8%** |
| granite4 | tiny-h | Two-Step | **76.4%** |

##### 📦 Size 2000 (2 items)

| Model Family | Params | Mode | Accuracy |
| :--- | :--- | :--- | :--- |
| granite4 | tiny-h | Two-Step | **77.2%** |
| granite4 | tiny-h | Two-Step | **72.3%** |

##### 📦 Size 10000 (2 items)

| Model Family | Params | Mode | Accuracy |
| :--- | :--- | :--- | :--- |
| granite4 | tiny-h | Two-Step | **73.8%** |
| granite4 | tiny-h | Two-Step | **68.5%** |

#### 🎲 Probabilistic Mode

##### 📦 Size 80 (36 items)

| Model Family | Params | Mode | Accuracy |
| :--- | :--- | :--- | :--- |
| gpt-oss | 20b | Probabilistic | **96.3%** |
| gpt-oss | 20b | Probabilistic | **95.0%** |
| qwen3 | 4b | Probabilistic | **92.5%** |
| qwen3 | 8b | Probabilistic | **92.5%** |
| qwen3 | 14b | Probabilistic | **90.0%** |
| qwen3 | 14b | Probabilistic | **90.0%** |
| qwen3 | 8b | Probabilistic | **90.0%** |
| phi4 | 14b | Probabilistic | **86.3%** |
| phi4 | 14b | Probabilistic | **86.3%** |
| qwen3 | 4b | Probabilistic | **86.3%** |
| granite3.3 | 8b | Probabilistic | **78.8%** |
| granite3.2 | 8b | Probabilistic | **77.5%** |
| granite3.3 | 8b | Probabilistic | **76.3%** |
| qwen3 | 1.7b | Probabilistic | **76.3%** |
| granite3.2 | 8b | Probabilistic | **75.0%** |
| gemma3n | e4b | Probabilistic | **70.0%** |
| gemma3n | e4b | Probabilistic | **67.5%** |
| gemma3 | 4b | Probabilistic | **66.3%** |
| qwen3 | 1.7b | Probabilistic | **66.3%** |
| gemma3 | 4b | Probabilistic | **63.8%** |
| gemma3n | e2b | Probabilistic | **63.8%** |
| gemma3n | e2b | Probabilistic | **63.8%** |
| deepseek-r1 | 7b | Probabilistic | **61.3%** |
| mistral | 7b | Probabilistic | **61.3%** |
| deepseek-r1 | 7b | Probabilistic | **58.8%** |
| granite3.2 | 2b | Probabilistic | **57.5%** |
| qwen3 | 0.6b | Probabilistic | **57.5%** |
| qwen3 | 0.6b | Probabilistic | **56.3%** |
| mistral | 7b | Probabilistic | **55.0%** |
| granite3.2 | 2b | Probabilistic | **51.3%** |
| llama3.2 | 1b | Probabilistic | **48.8%** |
| deepseek-r1 | 1.5b | Probabilistic | **42.5%** |
| deepseek-r1 | 1.5b | Probabilistic | **41.3%** |
| llama3.2 | 1b | Probabilistic | **40.0%** |
| gemma3 | 1b | Probabilistic | **35.0%** |
| gemma3 | 1b | Probabilistic | **33.8%** |

