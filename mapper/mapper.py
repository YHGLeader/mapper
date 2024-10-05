import wifi
import requests
import matplotlib.pyplot as plt
import numpy as np

def scan_wifi():
    networks = wifi.Cell.all('wlan0')  # Replace 'wlan0' with your actual interface name
    return [(network.ssid, network.signal) for network in networks]

def get_location():
    response = requests.get('https://ipinfo.io')
    return response.json()

def plot_bar_chart(networks, location):
    ssids = [network[0] for network in networks]
    signals = [network[1] for network in networks]

    plt.figure(figsize=(10, 6), facecolor='black')

    bars = plt.bar(ssids, signals, color='green', edgecolor='darkred', alpha=0.8)  # Bar color green with dark red edges
    plt.axhline(y=0, color='green', linestyle='--', label='No Signal')  # Line color to green
    plt.title(f'Nearby Wi-Fi Signals at Location: {location["loc"]}', color='green')  # Title color to green
    plt.xlabel('SSID', color='green')  # X-axis label color to green
    plt.ylabel('Signal Strength (dBm)', color='green')  # Y-axis label color to green
    plt.legend(facecolor='black', edgecolor='green', fontsize='medium', loc='upper left')  # Legend color
    plt.xticks(rotation=45, color='green')  # X-tick color to green
    plt.yticks(color='green')  # Y-tick color to green
    plt.tight_layout()

    return ssids, signals, bars  # Return SSIDs, signals, and bars for event handling

def plot_radar_chart(ssids, signals, location):
    num_networks = len(ssids)
    angles = np.linspace(0, 2 * np.pi, num_networks, endpoint=False).tolist()

    # Closing the loop
    signals += signals[:1]
    angles += angles[:1]

    fig = plt.figure(figsize=(8, 8), facecolor='black')
    ax = fig.add_subplot(121, polar=True)  # Radar chart on the left
    ax.fill(angles, signals, color='green', alpha=0.25)  # Set radar chart fill color to green
    ax.set_yticks(range(-100, 1, 10))
    ax.set_ylim(-100, 0)

    for i in range(num_networks):
        ax.plot(angles[i], signals[i], 'o', markersize=10, color='green', label=ssids[i])  # Point color to green

    ax.set_title('Radar Chart', size=15, color='green')  # Title color to green
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1), facecolor='black', edgecolor='green')

    # Create bar chart on the right
    plt.subplot(122)  # Bar chart on the right
    plt.bar(ssids, signals[:-1], color='green', edgecolor='darkred', alpha=0.8)  # Bar color green with dark red edges
    plt.axhline(y=0, color='green', linestyle='--', label='No Signal')  # Line color to green
    plt.title(f'Nearby Wi-Fi Signals at Location: {location["loc"]}', color='green')  # Title color to green
    plt.xlabel('SSID', color='green')  # X-axis label color to green
    plt.ylabel('Signal Strength (dBm)', color='green')  # Y-axis label color to green
    plt.legend(facecolor='black', edgecolor='green', fontsize='medium', loc='upper left')  # Legend color
    plt.xticks(rotation=45, color='green')  # X-tick color to green
    plt.yticks(color='green')  # Y-tick color to green
    plt.tight_layout()
    
    plt.show()

def scan_selected_wifi(ssid):
    print(f"Scanning for the selected Wi-Fi network: {ssid}")
    # Implement your specific scanning logic here
    # For example, you can try to connect or gather more info about the network

def on_click(event, ssids, bars):
    if event.inaxes == bars[0].axes:  # Check if the click is within the axes of the bar chart
        for bar, ssid in zip(bars, ssids):
            if bar.contains(event.x, event.y)[0]:  # Check if the bar was clicked
                scan_selected_wifi(ssid)
                break

def main():
    previous_ssids = set()  # Store previous SSIDs
    
    print('''
\033[31m ███╗   ███╗ █████╗ ██████╗ ██████╗ ███████╗██████╗ 
 ████╗ ████║██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
 ██╔████╔██║███████║██████╔╝██████╔╝█████╗  ██████╔╝
 ██║╚██╔╝██║██╔══██║██╔═══╝ ██╔═══╝ ██╔══╝  ██╔══██╗
 ██║ ╚═╝ ██║██║  ██║██║     ██║     ███████╗██║  ██║
 ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝     ╚══════╝╚═╝  ╚═╝
                                                   


                                                   \033[0m''')

    command = input("Enter command (type 'map' to visualize nearby Wi-Fi signals): ").strip().lower()
    if command == 'map':
        print("Scanning for Wi-Fi networks...")
        networks = scan_wifi()
        location = get_location()
        
        current_ssids = {network[0] for network in networks}
        new_networks = current_ssids - previous_ssids  # Find new networks

        if new_networks:
            print("New networks detected:", new_networks)
        else:
            print("No new networks detected.")

        # Update previous SSIDs
        previous_ssids.update(current_ssids)

        ssids, signals, bars = plot_bar_chart(networks, location)  # Get ssids and signals from bar chart
        plot_radar_chart(ssids, signals, location)  # Pass ssids and signals to radar chart

        # Connect the click event
        plt.gcf().canvas.mpl_connect('button_press_event', lambda event: on_click(event, ssids, bars))
        
        plt.show()
    else:
        print("Unknown command. Please type 'map'.")

if __name__ == "__main__":
    main()
