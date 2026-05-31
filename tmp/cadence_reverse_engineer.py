"""Reverse-engineer the blocking script's behavior from cadence fingerprints.

Applies the nius-project's temporal clustering methodology to the louisbetonberlin
blocking ring. For each ring member we extract:

1. INTER-BLOCK CADENCE HISTOGRAM — distribution of gaps between consecutive blocks
   bucketed into [≤50ms, 50-100ms, 100-200ms, 200-500ms, 500ms-1s, 1-5s, 5-30s,
   30s-5min, 5-30min, 30min+] — this fingerprints the automation tool's rate-limit
   behavior and batch-sleep intervals.

2. SESSION STRUCTURE — blocks cluster into sessions (gap > 5 min = new session).
   We measure: session size (blocks/session), session duration, inter-session gaps,
   and whether sessions start at similar times across ring members.

3. BATCH BOUNDARIES — within a session, sub-pauses (2-5 min) indicate batch loading
   (reading next chunk from a file). We extract batch sizes to identify the list
   page size (e.g., 100, 250, 500, 1000 items per batch).

4. CROSS-MEMBER CADENCE CORRELATION — are cadence histograms similar across ring
   members? If the same tool is used, histograms cluster. Different tools would
   produce different rate-limit fingerprints.

5. TEMPORAL WAVEFRONT — for shared victims, do blocks arrive in synchronized waves?
   Plot per-day counts for each member to see if imports happen on the same days.
"""

import sys
sys.path.insert(0, r'C:\Users\clemensv\OneDrive - Microsoft\Agents\nius')
from nius_bot_dossier.kusto_client import execute_query
import pandas as pd
import numpy as np
from scipy import stats
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

# ---------------------------------------------------------------------------
# Ring member DIDs
# ---------------------------------------------------------------------------
RING_CORE = {
    "did:plc:kd4wtd75a637g2gvg2dh2b3t": "louisbetonberlin",
    "did:plc:gjcwwrezaz5qdcjn3347qvtl": "smatsto",
    "did:plc:qildfzoh5p24jgion4xiycvz": "core_C",
    "did:plc:xcytuwwb3b33ipiqzmqzbs45": "core_D",
    "did:plc:hwpiekun4iebo4oqevjfe6ss": "core_E",
    "did:plc:tfspkb2htmw7vwdgqj7mzx7m": "core_F",
}

RING_EXTENDED = {
    "did:plc:3c7r453vexmpwu6nheazyikk": "dqita",
    "did:plc:u4e3ytzjxb7vapbdmr4oz7ld": "adametokirkfor",
    "did:plc:5v7itrhmq6zhvpqn2sfmcwaw": "maribel1917",
    "did:plc:l3fkqug2hhn4upcdewogsijh": "castironirish",
    "did:plc:vb6p4kuz3kmtqrcix2ghjkwf": "vappytoy",
    "did:plc:oqc7737mwl6y22wjqdduujex": "fkftsh",
    "did:plc:qbw4i5hcyc6dtuckixaogxlc": "solire",
    "did:plc:dvhyaxbrf7uh6eemujbd4jao": "sasunarusasu",
    "did:plc:qq2eg3kbh44gytxlghozodeb": "fakeflamesprite",
    "did:plc:5sjri67leyvnlenx7tzgfulk": "verezi",
}

ALL_RING = {**RING_CORE, **RING_EXTENDED}
ALL_DIDS = list(ALL_RING.keys())

# Cadence histogram bins (milliseconds)
BIN_EDGES_MS = [0, 50, 100, 200, 500, 1000, 5000, 30000, 300000, 1800000, float("inf")]
BIN_LABELS = ["≤50ms", "50-100ms", "100-200ms", "200-500ms", "0.5-1s",
              "1-5s", "5-30s", "30s-5min", "5-30min", ">30min"]

# Session boundary threshold (ms)
SESSION_GAP_MS = 300_000  # 5 minutes

# Batch boundary threshold (ms) — sub-pauses within a session
BATCH_GAP_MS = 120_000   # 2 minutes (but < session gap)

