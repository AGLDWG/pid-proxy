from pathlib import Path
import csv


CONF_DIR = Path(__file__).parent.parent.joinpath("conf")

pid_counts = []

for f in CONF_DIR.glob("**/*.conf"):
    c = 0
    for l in f.read_text().splitlines():
        if l.startswith("# https://linked.data.gov.au/"):
            c += 1
    pid_counts.append((f.name, c))

pid_counts_sorted = sorted(pid_counts, key=lambda tup: tup[0])

with open("pids_count.csv", "w") as csvfile:
    w = csv.writer(csvfile)

    total = 0
    for x in pid_counts_sorted:
        total += x[1]
        w.writerow(x)
    w.writerow(["Total", total])

