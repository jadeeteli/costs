import sys

path = "src/App.jsx"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

original = src
fixes = [
    (
        'con más de 12 meses y menos de 18 meses de edad":{"category":"INSCRIPCIONES ACCESS LBO/RBR","prices":{"Member":[{"year":2025,"with_vat":33,"no_vat":27.27},{"year":2026,"with_vat":36,"no_vat":29.75}],"User":[{"year":2025,"with_vat":45,"no_vat":37.19},{"year":2026,"with_vat":51,"no_vat":42.15}],"Canine_Collaborator":[]}}',
        'con más de 12 meses y menos de 18 meses de edad":{"category":"INSCRIPCIONES ACCESS LBO/RBR","prices":{"Member":[{"year":2025,"with_vat":33,"no_vat":27.27},{"year":2026,"with_vat":36,"no_vat":29.75}],"User":[{"year":2025,"with_vat":45,"no_vat":37.19},{"year":2026,"with_vat":51,"no_vat":42.15}],"Canine_Collaborator":[{"year":2026,"with_vat":30.86,"no_vat":25.5}]}}',
    ),
    (
        'con más de 9 meses y menos de 12 meses de edad":{"category":"INSCRIPCIONES ACCESS LBO/RBR","prices":{"Member":[{"year":2025,"with_vat":22,"no_vat":18.18},{"year":2026,"with_vat":24,"no_vat":19.83}],"User":[{"year":2025,"with_vat":30,"no_vat":24.79},{"year":2026,"with_vat":34,"no_vat":28.1}],"Canine_Collaborator":[]}}',
        'con más de 9 meses y menos de 12 meses de edad":{"category":"INSCRIPCIONES ACCESS LBO/RBR","prices":{"Member":[{"year":2025,"with_vat":22,"no_vat":18.18},{"year":2026,"with_vat":24,"no_vat":19.83}],"User":[{"year":2025,"with_vat":30,"no_vat":24.79},{"year":2026,"with_vat":34,"no_vat":28.1}],"Canine_Collaborator":[{"year":2026,"with_vat":20.57,"no_vat":17}]}}',
    ),
    (
        '"with_vat":12,"no_vat":9.92}],"User":[{"year":2025,"with_vat":15,"no_vat":12.4},{"year":2026,"with_vat":17,"no_vat":14.05}],"Canine_Collaborator":[]}}',
        '"with_vat":12,"no_vat":9.92}],"User":[{"year":2025,"with_vat":15,"no_vat":12.4},{"year":2026,"with_vat":17,"no_vat":14.05}],"Canine_Collaborator":[{"year":2026,"with_vat":10.29,"no_vat":8.5}]}}',
    ),
    (
        'con más de 12 meses y menos de 18 meses de edad":{"category":"INSCRIPCIONES PREMIUM LOE/RRC","prices":{"Member":[{"year":2025,"with_vat":50.7,"no_vat":41.9},{"year":2026,"with_vat":54,"no_vat":44.63}],"User":[{"year":2025,"with_vat":61.5,"no_vat":50.83},{"year":2026,"with_vat":66,"no_vat":54.55}],"Canine_Collaborator":[]}}',
        'con más de 12 meses y menos de 18 meses de edad":{"category":"INSCRIPCIONES PREMIUM LOE/RRC","prices":{"Member":[{"year":2025,"with_vat":50.7,"no_vat":41.9},{"year":2026,"with_vat":54,"no_vat":44.63}],"User":[{"year":2025,"with_vat":61.5,"no_vat":50.83},{"year":2026,"with_vat":66,"no_vat":54.55}],"Canine_Collaborator":[{"year":2026,"with_vat":39.93,"no_vat":33}]}}',
    ),
    (
        'con más de 6 meses y menos de 9 meses de edad":{"category":"INSCRIPCIONES PREMIUM LOE/RRC","prices":{"Member":[{"year":2025,"with_vat":16.9,"no_vat":13.97},{"year":2026,"with_vat":18,"no_vat":14.88}],"User":[{"year":2025,"with_vat":20.5,"no_vat":16.94},{"year":2026,"with_vat":22,"no_vat":18.18}],"Canine_Collaborator":[]}}',
        'con más de 6 meses y menos de 9 meses de edad":{"category":"INSCRIPCIONES PREMIUM LOE/RRC","prices":{"Member":[{"year":2025,"with_vat":16.9,"no_vat":13.97},{"year":2026,"with_vat":18,"no_vat":14.88}],"User":[{"year":2025,"with_vat":20.5,"no_vat":16.94},{"year":2026,"with_vat":22,"no_vat":18.18}],"Canine_Collaborator":[{"year":2026,"with_vat":13.31,"no_vat":11}]}}',
    ),
    (
        'con más de 9 meses y menos de 12 meses de edad":{"category":"INSCRIPCIONES PREMIUM LOE/RRC","prices":{"Member":[{"year":2025,"with_vat":33.8,"no_vat":27.93},{"year":2026,"with_vat":36,"no_vat":29.75}],"User":[{"year":2025,"with_vat":41,"no_vat":33.88},{"year":2026,"with_vat":44,"no_vat":36.36}],"Canine_Collaborator":[]}}',
        'con más de 9 meses y menos de 12 meses de edad":{"category":"INSCRIPCIONES PREMIUM LOE/RRC","prices":{"Member":[{"year":2025,"with_vat":33.8,"no_vat":27.93},{"year":2026,"with_vat":36,"no_vat":29.75}],"User":[{"year":2025,"with_vat":41,"no_vat":33.88},{"year":2026,"with_vat":44,"no_vat":36.36}],"Canine_Collaborator":[{"year":2026,"with_vat":26.62,"no_vat":22}]}}',
    ),
]

count = 0
for old, new in fixes:
    if old in src:
        src = src.replace(old, new, 1)
        count += 1
    else:
        print("NOT FOUND:", old[:80])

if src != original:
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)

print(f"Applied {count} of {len(fixes)} fixes")
