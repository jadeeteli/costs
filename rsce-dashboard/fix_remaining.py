path = "src/App.jsx"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

original = src
report = []

def append_within_window(anchor, old_tail, new_tail, label):
    global src
    idx = src.find(anchor)
    if idx == -1:
        report.append(f"NOT FOUND anchor: {label}")
        return
    window = src[idx:idx+600]
    rel = window.find(old_tail)
    if rel == -1:
        report.append(f"anchor found but tail pattern missing: {label} -- printing next 600 chars for review:")
        report.append(window)
        return
    abs_pos = idx + rel
    src = src[:abs_pos] + new_tail + src[abs_pos+len(old_tail):]
    report.append(f"FIXED: {label}")

append_within_window(
    'DE RAZAS ESPAÑOLAS BONIFICADAS":{"category":"OTRAS INSCRIPCIONES"',
    '{"year":2024,"with_vat":5.6,"no_vat":4.63}]}}',
    '{"year":2024,"with_vat":5.6,"no_vat":4.63},{"year":2026,"with_vat":5.89,"no_vat":4.87}]}}',
    "INSCRIPCIÓN CACHORRO DE RAZAS ESPAÑOLAS BONIFICADAS"
)

append_within_window(
    'EN EL REGISTRO DE GRUPOS ÉTNICOS":{"category":"OTRAS INSCRIPCIONES"',
    '{"year":2024,"with_vat":5.6,"no_vat":4.63}]}}',
    '{"year":2024,"with_vat":5.6,"no_vat":4.63},{"year":2026,"with_vat":6.66,"no_vat":5.5}]}}',
    "INSCRIPCIÓN CACHORRO EN EL REGISTRO DE GRUPOS ÉTNICOS"
)

if src != original:
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)

print("\n".join(report))
