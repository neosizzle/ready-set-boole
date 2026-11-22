#!/usr/bin/env python3

import json
import sys
import math
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ==========================================
# Configuration
# ==========================================

OUTPUT_HTML = "complexity_analysis.html"

COMPLEXITIES = {
    "Constant": lambda n: 1,
    "Linear": lambda n: n,
    "NLogN": lambda n: n * math.log2(n),
    "LogN": lambda n: math.log2(n),
    "Quadratic": lambda n: n ** 2,
}

# Fixed color per complexity so a given reference curve looks the
# same in every subplot. None of these is the measured-trace blue.
REFERENCE_COLORS = {
    "Constant": "#ff7f0e",
    "Linear": "#d62728",
    "NLogN": "#9467bd",
    "LogN": "#2ca02c",
    "Quadratic": "#8c564b",
}

MEASURED_COLOR = "#1f77b4"


# ==========================================
# Extract benchmark results
# ==========================================

def load_results(result_file):

    with open(result_file, "r") as file:
        results = json.load(file)

    benchmarks = {}
    units = {}

    for item in results["benchmarks"]:

        name = item["name"]

        # Ignore complexity aggregate rows.
        if "BigO" in name or "RMS" in name:
            continue

        parts = name.split("/")

        if len(parts) < 2:
            continue

        benchmark_name = parts[0]

        try:
            n = int(parts[1])
        except ValueError:
            continue

        time = item.get("cpu_time")

        if time is None:
            time = item.get("real_time")

        if time is None:
            continue

        benchmarks.setdefault(benchmark_name, []).append(
            (n, time)
        )

        # Capture the real unit reported by Google Benchmark
        # instead of assuming nanoseconds.
        units.setdefault(
            benchmark_name,
            item.get("time_unit", "ns")
        )

    return benchmarks, units


# ==========================================
# Plot benchmark results
# ==========================================

def plot_results(benchmarks, units):

    algorithms = list(benchmarks.keys())

    if not algorithms:
        raise RuntimeError("No benchmark measurements found.")

    # vertical_spacing must be <= 1 / (rows - 1); keep it safe for
    # large numbers of algorithms.
    rows = len(algorithms)
    vertical_spacing = min(0.08, 1.0 / max(rows - 1, 1))

    fig = make_subplots(
        rows=rows,
        cols=1,
        subplot_titles=algorithms,
        vertical_spacing=vertical_spacing
    )

    for index, algorithm in enumerate(algorithms, start=1):

        data = sorted(benchmarks[algorithm])

        n_values = [x[0] for x in data]
        times = [x[1] for x in data]

        unit = units.get(algorithm, "ns")

        # ======================================
        # Measured benchmark results
        # ======================================

        fig.add_trace(
            go.Scatter(
                x=n_values,
                y=times,
                mode="lines+markers",
                name="Measured",
                legendgroup="measured",
                showlegend=(index == 1),
                line=dict(
                    color=MEASURED_COLOR,
                    width=3
                ),
                marker=dict(size=7),
                hovertemplate=(
                    f"<b>{algorithm} - Measured</b><br>"
                    "Input size: %{x}<br>"
                    f"CPU Time: %{{y:.3f}} {unit}"
                    "<extra></extra>"
                )
            ),
            row=index,
            col=1
        )

        # ======================================
        # Theoretical complexity reference curves
        # ======================================

        for name, function in COMPLEXITIES.items():

            # Anchor the reference curve at the first point whose
            # theoretical value is non-zero. This avoids dividing by
            # zero for LogN / NLogN when the smallest N is 1
            # (log2(1) == 0).
            anchor = next(
                (
                    (n, t)
                    for n, t in zip(n_values, times)
                    if function(n) != 0
                ),
                None
            )

            if anchor is None:
                continue

            anchor_n, anchor_time = anchor

            reference = [
                anchor_time * function(n) / function(anchor_n)
                for n in n_values
            ]

            fig.add_trace(
                go.Scatter(
                    x=n_values,
                    y=reference,
                    mode="lines",
                    name=f"O({name}) reference",
                    legendgroup=name,
                    showlegend=(index == 1),
                    line=dict(
                        color=REFERENCE_COLORS.get(name),
                        dash="dash",
                        width=2
                    ),
                    opacity=0.7,
                    hovertemplate=(
                        f"<b>{algorithm} - O({name})</b><br>"
                        "Input size: %{x}<br>"
                        f"Reference Time: %{{y:.3f}} {unit}"
                        "<extra></extra>"
                    )
                ),
                row=index,
                col=1
            )

        # ======================================
        # Axes
        # ======================================

        fig.update_xaxes(
            title_text="Input size (N)",
            type="log",
            row=index,
            col=1
        )

        fig.update_yaxes(
            title_text=f"CPU time ({unit})",
            type="log",
            row=index,
            col=1
        )

    # ==========================================
    # Layout
    # ==========================================

    fig.update_layout(
        title="Algorithm Complexity Analysis",
        height=500 * rows,
        template="plotly_white",
        hovermode="closest",
        # Extra top room so the horizontal legend and the toggle
        # buttons don't sit on top of the first subplot's title.
        margin=dict(t=160),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0
        )
    )

    # ==========================================
    # Axis scale toggle buttons
    # ==========================================

    def axis_relayout(x_type, y_type):
        """Build a relayout dict that targets EVERY subplot's axes."""
        relayout = {}
        for i in range(1, rows + 1):
            x_key = "xaxis" if i == 1 else f"xaxis{i}"
            y_key = "yaxis" if i == 1 else f"yaxis{i}"
            relayout[f"{x_key}.type"] = x_type
            relayout[f"{y_key}.type"] = y_type
        return relayout

    buttons = [
        dict(
            label="Log X / Log Y",
            method="relayout",
            args=[axis_relayout("log", "log")]
        ),
        dict(
            label="Linear X / Linear Y",
            method="relayout",
            args=[axis_relayout("linear", "linear")]
        ),
        dict(
            label="Log X / Linear Y",
            method="relayout",
            args=[axis_relayout("log", "linear")]
        ),
        dict(
            label="Linear X / Log Y",
            method="relayout",
            args=[axis_relayout("linear", "log")]
        )
    ]

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                buttons=buttons,
                x=0,
                y=1.06,
                xanchor="left",
                yanchor="bottom"
            )
        ]
    )

    # ==========================================
    # Save and display
    # ==========================================

    fig.write_html(
        OUTPUT_HTML,
        include_plotlyjs=True,
        full_html=True
    )

    print(f"Interactive graph saved to {OUTPUT_HTML}")

    fig.show()


# ==========================================
# Main
# ==========================================

def main():

    if len(sys.argv) != 2:
        print(
            f"Usage: python {Path(sys.argv[0]).name} "
            "<result_file.json>"
        )
        sys.exit(1)

    result_file = Path(sys.argv[1])

    if not result_file.is_file():
        print(f"Error: Result file not found: {result_file}")
        sys.exit(1)

    try:

        print(f"Loading results from: {result_file}")

        benchmarks, units = load_results(result_file)

        if not benchmarks:
            print("No benchmark measurements found.")
            return

        # Print extracted results.
        for algorithm, measurements in benchmarks.items():

            unit = units.get(algorithm, "ns")

            print(f"\n{algorithm}")

            for n, time in sorted(measurements):
                print(
                    f"  N = {n:<10} CPU Time = {time} {unit}"
                )

        print("\nGenerating interactive complexity graphs...")

        plot_results(benchmarks, units)

        print("\nBenchmark analysis completed.")

    except Exception as error:
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()