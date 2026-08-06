"""
Graph Generator
"""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


class GraphGenerator:

    def generate(self, csv_file):

        csv_file = Path(csv_file)

        output_dir = csv_file.parent

        data = pd.read_csv(csv_file)

        ########################################################
        # Delay vs RTT
        ########################################################

        plt.figure(figsize=(8, 5))

        plt.plot(
            data["Delay"].str.replace("ms", "").astype(float),
            data["Average RTT"],
            marker="o",
        )

        plt.title("Delay vs Average RTT")

        plt.xlabel("Delay (ms)")

        plt.ylabel("Average RTT (ms)")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            output_dir / "delay_vs_rtt.png",
            dpi=300,
        )

        plt.close()

        ########################################################
        # Delay vs Throughput
        ########################################################

        plt.figure(figsize=(8, 5))

        plt.plot(
            data["Delay"].str.replace("ms", "").astype(float),
            data["Throughput"],
            marker="o",
        )

        plt.title("Delay vs Throughput")

        plt.xlabel("Delay (ms)")

        plt.ylabel("Throughput (Mbps)")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            output_dir / "delay_vs_throughput.png",
            dpi=300,
        )

        plt.close()

        ########################################################
        # Delay vs Jitter
        ########################################################

        plt.figure(figsize=(8, 5))

        plt.plot(
            data["Delay"].str.replace("ms", "").astype(float),
            data["Jitter"],
            marker="o",
        )

        plt.title("Delay vs Jitter")

        plt.xlabel("Delay (ms)")

        plt.ylabel("Jitter (ms)")

        plt.grid(True)

        plt.tight_layout()

        plt.savefig(
            output_dir / "delay_vs_jitter.png",
            dpi=300,
        )

        plt.close()

        return output_dir

