import os
import random
import subprocess
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ==============================
# Configuration
# ==============================

# Total number of operations per test
Q = 1_000_000
# Key range for random sampling
KEY_MIN, KEY_MAX = -1_000_000_000, 1_000_000_000

# Directory to store generated tests
TEST_DIR = "tests"
os.makedirs(TEST_DIR, exist_ok=True)

# C++ binaries to benchmark
BINARIES = {
    "Treap": "./treap",
    "Splay": "./splay"
}

# ==============================
# Test Generators
# ==============================

def write_test(filename, ops):
    """Write ABCE-format test to filename."""
    with open(filename, "w") as f:
        f.write(f"{len(ops)}\n")
        for op in ops:
            if op[0] == 6:
                f.write(f"6 {op[1]} {op[2]}\n")
            else:
                f.write(f"{op[0]} {op[1]}\n")

def generate_simple_patterns():
    """Generate ascending, descending, and random insert+search patterns."""
    base = TEST_DIR + os.sep
    # 1. Ascending
    ops = []
    for x in range(1, Q+1):
        ops.append((1, x))
        ops.append((3, x))
    write_test(base + "simple_ascending.in", ops)

    # 2. Descending
    ops = []
    for x in range(Q, 0, -1):
        ops.append((1, x))
        ops.append((3, x))
    write_test(base + "simple_descending.in", ops)

    # 3. Random
    seq = list(range(1, Q+1))
    random.shuffle(seq)
    ops = []
    for x in seq:
        ops.append((1, x))
        ops.append((3, x))
    write_test(base + "simple_random.in", ops)

def generate_heavy_patterns():
    """
    Generate four heavy workload types:
      - insertion-heavy (70% inserts, 20% deletes, 10% other ops)
      - deletion-heavy  (20% inserts, 70% deletes, 10% other ops)
      - search-heavy    (10% inserts, 10% deletes, 80% other ops)
      - balanced        (25% inserts, 25% deletes, 50% other ops)
    'Other ops' are evenly split among search(3), pred(4), succ(5), range(6).
    """
    patterns = {
        "insert_heavy":  (70, 20, 10),
        "delete_heavy":  (20, 70, 10),
        "search_heavy":  (10, 10, 80),
        "balanced":      (25, 25, 50),
    }
    for name, (p1, p2, p3) in patterns.items():
        ops = []
        # compute counts
        c1 = int(Q * p1/100)
        c2 = int(Q * p2/100)
        crest = Q - c1 - c2
        # generate inserts
        for _ in range(c1):
            x = random.randint(KEY_MIN, KEY_MAX)
            ops.append((1, x))
        # deletes
        for _ in range(c2):
            x = random.randint(KEY_MIN, KEY_MAX)
            ops.append((2, x))
        # other ops evenly
        coc = crest // 4
        for _ in range(coc):
            x = random.randint(KEY_MIN, KEY_MAX)
            ops.append((3, x))
        for _ in range(coc):
            x = random.randint(KEY_MIN, KEY_MAX)
            ops.append((4, x))
        for _ in range(coc):
            x = random.randint(KEY_MIN, KEY_MAX)
            ops.append((5, x))
        for _ in range(coc):
            x = random.randint(KEY_MIN, KEY_MAX)
            y = random.randint(KEY_MIN, KEY_MAX)
            if x > y: x, y = y, x
            ops.append((6, x, y))
        # adjust to exactly Q
        while len(ops) < Q:
            ops.append((3, random.randint(KEY_MIN, KEY_MAX)))
        if len(ops) > Q:
            ops = ops[:Q]
        random.shuffle(ops)
        write_test(f"{TEST_DIR}/{name}.in", ops)

def generate_range_heavy():
    """Generate a workload with many range queries (type 6)."""
    # 50% inserts, 10% deletes, 20% searches, 20% range
    p = {"i":50, "d":10, "s":20, "r":20}
    # map to op codes
    codes = []
    codes += [1]*int(Q*p["i"]/100)
    codes += [2]*int(Q*p["d"]/100)
    codes += [3]*int(Q*p["s"]/100)
    codes += [6]*int(Q*p["r"]/100)
    # fill remainder with searches
    while len(codes) < Q:
        codes.append(3)
    random.shuffle(codes)

    ops = []
    for op in codes:
        if op in (1,2,3):
            x = random.randint(KEY_MIN, KEY_MAX)
            ops.append((op, x))
        else:  # range
            x = random.randint(KEY_MIN, KEY_MAX)
            y = random.randint(KEY_MIN, KEY_MAX)
            if x>y: x,y=y,x
            ops.append((6, x, y))
    write_test(f"{TEST_DIR}/range_heavy.in", ops)

# ==============================
# Benchmark Harness
# ==============================

def compile_binaries():
    subprocess.run(["g++", "-O2", "-std=c++17", "treap.cpp", "-o", "treap"], check=True)
    subprocess.run(["g++", "-O2", "-std=c++17", "splay.cpp", "-o", "splay"], check=True)

def benchmark():
    results = {name: [] for name in BINARIES}
    test_files = sorted(os.listdir(TEST_DIR))
    sizes = []

    for fn in test_files:
        path = f"{TEST_DIR}/{fn}"
        # Read number of operations (for plotting later)
        with open(path) as f_in:
            n = int(f_in.readline().strip())
        sizes.append(n)

        print(f"▶ Running test file: {fn}", flush=True)
        for name, exe in BINARIES.items():
            print(f"   • {name:6} … ", end="", flush=True)
            start = time.time()
            subprocess.run([exe], stdin=open(path), stdout=subprocess.DEVNULL)
            elapsed = (time.time() - start) * 1000
            print(f"{elapsed:.0f} ms", flush=True)
            results[name].append(elapsed)

    # (rest of your plotting code follows...)


    # Plot
    plt.figure(dpi=300)
    for name, times in results.items():
        plt.plot(sizes, times, label=name, marker='o')
    plt.xscale("log", base=2)
    plt.yscale("log", base=10)
    plt.xlabel("Number of Operations")
    plt.ylabel("Time (ms)")
    plt.legend()
    plt.gca().yaxis.set_major_formatter(ticker.ScalarFormatter())
    plt.title("Treap vs Splay Performance")
    plt.tight_layout()
    plt.savefig("benchmark.png")
    plt.show()

if __name__ == "__main__":
    # 1) Generate all test files
    generate_simple_patterns()
    generate_heavy_patterns()
    generate_range_heavy()
    print("Tests generated in './tests/'")

    # 2) Compile C++ implementations
    compile_binaries()
    print("Binaries compiled.")

    # 3) Run benchmarks and plot
    benchmark()
    print("Benchmark complete. Plot saved to 'benchmark.png'.")
