import matplotlib.pyplot as plt


def generate_boxplot(values, output):

    plt.figure(figsize=(6,5))


    plt.boxplot(
        values
    )


    plt.ylabel(
        "RTT (ms)"
    )


    plt.title(
        "RTT Distribution"
    )


    plt.grid(True)


    plt.savefig(
        output,
        bbox_inches="tight"
    )


    plt.close()
