#!/usr/bin/env python3
"""Cost model: monthly cost = (CPU requested x $/vCPU-h + memory requested x $/GiB-h) x 730 h.
Rates default to AWS Fargate-style on-demand prices - CHECK current prices and edit if needed.
Example:  python3 tools/cost_calc.py
"""
import argparse

H = 730
p = argparse.ArgumentParser()
p.add_argument("--cpu-rate", type=float, default=0.04048, help="$ per vCPU-hour")
p.add_argument("--mem-rate", type=float, default=0.004445, help="$ per GiB-hour")
p.add_argument("--after-avg-replicas", type=float, default=2.0,
               help="average web replicas over a month with HPA (measure it!)")
a = p.parse_args()

def monthly(pods, cpu, mem_gib):
    return pods * (cpu * a.cpu_rate + mem_gib * a.mem_rate) * H

# (pods, cpu cores, memory GiB) taken from the manifests' *requests*
before = monthly(6, 0.5, 0.5) + monthly(1, 0.5, 0.5)     # 6 web + 1 redis, over-sized
after = monthly(a.after_avg_replicas, 0.1, 0.0625) + monthly(1, 0.05, 0.03125)
print(f"BEFORE: ${before:8.2f} / month")
print(f"AFTER : ${after:8.2f} / month  (avg {a.after_avg_replicas} web replicas)")
print(f"SAVING: ${before-after:8.2f} / month  ({(before-after)/before*100:.1f} %)")
