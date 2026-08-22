import os

found = False
for root, dirs, files in os.walk('dataforge/cognitive'):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                content = fp.read()
                if 'genelindeki uygulamaları' in content or 'değerlendiriyorum' in content:
                    print(f'FOUND IN: {p}')
                    found = True

if not found:
    print("TAMAMEN TEMİZ: Hiçbir statik cümle kalıntısı bulunamadı!")
