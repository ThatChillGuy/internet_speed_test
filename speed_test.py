#!/usr/bin/env python3
"""
Internet Speed Tester
---------------------
A program that measures download and upload speeds, displays ping results and connection stability,
and provides tips for improving internet speed. It also logs test results to track speed trends over time.
"""

import os
import sys
import time
import json
import datetime
from pathlib import Path
import statistics

# Check if required packages are installed
try:
    import speedtest
except ImportError:
    print("speedtest-cli is not installed. Run the following command to install it:")
    print("pip install speedtest-cli")
    sys.exit(1)

try:
    import matplotlib.pyplot as plt
except ImportError:
    print("matplotlib is not installed. Run the following command to install it:")
    print("pip install matplotlib")
    sys.exit(1)

class InternetSpeedTester:
    """Class for testing internet speed and logging results."""
    
    def __init__(self):
        """Initialize the speed tester."""
        self.log_dir = Path("logs")
        self.log_file = self.log_dir / "speed_test_log.json"
        self.results = None
        self.stability_samples = []
        
        # Create logs directory if it doesn't exist
        if not self.log_dir.exists():
            self.log_dir.mkdir(parents=True)
            
        # Create log file if it doesn't exist
        if not self.log_file.exists():
            with open(self.log_file, 'w') as f:
                json.dump([], f)
    
    def run_test(self):
        """Run the speed test and return the results."""
        print("Running speed test... (this may take a minute)")
        
        try:
            st = speedtest.Speedtest()
            st.get_best_server()
            
            # Measure download speed
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            print(f"Download Speed: {download_speed:.2f} Mbps")
            
            # Measure upload speed
            upload_speed = st.upload() / 1_000_000  # Convert to Mbps
            print(f"Upload Speed: {upload_speed:.2f} Mbps")
            
            # Get ping
            ping = st.results.ping
            print(f"Ping: {ping:.2f} ms")
            
            # Test connection stability (by taking multiple ping samples)
            print("Testing connection stability...")
            self.stability_samples = self.test_stability()
            stability_score = self.calculate_stability_score()
            
            # Store results
            self.results = {
                "timestamp": datetime.datetime.now().isoformat(),
                "download_speed": round(download_speed, 2),
                "upload_speed": round(upload_speed, 2),
                "ping": round(ping, 2),
                "stability_score": stability_score,
                "stability_rating": self.get_stability_rating(stability_score)
            }
            
            return self.results
            
        except Exception as e:
            print(f"Error running speed test: {e}")
            return None
    
    def test_stability(self, samples=10):
        """Test connection stability by taking multiple ping samples."""
        ping_samples = []
        
        st = speedtest.Speedtest()
        server = st.get_best_server()
        
        for _ in range(samples):
            start_time = time.time()
            st.get_best_server()  # This sends a request to the server
            ping_time = (time.time() - start_time) * 1000  # Convert to ms
            ping_samples.append(ping_time)
            time.sleep(0.5)  # Wait half a second between samples
            
        return ping_samples
    
    def calculate_stability_score(self):
        """Calculate a stability score based on ping variation."""
        if not self.stability_samples:
            return 0
            
        # Lower standard deviation means more stable connection
        std_dev = statistics.stdev(self.stability_samples) if len(self.stability_samples) > 1 else 0
        avg_ping = statistics.mean(self.stability_samples)
        
        # Calculate coefficient of variation (CV) as a measure of stability
        cv = (std_dev / avg_ping) if avg_ping > 0 else 0
        
        # Convert to a 0-100 score (lower CV is better)
        # A CV of 0 means perfect stability (score 100)
        # A CV of 0.5 or higher means poor stability (score 0)
        stability_score = max(0, min(100, 100 * (1 - 2 * cv)))
        
        return round(stability_score, 2)
    
    def get_stability_rating(self, score):
        """Convert stability score to a rating."""
        if score >= 90:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 50:
            return "Fair"
        elif score >= 30:
            return "Poor"
        else:
            return "Very Poor"
    
    def log_results(self):
        """Log the test results to a file."""
        if not self.results:
            print("No results to log.")
            return
            
        # Read existing logs
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
            
        # Add new log
        logs.append(self.results)
        
        # Write updated logs
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)
            
        print(f"Results logged to {self.log_file}")
    
    def get_improvement_tips(self):
        """Generate tips for improving internet speed based on test results."""
        if not self.results:
            return ["Run a speed test first to get personalized tips."]
            
        tips = ["Tips for improving your internet speed:"]
        
        # Tips based on download speed
        download_speed = self.results["download_speed"]
        if download_speed < 10:
            tips.append("- Your download speed is quite low. Consider upgrading your internet plan.")
            tips.append("- Connect to your router using an Ethernet cable instead of Wi-Fi for better speeds.")
        
        # Tips based on upload speed
        upload_speed = self.results["upload_speed"]
        if upload_speed < 5:
            tips.append("- Your upload speed is low, which may affect video calls and file uploads.")
            tips.append("- Close background applications that might be uploading data.")
        
        # Tips based on ping
        ping = self.results["ping"]
        if ping > 50:
            tips.append("- Your ping is high, which may cause lag in online games and video calls.")
            tips.append("- Connect to a server that's geographically closer to you if possible.")
            tips.append("- Reduce the number of devices connected to your network.")
        
        # Tips based on stability
        stability_score = self.results["stability_score"]
        if stability_score < 70:
            tips.append("- Your connection stability is not optimal, which may cause intermittent issues.")
            tips.append("- Check for interference from other electronic devices.")
            tips.append("- Update your router's firmware or consider replacing an old router.")
            tips.append("- Position your router in a central location, away from walls and obstructions.")
        
        # General tips
        tips.append("- Restart your router and modem if you haven't done so recently.")
        tips.append("- Check for malware or background processes that might be using your bandwidth.")
        tips.append("- Consider using a wired connection for critical activities like gaming or video conferencing.")
        
        return tips
    
    def visualize_results(self):
        """Visualize the current test results."""
        if not self.results:
            print("No results to visualize.")
            return
            
        # Create a figure with subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot current speeds
        speeds = [self.results["download_speed"], self.results["upload_speed"]]
        labels = ["Download", "Upload"]
        colors = ["#3498db", "#2ecc71"]
        
        ax1.bar(labels, speeds, color=colors)
        ax1.set_title("Current Internet Speeds")
        ax1.set_ylabel("Speed (Mbps)")
        ax1.grid(axis="y", linestyle="--", alpha=0.7)
        
        # Add speed values on top of bars
        for i, speed in enumerate(speeds):
            ax1.text(i, speed + 0.5, f"{speed} Mbps", ha="center")
        
        # Plot ping and stability
        ping = self.results["ping"]
        stability = self.results["stability_score"]
        
        ax2.bar(["Ping (ms)", "Stability (%)"], [ping, stability], color=["#e74c3c", "#f39c12"])
        ax2.set_title("Ping and Connection Stability")
        ax2.grid(axis="y", linestyle="--", alpha=0.7)
        
        # Add values on top of bars
        ax2.text(0, ping + 2, f"{ping} ms", ha="center")
        ax2.text(1, stability + 2, f"{stability}%", ha="center")
        
        plt.tight_layout()
        
        # Save the figure
        plt.savefig("current_speed_test.png")
        print("Results visualization saved as 'current_speed_test.png'")
        
        # Show the figure
        plt.show()
    
    def visualize_history(self):
        """Visualize historical speed test data."""
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            print("No historical data available.")
            return
            
        if not logs:
            print("No historical data available.")
            return
            
        # Extract data
        timestamps = [datetime.datetime.fromisoformat(log["timestamp"]) for log in logs]
        download_speeds = [log["download_speed"] for log in logs]
        upload_speeds = [log["upload_speed"] for log in logs]
        pings = [log["ping"] for log in logs]
        
        # Create a figure with subplots
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
        
        # Plot download and upload speeds
        ax1.plot(timestamps, download_speeds, marker='o', linestyle='-', color="#3498db", label="Download")
        ax1.plot(timestamps, upload_speeds, marker='s', linestyle='-', color="#2ecc71", label="Upload")
        ax1.set_title("Internet Speed History")
        ax1.set_ylabel("Speed (Mbps)")
        ax1.grid(True, linestyle="--", alpha=0.7)
        ax1.legend()
        
        # Format x-axis dates
        fig.autofmt_xdate()
        
        # Plot ping
        ax2.plot(timestamps, pings, marker='d', linestyle='-', color="#e74c3c")
        ax2.set_title("Ping History")
        ax2.set_ylabel("Ping (ms)")
        ax2.set_xlabel("Date")
        ax2.grid(True, linestyle="--", alpha=0.7)
        
        plt.tight_layout()
        
        # Save the figure
        plt.savefig("speed_test_history.png")
        print("History visualization saved as 'speed_test_history.png'")
        
        # Show the figure
        plt.show()


def main():
    """Main function to run the speed test."""
    tester = InternetSpeedTester()
    
    print("=" * 50)
    print("Internet Speed Tester")
    print("=" * 50)
    
    while True:
        print("\nOptions:")
        print("1. Run Speed Test")
        print("2. View Improvement Tips")
        print("3. Visualize Current Results")
        print("4. Visualize Speed History")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            results = tester.run_test()
            if results:
                print("\nTest Results:")
                print(f"Download Speed: {results['download_speed']} Mbps")
                print(f"Upload Speed: {results['upload_speed']} Mbps")
                print(f"Ping: {results['ping']} ms")
                print(f"Connection Stability: {results['stability_score']}% ({results['stability_rating']})")
                tester.log_results()
        
        elif choice == "2":
            tips = tester.get_improvement_tips()
            print("\n" + "\n".join(tips))
        
        elif choice == "3":
            tester.visualize_results()
        
        elif choice == "4":
            tester.visualize_history()
        
        elif choice == "5":
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

    # Prevent console from closing immediately
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()