import os, random, subprocess, time


NUM_QUERIES = 1_000_000
MAX_VAL     = 1_000_000_000
TEST_DIR    = "tests"
os.makedirs(TEST_DIR, exist_ok=True)

BINARIES = {
    'treap': './treap',
    'splay': './splay',
}

percentages = {}
for op in range(1, 7):
    name = f"heavy_op{op}"
    percentages[name] = {i: 6.0 for i in range(1, 7)}
    percentages[name][op] = 70.0

equal_pct = 100.0 / 6.0
percentages['equal_mix'] = {i: equal_pct for i in range(1, 7)}


categories = {}
for cat, pct_map in percentages.items():
    quotas = {i: int(NUM_QUERIES * pct_map[i] / 100.0) for i in range(1, 7)}
    total = sum(quotas.values())
    # Corectam din cauza rotunjirii
    i = 1
    while total < NUM_QUERIES:
        quotas[i] += 1
        total += 1
        i = i % 6 + 1
    while total > NUM_QUERIES:
        quotas[i] -= 1
        total -= 1
        i = i % 6 + 1
    categories[cat] = quotas

#generare fisiere test
print("Generating test files…")
test_paths = {}
for cat, quotas in categories.items():
    path = os.path.join(TEST_DIR, f"{cat}.in")
    with open(path, 'w') as f:
        f.write(f"{NUM_QUERIES}\n")
        # construim lista de coduri op, o shuffle-uim
        ops = []
        for op_code, count in quotas.items():
            ops += [op_code] * count
        random.shuffle(ops)
        # scriem fiecare linie
        for op in ops:
            if op in (1,2,3,4,5):
                x = random.randint(-MAX_VAL, MAX_VAL)
                f.write(f"{op} {x}\n")
            else:  # op == 6
                x = random.randint(-MAX_VAL, MAX_VAL)
                y = random.randint(-MAX_VAL, MAX_VAL)
                if x > y: x, y = y, x
                f.write(f"6 {x} {y}\n")
    test_paths[cat] = path
    print(f"  • {cat}.in ([{percentages[cat][1]:.1f}%, …, {percentages[cat][6]:.1f}%])")

#masuram timp
print("\nRunning benchmarks:")
results = {cat: {} for cat in categories}
for cat, path in test_paths.items():
    print(f"\n-- {cat} --")
    for name, exe in BINARIES.items():
        t0 = time.time()
        subprocess.run([exe], stdin=open(path), stdout=subprocess.DEVNULL)
        ms = (time.time() - t0) * 1000
        results[cat][name] = ms
        print(f"   {name:6s}: {ms:.0f} ms")

#tabel final
print("\nSummary (ms):")
# header
print(f"{'Test':20s}", end="")
for name in BINARIES:
    print(f"{name:>10s}", end="")
print()
# rows
for cat in categories:
    print(f"{cat:20s}", end="")
    for name in BINARIES:
        print(f"{results[cat][name]:10.0f}", end="")
    print()