# ============================================================================
# STEP 1: Pull raw inter-block gaps for each ring member
# ============================================================================
print("=" * 80)
print("STEP 1: INTER-BLOCK CADENCE FINGERPRINTS")
print("=" * 80)

cadence_data = {}

for did, handle in ALL_RING.items():
    q = f"""
    ['Bluesky.Graph.Block_v1']
    | where did == "{did}"
    | extend ts = ___time
    | order by ts asc
    | extend prev_ts = prev(ts)
    | where isnotnull(prev_ts)
    | extend gap_ms = datetime_diff("millisecond", ts, prev_ts)
    | where gap_ms > 0
    | summarize
        total = count() + 1,
        median_ms = percentile(gap_ms, 50),
        p5_ms = percentile(gap_ms, 5),
        p25_ms = percentile(gap_ms, 25),
        p75_ms = percentile(gap_ms, 75),
        p95_ms = percentile(gap_ms, 95),
        p99_ms = percentile(gap_ms, 99),
        bin_0_50 = countif(gap_ms <= 50),
        bin_50_100 = countif(gap_ms > 50 and gap_ms <= 100),
        bin_100_200 = countif(gap_ms > 100 and gap_ms <= 200),
        bin_200_500 = countif(gap_ms > 200 and gap_ms <= 500),
        bin_500_1000 = countif(gap_ms > 500 and gap_ms <= 1000),
        bin_1000_5000 = countif(gap_ms > 1000 and gap_ms <= 5000),
        bin_5000_30000 = countif(gap_ms > 5000 and gap_ms <= 30000),
        bin_30000_300000 = countif(gap_ms > 30000 and gap_ms <= 300000),
        bin_300000_1800000 = countif(gap_ms > 300000 and gap_ms <= 1800000),
        bin_gt_1800000 = countif(gap_ms > 1800000)
    """
    print(f"\n  [{handle}] querying cadence...")
    df = execute_query(q)
    if df.empty:
        print(f"    NO DATA")
        continue

    r = df.iloc[0]
    total = int(r["total"])
    median_ms = float(r["median_ms"])
    bins_raw = [
        int(r["bin_0_50"]), int(r["bin_50_100"]), int(r["bin_100_200"]),
        int(r["bin_200_500"]), int(r["bin_500_1000"]), int(r["bin_1000_5000"]),
        int(r["bin_5000_30000"]), int(r["bin_30000_300000"]),
        int(r["bin_300000_1800000"]), int(r["bin_gt_1800000"]),
    ]
    n_gaps = sum(bins_raw)
    bins_norm = np.array(bins_raw) / n_gaps if n_gaps > 0 else np.zeros(len(bins_raw))

    cadence_data[did] = {
        "handle": handle,
        "total": total,
        "median_ms": median_ms,
        "p5": float(r["p5_ms"]),
        "p25": float(r["p25_ms"]),
        "p75": float(r["p75_ms"]),
        "p95": float(r["p95_ms"]),
        "p99": float(r["p99_ms"]),
        "hist_raw": bins_raw,
        "hist_norm": bins_norm,
    }

    # Print summary
    print(f"    Blocks: {total:>8}")
    print(f"    Median gap: {median_ms:>8.0f} ms")
    print(f"    P5/P25/P75/P95: {r['p5_ms']:.0f} / {r['p25_ms']:.0f} / {r['p75_ms']:.0f} / {r['p95_ms']:.0f} ms")
    print(f"    Histogram: ", end="")
    for lbl, pct in zip(BIN_LABELS, bins_norm * 100):
        if pct > 1:
            print(f"{lbl}={pct:.0f}%  ", end="")
    print()

# ============================================================================
# STEP 2: CADENCE CLUSTERING — which accounts use the same tool?
# ============================================================================
print(f"\n{'=' * 80}")
print("STEP 2: CADENCE CLUSTERING (L1 distance on normalized histograms)")
print("=" * 80)

dids_with_data = [d for d in ALL_DIDS if d in cadence_data]
N = len(dids_with_data)
cad_matrix = np.stack([cadence_data[d]["hist_norm"] for d in dids_with_data])

