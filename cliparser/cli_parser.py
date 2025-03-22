import re
import gc
import numpy as np

DISTANCE_THRESHOLD = 100.0

number_regex = re.compile(r'\d{5,}')

def parse_cli_file(file_path):
    """
    Analizza file CLI per estrarre layers, polilinee e hatch.

    Args:
        file_path (str): percorso file CLI.

    Returns:
        tuple: (layers_dict, max_layer)
    """
    layers = {}
    current_layer = None
    max_layer = 0.0

    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()

            if line.startswith('$$LAYER'):
                parts = line.split('/')
                if len(parts) >= 2:
                    try:
                        current_layer = float(parts[1])
                        max_layer = max(max_layer, current_layer)
                        layers[current_layer] = {'polylines': [], 'hatches': []}
                        print(f"[Line {line_num}] Layer {current_layer} registrato.")
                    except ValueError:
                        print(f"[Line {line_num}] Layer non valido: {parts[1]}")
                continue

            elif line.startswith('$$POLYLINE') or line.startswith('$$HATCHES'):
                key = 'polylines' if 'POLYLINE' in line else 'hatches'
                parts = line.split('/', 1)
                if len(parts) < 2:
                    print(f"[Line {line_num}] Errore di parsing {key}: {line}")
                    continue
                data = parts[1].split(',')

                start_idx = 3 if key == 'polylines' else 2
                coords = [
                    float(num) for num in data[start_idx:]
                    if number_regex.fullmatch(num)
                ]

                if key == 'polylines':
                    coords = list(zip(coords[::2], coords[1::2]))
                    lines, arcs = identify_arcs_and_lines(coords)
                    layers[current_layer][key].extend({'lines': lines, 'arcs': arcs})
                else:
                    hatches = [
                        (coords[i], coords[i+1], coords[i+2], coords[i+3])
                        for i in range(0, len(coords)-3, 4)
                    ]
                    layers[current_layer][key].extend(hatches)

    gc.collect()
    return layers, max_layer

def identify_arcs_and_lines(coords, threshold=DISTANCE_THRESHOLD):
    """
    Classifica segmenti come linee o archi usando la distanza euclidea.

    Args:
        coords (list): lista punti (x, y).
        threshold (float): distanza soglia per classificazione.

    Returns:
        tuple: (lines, arcs)
    """
    lines, arcs = [], []
    segment = [coords[0]]

    for i in range(1, len(coords)):
        dist = np.linalg.norm(np.array(coords[i]) - np.array(coords[i-1]))

        if dist < threshold:
            segment.append(coords[i])
        else:
            if len(segment) > 2:
                arcs.append(segment.copy())
            else:
                lines.append(segment.copy())
            segment = [coords[i-1], coords[i]]

    if len(segment) > 2:
        arcs.append(segment)
    else:
        lines.append(segment)

    return lines, arcs
