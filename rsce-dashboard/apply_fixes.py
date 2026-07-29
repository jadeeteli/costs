#!/usr/bin/env python3
import sys
import re

if len(sys.argv) != 2:
    print("Usage: python3 apply_fixes.py <path-to-App.jsx>")
    sys.exit(1)

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

original = src
changes = []

hidden_marker = '"SIN DESCRIPCIÓN (revisar origen - tasa fija 0,25€)",'
new_entry = '"IMPRESO ALTA DE CAMADA (PERROS DE RAZA)",'
if hidden_marker in src and new_entry not in src:
    src = src.replace(hidden_marker, hidden_marker + "\n  " + new_entry, 1)
    changes.append("Added IMPRESO ALTA DE CAMADA (PERROS DE RAZA) to HIDDEN_PRODUCTS")
elif new_entry in src:
    changes.append("HIDDEN_PRODUCTS already contains IMPRESO ALTA DE CAMADA (PERROS DE RAZA) -- skipped")
else:
    changes.append("WARNING: could not find HIDDEN_PRODUCTS anchor line -- fix 1 not applied, check manually")

camada_fixes = [
    ('"INSCRIPCIÓN CACHORRO PREMIUM LOE/RRC":{"category":"INSCRIPCIONES PREMIUM LOE/RRC"',
     '"Canine_Collaborator":[]',
     '"Canine_Collaborator":[{"year":2026,"with_vat":13.31,"no_vat":11}]'),
    ('"INSCRIPCIÓN CACHORRO ACCESS LBO/RBR":{"category":"INSCRIPCIONES ACCESS LBO/RBR"',
     '"Canine_Collaborator":[]',
     '"Canine_Collaborator":[{"year":2026,"with_vat":10.29,"no_vat":8.5}]'),
    ('"RECARGO POR INSCRIPCIÓN DE CACHORRO PREMIUM LOE/RRC con más de 12 meses y menos de 18 meses de edad"',
     '"Canine_Collaborator":[]',
     '"Canine_Collaborator":[{"year":2026,"with_vat":39.93,"no_vat":33}]'),
    ('"RECARGO POR INSCRIPCIÓN DE CACHORRO PREMIUM LOE/RRC con más de 6 meses y menos de 9 meses de edad"',
     '"Canine_Collaborator":[]',
     '"Canine_Collaborator":[{"year":2026,"with_vat":13.31,"no_vat":11}]'),
    ('"RECARGO POR INSCRIPCIÓN DE CACHORRO PREMIUM LOE/RRC con más de 9 meses y menos de 12 meses de edad"',
     '"Canine_Collaborator":[]',
     '"Canine_Collaborator":[{"year":2026,"with_vat":26.62,"no_vat":22}]'),
    ('"RECARGO POR INSCRIPCIÓN DE CACHORRO ACCESS LBO/RBR con más de 6 meses y menos de 9 meses de edad"',
     '"Canine_Collaborator":[]',
     '"Canine_Collaborator":[{"year":2026,"with_vat":10.29,"no_vat":8.5}]'),
    ('"RECARGO POR INSCRIPCIÓN DE CACHORRO ACCESS LBO/RBR con más de 12 meses y menos de 18 meses de edad"',
     '"Canine_Collaborator":[]',
     '"Canine_Collaborator":[{"year":2026,"with_vat":30.86,"no_vat":25.5}]'),
    ('"RECARGO POR INSCRIPCIÓN DE CACHORRO ACCESS LBO/RBR con más de 9 meses y menos de 12 meses de edad"',
     '"Canine_Collaborator":[]',
     '"Canine_Collaborator":[{"year":2026,"with_vat":20.57,"no_vat":17}]'),
]

for anchor, old_val, new_val in camada_fixes:
    idx = src.find(anchor)
    if idx == -1:
        changes.append(f"WARNING: could not find product block for anchor starting '{anchor[:60]}...' -- skipped")
        continue
    window = src[idx:idx+2000]
    rel = window.find(old_val)
    if rel == -1:
        changes.append(f"WARNING: '{anchor[:60]}...' found but no empty Canine_Collaborator nearby -- may already be filled")
        continue
    abs_pos = idx + rel
    src = src[:abs_pos] + new_val + src[abs_pos + len(old_val):]
    changes.append(f"Filled 2026 Canine_Collaborator price for: {anchor[:70]}...")

append_fixes = [
    ('"INSCRIPCIÓN CACHORRO DE RAZAS ESPAÑOLAS BONIFICADAS"',
     '{"year":2024,"with_vat":5.6,"no_vat":4.63}]}}',
     '{"year":2024,"with_vat":5.6,"no_vat":4.63},{"year":2026,"with_vat":5.89,"no_vat":4.87}]}}'),
    ('"INSCRIPCIÓN CACHORRO EN EL REGISTRO DE GRUPOS ÉTNICOS"',
     '"Canine_Collaborator":[{"year":2024,"with_vat":5.6,"no_vat":4.63}]',
     '"Canine_Collaborator":[{"year":2024,"with_vat":5.6,"no_vat":4.63},{"year":2026,"with_vat":6.66,"no_vat":5.5}]'),
]

for anchor, old_val, new_val in append_fixes:
    idx = src.find(anchor)
    if idx == -1:
        changes.append(f"WARNING: could not find anchor '{anchor}' -- skipped")
        continue
    window = src[idx:idx+2000]
    rel = window.find(old_val)
    if rel == -1:
        changes.append(f"WARNING: '{anchor}' found but expected pattern not present nearby -- check manually")
        continue
    abs_pos = idx + rel
    src = src[:abs_pos] + new_val + src[abs_pos + len(old_val):]
    changes.append(f"Appended 2026 Canine_Collaborator price for: {anchor}")

m = re.search(r"const MANUAL_CODE_OVERRIDES = \{(.*?)\n\};", src, re.DOTALL)
if m:
    body = m.group(1)
    keys = re.findall(r'"((?:[^"\\]|\\.)*)"\s*:', body)
    seen = {}
    dupes = set()
    for k in keys:
        if k in seen:
            dupes.add(k)
        seen[k] = True
    if dupes:
        changes.append(f"NOTE: MANUAL_CODE_OVERRIDES has {len(dupes)} duplicate key(s):")
        for d in sorted(dupes):
            changes.append(f"    - {d}")
else:
    changes.append("WARNING: could not locate MANUAL_CODE_OVERRIDES block")

if src != original:
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
    print(f"Wrote changes to {path}\n")
else:
    print("No changes were made to the file.\n")

print("Summary:")
for c in changes:
    print(" -", c)
