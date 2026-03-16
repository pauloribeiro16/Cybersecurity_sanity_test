const PRELOADED_DATA = [
  {
    "family": "deepseek-r1",
    "params": "1.5b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 54.56,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "1.5b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 56.35,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "1.5b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 56.8,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "1.5b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 0,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "1.5b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 53.75,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "1.5b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 42.5,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "1.5b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 41.25,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "1.5b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 41.25,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "1.5b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 50,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "7b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 73.67,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "7b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 76.15,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "7b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 77.2,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 83.75,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 77.5,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 58.75,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 67.5,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 61.25,
    "time": 0
  },
  {
    "family": "deepseek-r1",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 70,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "1b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 59.13,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "1b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 61.1,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "1b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 59.6,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 62.5,
    "time": 27.52
  },
  {
    "family": "gemma3",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 51.25,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 35,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 51.25,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 33.75,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 50,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "4b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 73.71,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "4b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 75.15,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "4b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 75.2,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 75,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 81.25,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 66.25,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 81.25,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 63.75,
    "time": 0
  },
  {
    "family": "gemma3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 81.25,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e2b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 76.42,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e2b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 78.5,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e2b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 79.4,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 86.25,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 83.75,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 63.75,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 75,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 63.75,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 77.5,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e4b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 78.78,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e4b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 81.6,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e4b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 81.8,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 86.25,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 86.25,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 67.5,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 82.5,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 70,
    "time": 0
  },
  {
    "family": "gemma3n",
    "params": "e4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 83.75,
    "time": 0
  },
  {
    "family": "glm-4.7-flash",
    "params": "latest",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 90.45,
    "time": 0
  },
  {
    "family": "glm-4.7-flash",
    "params": "latest",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 93.8,
    "time": 0
  },
  {
    "family": "glm-4.7-flash",
    "params": "latest",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 96.25,
    "time": 0
  },
  {
    "family": "gpt-oss",
    "params": "20b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 86.74,
    "time": 0
  },
  {
    "family": "gpt-oss",
    "params": "20b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 90.25,
    "time": 0
  },
  {
    "family": "gpt-oss",
    "params": "20b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 91,
    "time": 0
  },
  {
    "family": "gpt-oss",
    "params": "20b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 98.75,
    "time": 0
  },
  {
    "family": "gpt-oss",
    "params": "20b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 97.5,
    "time": 0
  },
  {
    "family": "gpt-oss",
    "params": "20b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 95,
    "time": 0
  },
  {
    "family": "gpt-oss",
    "params": "20b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 90,
    "time": 0
  },
  {
    "family": "gpt-oss",
    "params": "20b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 96.25,
    "time": 0
  },
  {
    "family": "gpt-oss",
    "params": "20b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 92.5,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "8b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 81.11,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "8b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 84.5,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "8b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 86,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 86.25,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 86.25,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 77.5,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 82.5,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 75,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 83.75,
    "time": 0
  },
  {
    "family": "granite3.3",
    "params": "8b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 61.91,
    "time": 0
  },
  {
    "family": "granite3.3",
    "params": "8b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 69.1,
    "time": 0
  },
  {
    "family": "granite3.3",
    "params": "8b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 66.6,
    "time": 0
  },
  {
    "family": "granite3.3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 73.75,
    "time": 0
  },
  {
    "family": "granite3.3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 75,
    "time": 0
  },
  {
    "family": "granite3.3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 76.25,
    "time": 0
  },
  {
    "family": "granite3.3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 61.25,
    "time": 0
  },
  {
    "family": "granite3.3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 78.75,
    "time": 0
  },
  {
    "family": "granite3.3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 68.75,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "latest",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 82.15,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "latest",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 85,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "latest",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 92.5,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 76.39,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 76.32,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 68.54,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 73.85,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 78.5,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 80.6,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 72.3,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 77.2,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 83.4,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 83.4,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 76.4,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 78.8,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 81.25,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 91.25,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 82.5,
    "time": 0
  },
  {
    "family": "granite4",
    "params": "tiny-h",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 87.5,
    "time": 0
  },
  {
    "family": "LLaDA-8B-Instruct-GGUF",
    "params": "Q2_K",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 1.25,
    "time": 0
  },
  {
    "family": "LLaDA-8B-Instruct-GGUF",
    "params": "Q8_0",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 0,
    "time": 0
  },
  {
    "family": "NVIDIA-Orchestrator-Cybersecurity-8B-Merged-GGUF",
    "params": "Q8_0",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 93.75,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "2b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 73.75,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "2b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 75.75,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "2b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 76,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 0,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 73.75,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 51.25,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 72.5,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 57.5,
    "time": 0
  },
  {
    "family": "granite3.2",
    "params": "2b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 71.25,
    "time": 0
  },
  {
    "family": "lfm2.5-thinking",
    "params": "latest",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 57.8,
    "time": 0
  },
  {
    "family": "lfm2.5-thinking",
    "params": "latest",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 63.75,
    "time": 0
  },
  {
    "family": "llama3.2",
    "params": "1b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 59.12,
    "time": 0
  },
  {
    "family": "llama3.2",
    "params": "1b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 60.6,
    "time": 0
  },
  {
    "family": "llama3.2",
    "params": "1b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 62.4,
    "time": 0
  },
  {
    "family": "llama3.2",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 22.5,
    "time": 0
  },
  {
    "family": "llama3.2",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 68.75,
    "time": 0
  },
  {
    "family": "llama3.2",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 48.75,
    "time": 0
  },
  {
    "family": "llama3.2",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 42.5,
    "time": 0
  },
  {
    "family": "llama3.2",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 40,
    "time": 0
  },
  {
    "family": "llama3.2",
    "params": "1b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 38.75,
    "time": 0
  },
  {
    "family": "ministral-3",
    "params": "latest",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 84.66,
    "time": 0
  },
  {
    "family": "ministral-3",
    "params": "latest",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 88.8,
    "time": 0
  },
  {
    "family": "ministral-3",
    "params": "latest",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 95,
    "time": 0
  },
  {
    "family": "mistral",
    "params": "7b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 69.34,
    "time": 0
  },
  {
    "family": "mistral",
    "params": "7b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 71.6,
    "time": 0
  },
  {
    "family": "mistral",
    "params": "7b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 73.4,
    "time": 0
  },
  {
    "family": "mistral",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 80,
    "time": 0
  },
  {
    "family": "mistral",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 81.25,
    "time": 0
  },
  {
    "family": "mistral",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 61.25,
    "time": 0
  },
  {
    "family": "mistral",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 81.25,
    "time": 0
  },
  {
    "family": "mistral",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 55,
    "time": 0
  },
  {
    "family": "mistral",
    "params": "7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 80,
    "time": 0
  },
  {
    "family": "phi4",
    "params": "14b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 86.99,
    "time": 0
  },
  {
    "family": "phi4",
    "params": "14b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 90.75,
    "time": 0
  },
  {
    "family": "phi4",
    "params": "14b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 91.8,
    "time": 0
  },
  {
    "family": "phi4",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 0,
    "time": 0
  },
  {
    "family": "phi4",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 93.75,
    "time": 0
  },
  {
    "family": "phi4",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 86.25,
    "time": 0
  },
  {
    "family": "phi4",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 88.75,
    "time": 0
  },
  {
    "family": "phi4",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 86.25,
    "time": 0
  },
  {
    "family": "phi4",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 92.5,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "0.6b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 56.57,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "0.6b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 60.7,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "0.6b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 55.2,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "0.6b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 0,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "0.6b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 66.25,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "0.6b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 57.5,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "0.6b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 57.5,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "0.6b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 56.25,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "0.6b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 52.5,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "1.7b",
    "dataset": "CM-10000",
    "size": 10000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 78,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "1.7b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 80.15,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "1.7b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 82.2,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "1.7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 0,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "1.7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 88.75,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "1.7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 66.25,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "1.7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 75,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "1.7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 76.25,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "1.7b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 80,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "14b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 90.1,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "14b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 91.4,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 95,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 90,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 90,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 75,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 90,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "14b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 88.75,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "4b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 49.5,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "4b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 50,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 95,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 63.75,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 92.5,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 60,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 86.25,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "4b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 81.25,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "8b",
    "dataset": "CM-2000",
    "size": 2000,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 88.35,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "8b",
    "dataset": "CM-500",
    "size": 500,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 90,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 95,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "Yes",
    "accuracy": 92.5,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "Yes",
    "accuracy": 90,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "Yes",
    "accuracy": 80,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Probabilistic",
    "modified": "No",
    "accuracy": 92.5,
    "time": 0
  },
  {
    "family": "qwen3",
    "params": "8b",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Two-Step",
    "modified": "No",
    "accuracy": 86.25,
    "time": 0
  },
  {
    "family": "rnj-1",
    "params": "latest",
    "dataset": "CM-80",
    "size": 80,
    "mode": "Standard",
    "modified": "No",
    "accuracy": 90,
    "time": 0
  }
];