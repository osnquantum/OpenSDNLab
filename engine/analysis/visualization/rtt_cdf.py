import matplotlib.pyplot as plt


def generate_cdf(values, output):

    values = sorted(values)

    y = [
        (i+1)/len(values)
        for i in range(len(values))
    ]


    plt.figure(figsize=(8,5))

    plt.plot(
        values,
        y
    )

    plt.xlabel(
        "RTT (ms)"
    )

    plt.ylabel(
        "CDF"
    )

    plt.title(
        "RTT CDF"
    )

    plt.grid(True)

    plt.savefig(
        output,
        bbox_inches="tight"
    )

    plt.close()
