#look at the ./outputs/dp-experiments/1 folder, and inside, for each subfolder from 0 to 49, print the metrics and stdout files
import os
import json
import re
from pathlib import Path
from collections import defaultdict

def extract_total_time_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            if line == "[wall_micros]":
                if i + 2 < len(lines):
                    total_time = int(lines[i+1].split('=')[1].strip()) + int(lines[i+2].split('=')[1].strip()) / 1_000_000_000
                    i+=2
                    break
            i+=1

    return total_time

def extract_file_name_from_stderr(stderr_path):
    with open(stderr_path, 'r') as f:
        lines = f.readlines()
        if len(lines) >= 2 and lines[1].startswith("+ file="):
            return lines[1].strip().split('=')[1]
    return "unknown_file"

def parse_stdout(stdout_path):
    """
    Reads a stdout file with lines like:
      %---------------%
      n = 11
      initial_edges = 46
      objective = 47
      ----------
      ==========
    and returns (n, initial_edges, objective).
    """
    n = initial_edges = objective = None
    with open(stdout_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("n ="):
                n = int(line.split('=')[1])
            elif line.startswith("initial_edges ="):
                initial_edges = int(line.split('=')[1])
            elif line.startswith("objective ="):
                objective = int(line.split('=')[1])
    return n, initial_edges, objective

def process_experiment_folder(folder_path, flag):
    metrics_file = folder_path / 'metrics'
    stdout_file = folder_path / 'stdout'
    stderr_file = folder_path / 'stderr'

    file_name = extract_file_name_from_stderr(stderr_file) if stderr_file.exists() else "unknown_file"


    if stdout_file.exists():
        with open(stdout_file, 'r') as f:
            lines = f.readlines()
            if flag == "dp" and lines[1].startswith("No valid path"):
                return -1, file_name, None, None
            elif flag == "cp" and ("UNSATISFIABLE" in lines[0] or "UNKNOWN" in lines[0]):
                return -1, file_name, None, None

            n, initial_edges, objective = parse_stdout(stdout_file)
            if n is None or initial_edges is None or objective is None:
                # malformed stdout?
                return None, file_name, None, None

            delta_edges = objective - initial_edges
    else:
        return None, file_name, None, None
    time = extract_total_time_from_file(metrics_file) if metrics_file.exists() else None
    return time, file_name, n, delta_edges

    # if metrics_file.exists():
    #     time = extract_total_time_from_file(metrics_file)
    #     return time, file_name


def main():
    base_dp_path = Path('../gourd/experiments/3/0')
    results = []

    for exp_dir in base_dp_path.iterdir():
        if not exp_dir.is_dir():
            continue
        time, file_name, n, delta = process_experiment_folder(exp_dir, "cp")
        results.append((file_name, n, delta))

    # print only file_name, n, and delta
    for file_name, n, delta in results:
        print(f"({file_name}, {n}, {delta})")

if __name__ == "__main__":
    main()