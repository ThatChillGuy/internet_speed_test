# Internet Speed Tester

A Python program that measures download and upload speeds, displays ping results and connection stability, provides tips for improving internet speed, and tracks speed trends over time.

## Features

- Measures download and upload speeds
- Displays ping results and connection stability
- Provides personalized tips for improving internet speed
- Logs test results to track speed trends over time
- Visualizes current results and historical data

## Requirements

- Python 3.6 or higher
- speedtest-cli package
- matplotlib package

## Installation

1. Make sure you have Python installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. Install the required packages by running the following commands in a command prompt or terminal:

```
pip install speedtest-cli
pip install matplotlib
```

## Usage

### Option 1: Using the Batch File (Recommended for Windows)

1. Double-click the `run_speed_test.bat` file.
2. The program will start and display a menu with options.
3. The console window will remain open even if errors occur.

### Option 2: Running from Command Line

1. Open a command prompt or terminal.
2. Navigate to the directory containing the script:
   ```
   cd path\to\your\script
   ```
3. Run the script:
   ```
   python speed_test.py
   ```

### Option 3: Running in VSCode

1. Open the script in VSCode.
2. Click the "Run" button or press F5.

## Menu Options

1. **Run Speed Test**: Measures your download and upload speeds, ping, and connection stability.
2. **View Improvement Tips**: Provides personalized tips based on your test results.
3. **Visualize Current Results**: Creates and displays a graph of your current test results.
4. **Visualize Speed History**: Creates and displays graphs of your speed test history.
5. **Exit**: Exits the program.

## Logs and Visualizations

- Test results are logged to a JSON file in the `logs` directory.
- Visualizations are saved as PNG files in the current directory:
  - `current_speed_test.png`: Graph of current test results
  - `speed_test_history.png`: Graph of historical test data

## Troubleshooting

If you encounter any issues:

1. **Program closes immediately**: Use the batch file (`run_speed_test.bat`) to run the program.
2. **Missing packages**: Make sure you've installed the required packages using pip.
3. **Python not found**: Make sure Python is installed and added to your system PATH.