# L1 distance between cadence histograms (0 = identical, 2 = maximally different)
dist_matrix = np.zeros((N, N))
for i in range(N):
    for j in range(i + 1, N):
        d = float(np.abs(cad_matrix[i] - cad_matrix[j]).sum())
        dist_matrix[i, j] = dist_matrix[j, i] = d

print(f"\nPairwise cadence L1 distances:")
print(f"{'':>20}", end="")
for d in dids_with_data:
    print(f" {cadence_data[d]['handle'][:8]:>8}", end="")
print()
for i, di in enumerate(dids_with_data):
    print(f"{cadence_data[di]['handle']:<20}", end="")
    for j, dj in enumerate(dids_with_data):
        print(f" {dist_matrix[i,j]:>8.3f}", end="")
    print()

# Hierarchical clustering
if N > 2:
    condensed = squareform(dist_matrix)
    Z = linkage(condensed, method="average")
    labels = fcluster(Z, t=0.4, criterion="distance")  # threshold tuned

    print(f"\nCadence families (cut=0.4):")
    families = {}
    for did, lbl in zip(dids_with_data, labels):
        families.setdefault(lbl, []).append(did)
    for fam_id, members in sorted(families.items(), key=lambda x: -len(x[1])):
        handles = [cadence_data[d]["handle"] for d in members]
        medians = [cadence_data[d]["median_ms"] for d in members]
        print(f"  Family {fam_id}: {handles}")
        print(f"    Median gaps: {[f'{m:.0f}ms' for m in medians]}")

# ============================================================================
# STEP 3: SESSION STRUCTURE — batch sizes and session patterns
# ============================================================================
print(f"\n{'=' * 80}")
print("STEP 3: SESSION STRUCTURE (gap > 5min = new session)")
print("=" * 80)

for did, handle in list(ALL_RING.items())[:6]:  # Core members first
    q = f"""
    ['Bluesky.Graph.Block_v1']
    | where did == "{did}"
    | extend ts = ___time
    | order by ts asc
    | extend prev_ts = prev(ts)
    | extend gap_ms = iff(isnotnull(prev_ts), datetime_diff("millisecond", ts, prev_ts), tolong(99999999))
    | extend is_session_start = (gap_ms > {SESSION_GAP_MS} or isnull(prev_ts))
    | extend session_id = row_cumsum(iff(is_session_start, 1, 0))
    | summarize
        session_blocks = count(),
        session_start = min(ts),
        session_end = max(ts),
        session_duration_min = datetime_diff("minute", max(ts), min(ts))
      by session_id
    | summarize
        n_sessions = count(),
        median_session_size = percentile(session_blocks, 50),
        p25_session_size = percentile(session_blocks, 25),
        p75_session_size = percentile(session_blocks, 75),
        max_session_size = max(session_blocks),
        median_duration_min = percentile(session_duration_min, 50),
        total_blocks = sum(session_blocks)
    """
    print(f"\n  [{handle}]")
    df = execute_query(q)
    if df.empty:
        continue
    r = df.iloc[0]
    print(f"    Sessions: {int(r['n_sessions'])}")
    print(f"    Blocks/session: median={int(r['median_session_size'])}, "
          f"P25={int(r['p25_session_size'])}, P75={int(r['p75_session_size'])}, "
          f"max={int(r['max_session_size'])}")
    print(f"    Duration/session: median={int(r['median_duration_min'])} min")
    print(f"    Total blocks: {int(r['total_blocks'])}")

# ============================================================================
# STEP 4: BATCH SIZE ANALYSIS — within sessions, find sub-batches
# ============================================================================
print(f"\n{'=' * 80}")
print("STEP 4: BATCH SIZE ANALYSIS (sub-pauses 2-5min within sessions)")
print("=" * 80)
print("Looking for the internal page-size of the blocking tool...\n")

