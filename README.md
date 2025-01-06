# CPU Scheduling Simulator

A Python implementation of common CPU scheduling algorithms used in operating systems, featuring performance metrics calculation and Gantt chart visualization.

## Overview

This project simulates four fundamental CPU scheduling algorithms:
- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Shortest Remaining Time First (SRTF)
- Round Robin (RR)

The simulator calculates key performance metrics and generates visual representations of process execution through Gantt charts.

## Features

- **Multiple Scheduling Algorithms**:
  - FCFS: Non-preemptive scheduling based on arrival order
  - SJF: Non-preemptive scheduling based on burst time
  - SRTF: Preemptive version of SJF
  - RR: Time-slice based scheduling

- **Performance Metrics**:
  - Average Response Time
  - Average Turnaround Time
  - Average Waiting Time
  - Overall CPU Usage

- **Visual Representation**:
  - Gantt Chart Generation
  - Process Timeline Visualization
  - Idle Time Display

## Getting Started

### Prerequisites
- Python 3.x
- No additional modules required

### Installation
1. Clone the repository
```bash
git clone https://github.com/[your-username]/cpu-scheduling-simulator.git
```

2. Navigate to the project directory
```bash
cd cpu-scheduling-simulator
```

3. Run the simulator
```bash
python main.py
```

## Usage

1. Select number of processes (max 5)
2. For each process, enter:
   - Process ID (1-5)
   - Arrival Time (non-negative)
   - Burst Time (non-negative)
3. Choose scheduling algorithm:
   - A: First Come First Serve
   - B: Shortest Job First
   - C: Shortest Remaining Time First
   - D: Round Robin

## Implementation Details

### Project Structure
- `main.py`: Entry point and user interface
- `fcfs.py`: First Come First Serve implementation
- `sjf.py`: Shortest Job First implementation
- `srtf.py`: Shortest Remaining Time First implementation
- `rr.py`: Round Robin implementation

### Key Components
- Process Management
- Scheduling Algorithms
- Performance Metrics Calculation
- Gantt Chart Generation

## Sample Output

```
Gantt_Chart:
+------+------+------+------+------+
|  P1  |  I   |  P2  |  P3  |  P4  |
+------+------+------+------+------+
0      2      4      8      12     15

Average Turnaround Time: 8.25 ms
Average Response Time: 4.75 ms
Average Waiting Time: 3.50 ms
Overall CPU Usage: 85.33%
```

## Limitations
- Maximum 5 processes
- Process IDs must be 1-5
- Non-negative arrival and burst times
- Single processor simulation

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Acknowledgments

- Based on operating systems scheduling algorithms
- Created for COMP 20103 Operating Systems course
- Inspired by real-world OS process management systems
