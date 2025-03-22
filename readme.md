




  CLIparser README

CLIparser is a Python library for parsing `.CLI` (Common Layer Interface) files, 
used in additive manufacturing (3D printing). It extracts detailed information 
about layers, polylines, and hatches.

-------------------------
  Introduction to the CLI Format
-------------------------

The CLI format (Common Layer Interface) describes a 3D model through horizontal 
sections ("layers"), each typically containing:
- POLYLINE: outlines or profiles, represented by a series of XY coordinates.
- HATCHES: internal fill segments (linear strokes), each defined by start and end 
  coordinates.

Example of a CLI file structure:
$$LAYER/1
$$POLYLINE/...
$$HATCHES/...

For more details, please visit:
  https://www.hmilch.net/downloads/cli_format.html
We extend our thanks for their valuable information on the CLI format.

-------------------------
  Installation
-------------------------

At the moment, you can clone this repository or download the source code.


-------------------------
  Usage Example
-------------------------

Sample Python code:

    from cliparser.cli_parser import parse_cli_file

    layers, max_layer = parse_cli_file("path/to/file.cli")

    print("Max layer:", max_layer)
    for layer_idx, layer_data in layers.items():
        print("> Layer", layer_idx, "with", len(layer_data["polylines"]), "polylines and", len(layer_data["hatches"]), "hatches")

Note: For arc definition, CLIparser uses the **Euclidean distance** as the 
criterion to distinguish segments that belong to the same path from those forming a new one.

-------------------------
  License
-------------------------

This project is released under the GNU General Public License v3.0 (GPL v3).  
See the LICENSE file for the full text.

-------------------------
  Contributing
-------------------------

Feel free to open an issue or submit a pull request for improvements or fixes.

-------------------------
  Acknowledgments
-------------------------

- https://www.hmilch.net/downloads/cli_format.html for the detailed documentation on the CLI format.
- The open source community for ongoing inspiration.

