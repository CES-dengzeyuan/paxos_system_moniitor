import re
import pandas as pd
import matplotlib.pyplot as plt

# Initialize empty lists to store data
cpu_utilization = []
load_avg_5min = []
sent_rates = []
recv_rates = []
memory_usage = []


def init_data():
    cpu_utilization.clear()
    load_avg_5min.clear()
    sent_rates.clear()
    recv_rates.clear()
    memory_usage.clear()


def get_data(filename):
    with open(filename, 'r') as f:
        for line in f:
            # Extract CPU utilization
            match = re.search(r'CPU utilization: (\d+\.\d+)%', line)
            if match:
                cpu_utilization.append(float(match.group(1)))

            # Extract 5-minute system load average
            match = re.search(r'5 minutes: (\d+\.\d+)', line)
            if match:
                load_avg_5min.append(float(match.group(1)))

            # Extract Network bandwidth utilization rate
            match = re.search(r'Sent: (\d+\.\d+) Mbps, Received: (\d+\.\d+) Mbps', line)
            if match:
                sent_rate = float(match.group(1)) * 1000000 / (1024 * 1024)
                recv_rate = float(match.group(2)) * 1000000 / (1024 * 1024)
                sent_rates.append(sent_rate)
                recv_rates.append(recv_rate)

            # Extract memory usage
            match = re.search(r'Memory utilization: (\d+\.\d+)%', line)
            if match:
                memory_usage.append(float(match.group(1)))


def plot(filename):
    init_data()
    get_data(filename)
    # Convert the lists to pandas dataframes
    df_cpu = pd.DataFrame({'CPU Utilization': cpu_utilization})
    df_load = pd.DataFrame({'5-Minute System Load Average': load_avg_5min})
    df_sent = pd.DataFrame({'Network bandwidth utilization rate - Sent': sent_rates})
    df_recv = pd.DataFrame({'Network bandwidth utilization rate - Received': recv_rates})
    df_memory = pd.DataFrame({'Memory utilization': memory_usage})

    # Merge the dataframes
    df_cpu_load = pd.concat([df_cpu, df_load], axis=1)
    df_sent_recv = pd.concat([df_sent, df_recv], axis=1)

    # Plot the data using matplotlib
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 10))

    color = 'tab:red'
    axes[0].set_xlabel('Time')
    axes[0].set_ylabel('CPU Utilization (%)', color=color)
    axes[0].plot(df_cpu_load['CPU Utilization'], color=color)
    axes[0].tick_params(axis='y', labelcolor=color)

    ax2 = axes[0].twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('5-Minute System Load Average', color=color)
    ax2.plot(df_cpu_load['5-Minute System Load Average'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    color = 'tab:red'
    axes[1].set_xlabel('Time')
    axes[1].set_ylabel('Network bandwidth utilization rate - Sent (Mbps)', color=color)
    axes[1].plot(df_sent['Network bandwidth utilization rate - Sent'], color=color)
    axes[1].tick_params(axis='y', labelcolor=color)

    ax2 = axes[1].twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('Network bandwidth utilization rate - Received (Mbps)', color=color)
    ax2.plot(df_recv['Network bandwidth utilization rate - Received'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    df_memory.plot(ax=axes[2], legend=None)
    axes[2].set_ylabel('Memory utilization (%)')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped

    # Show the plot
    # plt.show()
    plt.savefig(filename.split('/')[1].split('.')[0] + '.png')
    plt.close()
