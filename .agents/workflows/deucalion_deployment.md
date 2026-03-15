---
description: Deploying jobs to the Deucalion Supercomputer (with Email & Metrics)
---

This workflow defines a generic approach to deploying tasks onto the Deucalion supercomputer using SLURM. It places a special focus on configuring SLURM email notifications so you know when jobs begin and finish, as well as tracking system metrics (CPU, RAM, GPU, VRAM) during the run.

### 1. Configure the SLURM Job Script

Create a `job.sh` file for your deployment. You must configure the **Email Notifications** and **Metric Polling** inside this script.

**Email Directives:**
Add the `#SBATCH --mail-type` and `#SBATCH --mail-user` directives to get automated alerts on your job status.

**Metrics Tracker:**
Launch a background Bash loop to poll `nvidia-smi`, `top`, and `free` to write comprehensive system load logs.

```bash
#!/bin/bash
#SBATCH --gpus=1
#SBATCH --cpus-per-task=16
#SBATCH --tasks-per-node=1
#SBATCH -A F202512235CPCAA1G
#SBATCH -t 2-00:00:00
#SBATCH -p normal-a100-40
#SBATCH -N 1
#SBATCH --out=output/%j.txt

# --- EMAIL NOTIFICATONS ---
# Receive emails when job begins, ends, fails, or requeues
#SBATCH --mail-type=ALL 
#SBATCH --mail-user=your.email@example.com

# --- METRIC TRACKING ---
# Start a background resource monitor for CPU, RAM, and GPU
MONITOR_LOG="output/resource_usage_${SLURM_JOB_ID}.log"
echo "--- Resource Monitor Started ---" > $MONITOR_LOG
(
  while true; do
    echo "=== $(date) ===" >> $MONITOR_LOG
    echo "[RAM Usage]" >> $MONITOR_LOG
    free -m >> $MONITOR_LOG
    echo "[CPU Usage (Top)]" >> $MONITOR_LOG
    top -b -n 1 -u $USER | head -n 12 | tail -n 6 >> $MONITOR_LOG
    echo "[GPU Usage]" >> $MONITOR_LOG
    nvidia-smi --query-gpu=utilization.gpu,utilization.memory,memory.used,memory.total,power.draw --format=csv,noheader >> $MONITOR_LOG
    echo "" >> $MONITOR_LOG
    sleep 30
  done
) &
MONITOR_PID=$!

# --- YOUR MAIN JOB EXECUTION ---
# E.g., loading Conda, starting Singularity, running Python

echo "Starting main job execution..."
# >>> RUN YOUR COMMANDS HERE <<<

# --- CLEANUP ---
# Stop the background metric metric monitor
kill $MONITOR_PID
echo "Job $SLURM_JOB_ID complete. Usage log saved to $MONITOR_LOG"
```

### 2. Implement Metrics in Python (If applicable)

If you are running a Python script, you should implement `psutil` within the script for tighter tracking of exact functions or loops (e.g., tracking the exact time a model takes to load into VRAM vs the time it takes to process tokens).

- **Upload/Load Time**: Capture the `time.time()` before and after the initial model load/upload block.
- **Run Time**: Capture the overarching start/end time of your main loops.
- **OS Resource Limits**: Import `psutil` to track exact maximums.

### 3. Deploy to Deucalion

1. Transfer your project directory to Deucalion:
```bash
rsync -avz ./my_project username@deucalion:/projects/F202512235CPCAA1/my_project/
```

2. Login to a Deucalion Login Node and schedule the job:
```bash
cd /projects/F202512235CPCAA1/my_project/
sbatch job.sh
```

### 4. Monitor & Retrieve Results

- Check job queue manually: `squeue -u $USER`
- You will receive an **Email Notification** the moment your job begins running on an A100 GPU node, and another email with the completion status when it finishes.
- Retrieve the output logs (including the custom metric tracker logs) back to your local machine:
```bash
rsync -avz username@deucalion:/projects/F202512235CPCAA1/my_project/output/ ./output/
```