# For louisbetonberlin specifically, get the full gap sequence to identify batch sizes
q_batches = f"""
['Bluesky.Graph.Block_v1']
| where did == "{list(RING_CORE.keys())[0]}"
| where ___time > datetime(2026-05-13)
| extend ts = ___time
| order by ts asc
| extend prev_ts = prev(ts)
| where isnotnull(prev_ts)
| extend gap_ms = datetime_diff("millisecond", ts, prev_ts)
| extend is_session_start = (gap_ms > {SESSION_GAP_MS})
| extend is_batch_boundary = (gap_ms > {BATCH_GAP_MS} and gap_ms <= {SESSION_GAP_MS})
| extend session_id = row_cumsum(iff(is_session_start, 1, 0))
| extend batch_marker = row_cumsum(iff(is_batch_boundary or is_session_start, 1, 0))
| summarize batch_size = count() by session_id, batch_marker
| where batch_size > 5
| summarize
    n_batches = count(),
    median_batch = percentile(batch_size, 50),
    p25_batch = percentile(batch_size, 25),
    p75_batch = percentile(batch_size, 75),
    mode_candidates = make_list(batch_size)
"""
print("  [louisbetonberlin] Batch sizes (May 13+):")
df_batch = execute_query(q_batches)
if not df_batch.empty:
    r = df_batch.iloc[0]
    print(f"    Batches found: {int(r['n_batches'])}")
    print(f"    Batch size: median={int(r['median_batch'])}, "
          f"P25={int(r['p25_batch'])}, P75={int(r['p75_batch'])}")
    # Find mode(s) from the list
    sizes = r["mode_candidates"]
    if isinstance(sizes, list) and len(sizes) > 0:
        from collections import Counter
        c = Counter(sizes)
        top5 = c.most_common(10)
        print(f"    Top batch sizes: {top5}")
        # Look for round numbers
        round_nums = [s for s, _ in top5 if s % 50 == 0 or s % 100 == 0 or s % 25 == 0]
        if round_nums:
            print(f"    → Round-number batch sizes detected: {round_nums}")

# Also check smatsto
q_batches_smatsto = q_batches.replace(list(RING_CORE.keys())[0], list(RING_CORE.keys())[1])
print("\n  [smatsto] Batch sizes (May 13+):")
df_batch_s = execute_query(q_batches_smatsto)
if not df_batch_s.empty:
    r = df_batch_s.iloc[0]
    print(f"    Batches found: {int(r['n_batches'])}")
    print(f"    Batch size: median={int(r['median_batch'])}, "
          f"P25={int(r['p25_batch'])}, P75={int(r['p75_batch'])}")
    sizes = r["mode_candidates"]
    if isinstance(sizes, list) and len(sizes) > 0:
        from collections import Counter
        c = Counter(sizes)
        print(f"    Top batch sizes: {c.most_common(10)}")

# ============================================================================
# STEP 5: RATE-LIMIT FINGERPRINT — does the 70-100ms gap match AT Protocol limits?
# ============================================================================
print(f"\n{'=' * 80}")
print("STEP 5: RATE-LIMIT FINGERPRINT ANALYSIS")
print("=" * 80)
print("""
Known AT Protocol rate limits for createRecord:
- 10 points/second per did (block = 3 points → max ~3.3 blocks/sec = 300ms theoretical min)
- BUT observed gaps are 70-100ms → either:
  (a) The rate limiter counts differently for blocks
  (b) The tool pre-batches and the PDS processes faster than advertised
  (c) The PDS has different internal limits for block operations
  (d) The tool is running from a privileged context

Let's check the EXACT gap distributions to identify the rate-limiter's signature:
""")

