import matplotlib.pyplot as plt

def plot_population_trend(data, country):
    """
    Plot the population trend for the selected country.
    """
    if data is None or data.empty:
        print("No data available for plotting population trend.")
        return

    # Plot only if data exists
    plt.figure(figsize=(10, 5))
    plt.plot(data.columns, data.values.flatten(), marker='o', label=f"{country} Population")
    plt.title(f"{country} Population Trend")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.legend()
    plt.grid()
    plt.show()

def plot_growth_rate(data, country):
    """
    Plot the yearly growth rate for the selected country.
    """
    if data is None or data.empty:
        print("No data available for plotting growth rate.")
        return

    # Plot only if data exists
    plt.figure(figsize=(10, 5))
    plt.bar(data.columns, data.values.flatten(), color='orange', label=f"{country} Growth Rate")
    plt.title(f"{country} Yearly Growth Rate")
    plt.xlabel("Year")
    plt.ylabel("Growth Rate (%)")
    plt.legend()
    plt.grid()
    plt.show()
