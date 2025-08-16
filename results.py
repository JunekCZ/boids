import matplotlib.pyplot as plt
import csv

x = []
bf = []
qt = []

with open("benchmark_results.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        x.append(int(row["num_boids"]))
        bf.append(float(row["brute_force_ms"]))
        qt.append(float(row["quadtree_ms"]))

plt.plot(x, bf, label="Brute-force", marker="o")
plt.plot(x, qt, label="QuadTree", marker="o")
plt.xlabel("Počet boidů")
plt.ylabel("Průměrný čas kroku [ms]")
plt.title("Výkon QuadTree vs Brute-force")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("comparison_plot.png")
plt.show()
