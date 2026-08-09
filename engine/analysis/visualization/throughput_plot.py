import matplotlib.pyplot as plt


def generate_throughput(values, output):

    plt.figure(figsize=(8,5))


    plt.plot(
        range(1,len(values)+1),
        values,
        marker="o"
    )


    plt.xlabel(
        "Experiment Run"
    )


    plt.ylabel(
        "Throughput (Mbps)"
    )


    plt.title(
        "Throughput Stability"
    )


    plt.grid(True)


    plt.savefig(
        output,
        bbox_inches="tight"
    )


    plt.close()
