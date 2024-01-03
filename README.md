# Aurora

## Overview
Aurora is an emulator designed for analyzing BRAM write distribution on FPGA. It provides a framework for simulating and visualizing the behavior of BRAMs (Block RAMs) under different conditions and configurations.

## Features
- Emulation of BRAM write distribution in FPGA circuits.
- Support for multiple strategies and configurations.
- Visualization of BRAM usage and write distribution.

## Getting Started
### Prerequisites
- Python 3.x
- Required Python libraries: numpy, seaborn, matplotlib

### Installation
Clone the repository:
```bash
git clone https://github.com/HaoZhang-Ethan/Aurora.git
```
Install the required Python libraries:
```bash
pip install numpy seaborn matplotlib
```

### Usage
Run the main script to start the emulator:
```bash
python main.py
```

## File Structure
```
Aurora/
│
├── main.py               - Main script to start the emulator.
├── read_activate.py      - Module for reading and processing activation data.
├── read_circuit.py       - Module for parsing circuit information.
├── simulator.py          - Core simulation logic for BRAM emulation.
├── type.py               - Defines types and constants used in the project.
└── LICENSE               - The MIT License for the project.
```

## Modules Description
- `main.py`: Orchestrates the emulation process, integrating various modules.
- `read_activate.py`: Handles the reading of activation data for the simulation.
- `read_circuit.py`: Parses and processes circuit information for emulation.
- `simulator.py`: Contains the simulation algorithms for BRAM write distribution.
- `type.py`: Defines the data structures and constants used across the project.

## Contributing
Contributions to Aurora are welcome. Please read the contribution guidelines before submitting a pull request.

## License
This project is licensed under the [MIT License](https://github.com/HaoZhang-Ethan/Aurora/blob/main/LICENSE).
