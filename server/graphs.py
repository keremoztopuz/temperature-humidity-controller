import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
import os
import matplotlib


def create_live_graph():
    fig, ax = plt.subplots(ani)

    time_data = []
    value_data = []

    def update_plot(frame):
        ax.clear()
        time_data.append(frame)
        value_data.append(random.randint(0, 100))

        # Plot the data
        ax.plot(time_data, value_data, marker='o')
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')
        ax.set_title('Live Graph from PostgreSQL')

    ani = FuncAnimation(fig, update_plot, interval=1000)

    matplotlib.use('Agg')
    plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join(output_folder, 'graph.png'))

    output_folder = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_folder, exist_ok=True)


try:
    plt.savefig('graph.png')
    print("Graph saved successfully.")
except Exception as e:
    print("Error saving graph:", e)
