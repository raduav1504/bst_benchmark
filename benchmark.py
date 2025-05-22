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
# You can temporarily set this to 10_000 for a quick dry-run
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
    patterns = {
        "insert_heavy":  (70, 20, 10),
        "delete_heavy":  (20, 70, 10),
        "search_heavy":  (10, 10, 80),
        "balanced":      (25, 25, 50),
    }
    for name, (p1, p2, p3) in patterns.items():
        ops = []
        c1 = int(Q * p1/100)
        c2 = int(Q * p2/100)
        crest = Q - c1 - c2

        for _ in range(c1):
            ops.append((1, random.randint(KEY_MIN, KEY_MAX)))
        for _ in range(c2):
            ops.append((2, random.randint(KEY_MIN, KEY_MAX)))
        coc = crest // 4
        for _ in range(coc):
            ops.append((3, random.randint(KEY_MIN, KEY_MAX)))
        for _ in range(coc):
            ops.append((4, random.randint(KEY_MIN, KEY_MAX)))
        for _ in range(coc):
            ops.append((5, random.randint(KEY_MIN, KEY_MAX)))
        for _ in range(coc):
            x = random.randint(KEY_MIN, KEY_MAX)
            y = random.randint(KEY_MIN, KEY_MAX)
            if x > y: x, y = y, x
            ops.append((6, x, y))

        # pad/truncate to exactly Q
        if len(ops) < Q:
            ops += [(3, random.randint(KEY_MIN, KEY_MAX))] * (Q - len(ops))
        else:
            ops = ops[:Q]

        random.shuffle(ops)
        write_test(f"{TEST_DIR}/{name}.in", ops)

def generate_range_heavy():
    p = {"i":50, "d":10, "s":20, "r":20}
    codes = [1]*int(Q*p["i"]/100) + \
            [2]*int(Q*p["d"]/100) + \
            [3]*int(Q*p["s"]/100) + \
            [6]*int(Q*p["r"]/100)
    while len(codes) < Q:
        codes.append(3)
    random.shuffle(codes)

    ops = []
    for op in codes:
        if op in (1,2,3):
            ops.append((op, random.randint(KEY_MIN, KEY_MAX)))
        else:
            x = random.randint(KEY_MIN, KEY_MAX)
            y = random.randint(KEY_MIN, KEY_MAX)
            if x > y: x, y = y, x
            ops.append((6, x, y))
    write_test(f"{TEST_DIR}/range_heavy.in", ops)

# ==============================
# Benchmark Harness
# ==============================
def compile_binaries():
    subprocess.run(["g++", "-O2", "-std=c++17", "treap.cpp", "-o", "treap"], check=True)
    subprocess.run(["g++", "-O2", "-std=c++17", "splay.cpp", "-o", "splay"], check=True)

def benchmark():
    print("=== benchmark() START ===", flush=True)
    results = {name: [] for name in BINARIES}

    # DEBUG: show what tests folder looks like
    test_files = sorted(os.listdir(TEST_DIR))
    print("DEBUG: test_files =", test_files, flush=True)

    sizes = []

    for fn in test_files:
        print("DEBUG: loop got fn =", fn, flush=True)
        path = f"{TEST_DIR}/{fn}"
        with open(path) as f_in:
            n = int(f_in.readline().strip())
        sizes.append(n)

        print(f"▶ Running {fn}", flush=True)
        for name, exe in BINARIES.items():
            print(f"   • {name:6} … ", end="", flush=True)
            start = time.time()
            subprocess.run([exe], stdin=open(path), stdout=subprocess.DEVNULL)
            elapsed = (time.time() - start) * 1000
            print(f"{elapsed:.0f} ms", flush=True)
            results[name].append(elapsed)


    # Plot results
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
    print("Benchmark complete. Plot saved to 'benchmark.png'.")

if __name__ == "__main__":
    generate_simple_patterns()
    generate_heavy_patterns()
    generate_range_heavy()
    print("Tests generated in './tests/'")
    compile_binaries()
    print("Binaries compiled.")
    benchmark()