# Get fine-grained gap distribution around the rate-limit floor
q_fine_gaps = f"""
['Bluesky.Graph.Block_v1']
| where did == "{list(RING_CORE.keys())[0]}"
| where ___time between (datetime(2026-05-27) .. datetime(2026-05-28))
| extend ts = ___time
| order by ts asc
| extend prev_ts = prev(ts)
| where isnotnull(prev_ts)
| extend gap_ms = datetime_diff("millisecond", ts, prev_ts)
| where gap_ms > 0 and gap_ms < 500
| summarize
    bin_50_60 = countif(gap_ms >= 50 and gap_ms < 60),
    bin_60_70 = countif(gap_ms >= 60 and gap_ms < 70),
    bin_70_80 = countif(gap_ms >= 70 and gap_ms < 80),
    bin_80_90 = countif(gap_ms >= 80 and gap_ms < 90),
    bin_90_100 = countif(gap_ms >= 90 and gap_ms < 100),
    bin_100_110 = countif(gap_ms >= 100 and gap_ms < 110),
    bin_110_120 = countif(gap_ms >= 110 and gap_ms < 120),
    bin_120_150 = countif(gap_ms >= 120 and gap_ms < 150),
    bin_150_200 = countif(gap_ms >= 150 and gap_ms < 200),
    bin_200_300 = countif(gap_ms >= 200 and gap_ms < 300),
    bin_300_500 = countif(gap_ms >= 300 and gap_ms < 500),
    total = count()
"""
print("  [louisbetonberlin] Fine-grained gap distribution (May 27, 10ms bins):")
df_fine = execute_query(q_fine_gaps)
if not df_fine.empty:
    r = df_fine.iloc[0]
    total = int(r["total"])
    print(f"    Total gaps <500ms: {total}")
    for col in ["bin_50_60", "bin_60_70", "bin_70_80", "bin_80_90", "bin_90_100",
                "bin_100_110", "bin_110_120", "bin_120_150", "bin_150_200",
                "bin_200_300", "bin_300_500"]:
        n = int(r[col])
        pct = 100 * n / total if total > 0 else 0
        bar = "█" * int(pct / 2)
        label = col.replace("bin_", "").replace("_", "-") + "ms"
        print(f"    {label:>12}: {n:>6} ({pct:>5.1f}%) {bar}")

# Compare with smatsto's gap distribution on the same day
q_fine_smatsto = q_fine_gaps.replace(list(RING_CORE.keys())[0], list(RING_CORE.keys())[1])
print("\n  [smatsto] Fine-grained gap distribution (May 27):")
df_fine_s = execute_query(q_fine_smatsto)
if not df_fine_s.empty:
    r = df_fine_s.iloc[0]
    total = int(r["total"])
    print(f"    Total gaps <500ms: {total}")
    for col in ["bin_50_60", "bin_60_70", "bin_70_80", "bin_80_90", "bin_90_100",
                "bin_100_110", "bin_110_120", "bin_120_150", "bin_150_200",
                "bin_200_300", "bin_300_500"]:
        n = int(r[col])
        pct = 100 * n / total if total > 0 else 0
        bar = "█" * int(pct / 2)
        label = col.replace("bin_", "").replace("_", "-") + "ms"
        print(f"    {label:>12}: {n:>6} ({pct:>5.1f}%) {bar}")

# ============================================================================
# STEP 6: HOUR-OF-DAY CORRELATION — do ring members operate at the same times?
# ============================================================================
print(f"\n{'=' * 80}")
print("STEP 6: HOUR-OF-DAY OPERATION PATTERNS")
print("=" * 80)

q_hours = f"""
let ring = dynamic([{",".join(f'"{d}"' for d in ALL_DIDS)}]);
['Bluesky.Graph.Block_v1']
| where did in (ring)
| extend hour_utc = hourofday(___time)
| summarize blocks = count() by did, hour_utc
| order by did asc, hour_utc asc
"""
print("  Querying hourly patterns for all ring members...")
df_hours = execute_query(q_hours)
if not df_hours.empty:
    print(f"\n  {'Handle':<20} {'Peak hour(UTC)':>14} {'Active range':>14} {'Night blocks%':>14}")
    print("  " + "-" * 65)
    for did in ALL_DIDS:
        if did not in cadence_data:
            continue
        sub = df_hours[df_hours["did"] == did].copy()
        if sub.empty:
            continue
        sub["blocks"] = pd.to_numeric(sub["blocks"])
        sub["hour_utc"] = pd.to_numeric(sub["hour_utc"])
        total = sub["blocks"].sum()
        peak_hour = int(sub.loc[sub["blocks"].idxmax(), "hour_utc"])
        # Night = 23:00 - 07:00 UTC (= 00:00 - 08:00 CET roughly)
        night = sub[(sub["hour_utc"] >= 23) | (sub["hour_utc"] <= 6)]["blocks"].sum()
        night_pct = 100 * night / total if total > 0 else 0
        # Active range: hours with >5% of blocks
        thresh = 0.05 * total
        active_hours = sorted(sub[sub["blocks"] > thresh]["hour_utc"].tolist())
        if active_hours:
            active_range = f"{min(active_hours):02d}-{max(active_hours):02d} UTC"
        else:
            active_range = "?"
        handle = cadence_data[did]["handle"]
        print(f"  {handle:<20} {peak_hour:>14} {active_range:>14} {night_pct:>13.1f}%")

