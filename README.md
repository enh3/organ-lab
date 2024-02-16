# OrganLab

## Overview
OrganLab is a real-time synthesis program built with the pyo library. Inspired by the pipe organ, OrganLab allows you to define various "stops" with varied timbral profiles using additive and subtractive synthesis. These stops can then be transformed in different ways, such as imploding or exploding the spectrum, applying frequency modulation, or treating the harmonic and transient content independently. This project is part of my master's research-creation project at the Université de Montréal, and represents a work in progress. Contributions are welcome.

## Features
- **Pipe Organ Synthesis:** Use `emulations.py` to define your palette of stops.
- **Mutation Capabilities:** Expand `mutations.py` to alter stops in virtually limitless ways.
- **Dynamic Composition:** Customize `midi_nav.py` or `osc_nav.py`, to navigate through different states and automations.
- **MIDI & OSC Control:** Customize and control the software via OSC or MIDI.
- **Minimal GUI:** A minimal GUI for initial interaction and operation.
- **Expandable:** Designed for ongoing expansion and customization of stops, mutations, and patterns.

## Getting Started
### Prerequisites
- Python 3.x
- Pyo library
- MIDI/OSC input device (optional for enhanced control)

### Installation
Clone the repository and install the required Python packages:

git clone https://github.com/enh3/organ-lab.git
pip install pyo

### Usage
- **Editing Source Files:** Currently, OrganLab is operated by directly editing the source files. See `emulations.py`, `mutations.py`, and `patterns.py` for composition and synthesis manipulation.
- **GUI Operation:** Access the GUI for basic interactions such as adjusting the volume, stepping through the state tree and testing through an on screen keyboard. 
- **Control via MIDI or OSC:** For detailed instructions on controlling OrganLab using MIDI or OSC commands, please refer to the MIDI/OSC Control section below.

#### MIDI/OSC Control
- **OSC Commands:**
  - `/continue`: Advance to the next state (value of 1).
  - `/return`: Decrement to the previous (value of 1).
  - `/volume`: Control the volume with a floating point value between 0 and 1.
- **MIDI Commands:**
  - Use control changes on channel one with a value of 20, and a key representing the state you want to jump to, or noteon messages from C3 onwards (chromatically) on channel 7, to navigate states.

### Custom XML for l'église Saint-Édouard
A custom `.xml` file is available for integrating OrganLab with organ emulators like GrandOrgue or Organteq, specifically tailored for the organ at l'église Saint-Édouard. Please reach out if you'd like a copy.

## Future Directions
- **Automatic Emulation Creation:** Integrate audio file analysis (possibly using Essentia) for auto-creation of emulations.
- **Project File Customization:** Allow users to define their projects through a `.orglab` file without source code modifications.
- **Enhanced GUI:** Develop a more comprehensive GUI to support the graphically inclined.

## Contributing
Though this program has been so far based around my own creative project, I'd like it to eventually be useful for other people as well. If you'd like to contribute, throw me an email at net@kjel.ca and I'd be happy to help you sift through the codebase. 

## License
This project is licensed under LGPL 3.0 - see the LICENSE file for details.

## Acknowledgments
- Olivier Bélanger for the Pyo library
- The Université de Montréal and the OICRM for supporting this research project
