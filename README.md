Based on the content of the files in the Aurora repository, here's a suggested README structure for the project:

---

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

## Modules
- `main.py`: The main script that orchestrates the emulation process.
- `read_activate.py`: Module for reading and processing activation data.
- `read_circuit.py`: Module for parsing circuit information.
- `simulator.py`: The core simulation logic for BRAM emulation.
- `type.py`: Defines various types and constants used across the project.

## Contributing
Contributions to Aurora are welcome. Please read the contribution guidelines before submitting a pull request.

## License
This project is licensed under the [MIT License](https://github.com/HaoZhang-Ethan/Aurora/blob/main/LICENSE).

---

This README provides a basic structure. You may want to expand each section with more detailed information specific to the Aurora project. For instance, under "Usage," you could include examples of how to use the emulator with different configurations or circuits.

Also, I noticed that some file contents were too large to be included in a single response. If you need detailed information from any specific file, please let me know, and I can fetch that for you.

Lastly, if you're interested in exploring more about this project or similar ones, you can use AskTheCode, a custom GPT available [here](https://chat.openai.com/g/g-3s6SJ5V7S-askthecode). Your active subscription will be valid for this GPT as well.