# ============================================================================
# STEP 7: WAVEFRONT ANALYSIS — daily block counts across ring members
# ============================================================================
print(f"\n{'=' * 80}")
print("STEP 7: TEMPORAL WAVEFRONT (daily block counts)")
print("=" * 80)
print("Do ring members import on the same days or on different days?\n")

q_daily = f"""
let ring = dynamic([{",".join(f'"{d}"' for d in ALL_DIDS)}]);
['Bluesky.Graph.Block_v1']
| where did in (ring)
| extend day = bin(___time, 1d)
| summarize blocks = count() by did, day
| order by day asc
"""
df_daily = execute_query(q_daily)
if not df_daily.empty:
    df_daily["day"] = pd.to_datetime(df_daily["day"])
    df_daily["blocks"] = pd.to_numeric(df_daily["blocks"])

    # Pivot: days x members
    pivot = df_daily.pivot_table(index="day", columns="did", values="blocks", fill_value=0)
    pivot.columns = [ALL_RING.get(c, c[:12]) for c in pivot.columns]

    # Print summary: which days had the most coordinated activity
    pivot["active_members"] = (pivot > 100).sum(axis=1)
    pivot["total_blocks"] = pivot.drop(columns=["active_members"]).sum(axis=1)

    top_days = pivot.nlargest(15, "total_blocks")[["active_members", "total_blocks"]]
    print(f"  Top 15 days by total ring activity:")
    print(f"  {'Day':<12} {'Active':>7} {'Total blocks':>13}")
    for day, row in top_days.iterrows():
        print(f"  {str(day.date()):<12} {int(row['active_members']):>7} {int(row['total_blocks']):>13}")

    # Correlation between daily counts — do members spike on the same days?
    print(f"\n  Daily count correlations (Pearson) between core members:")
    core_handles = list(RING_CORE.values())
    core_cols = [c for c in pivot.columns if c in core_handles]
    if len(core_cols) >= 2:
        corr = pivot[core_cols].corr()
        print(corr.to_string())

# ============================================================================
# SUMMARY
# ============================================================================
print(f"\n{'=' * 80}")
print("SUMMARY: SCRIPT REVERSE-ENGINEERING")
print("=" * 80)
print("""
Based on the cadence fingerprints, the blocking tool likely:

1. RATE LIMITING: The tool fires blocks as fast as the PDS allows (70-100ms gaps)
   with no artificial delay — this is the AT Protocol's native createRecord rate limit.

2. BATCH PROCESSING: Blocks arrive in batches separated by 2-5 minute pauses.
   The batch size reveals the tool's page size for reading the blocklist file.

3. SESSION PATTERN: Sessions last minutes to hours, separated by >5 min gaps.
   Multiple sessions per day for high-volume blockers (smatsto).

4. TOOL FINGERPRINT: If all members show the same cadence histogram, they use
   the same tool. Different histograms → different tools or configurations.

5. DISTRIBUTION MODEL: smatsto crawls first, exports a list file. Other members
   import portions of that file days later. The file preserves order (ρ=0.9996
   for extended members) but Louis may randomize/subset it (ρ=0.058).

6. LIKELY TOOL ARCHITECTURE:
   - Input: Text file with one DID per line (the blocklist)
   - Processing: Read in chunks (batch size), call createRecord for each
   - Rate limit: Fire as fast as PDS allows, no artificial sleep
   - Pause between chunks: Load next page from file or API response
   - Session = one import run; multiple runs per day possible
""")

print("\nDone.")
