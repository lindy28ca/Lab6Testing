"""Genera el informe editable de entrega usando los scripts reales del proyecto."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from xml.sax.saxutils import escape
import html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Entrega"
OUT.mkdir(exist_ok=True)

exercises = [
    (
        "Validación del sistema de vida", "HealthAssertion",
        "Assert.AreNotEqual(0, health).",
        "Seleccioné AreNotEqual porque la condición de este ejercicio es que la vida sea distinta de cero. Con health = 100 se cumple; al cambiarla a 0, la aserción falla. Esta comparación comprueba específicamente el valor cero; no establece un rango de vida ni rechaza valores negativos.",
        "Puede detectar que un personaje continúe en un estado que requiere vida cuando su vida ya llegó a cero, por ejemplo, si no se activó la lógica de muerte.",
        "Player con Health = 100, durante Play Mode, y Console sin fallos de esta validación.",
        "Player con Health = 0, durante Play Mode, y el fallo de HealthAssertion en Console."
    ),
    (
        "Validación de un GameObject activo", "ActiveObjectAssertion",
        "Assert.IsTrue(target.activeInHierarchy).",
        "Seleccioné IsTrue porque el objeto debe estar activo. Utilicé activeInHierarchy, que indica si está activo realmente en la escena y considera el estado de sus padres. A diferencia de activeSelf, también detecta que un padre esté desactivado. Se añadió IsNotNull como validación auxiliar para comprobar que target esté asignado.",
        "Puede detectar la desactivación accidental de un objeto esencial, que impediría ejecutar sus componentes y afectaría el funcionamiento del videojuego.",
        "CriticalObject activo y GameManager con Target asignado a CriticalObject, durante Play Mode; Console sin fallos.",
        "CriticalObject desactivado durante Play Mode y el fallo de ActiveObjectAssertion en Console."
    ),
    (
        "Validación de posición", "PositionAssertion",
        "Assert.AreApproximatelyEqual(0f, coordenada, 0.001f), para X, Y y Z.",
        "Seleccioné AreApproximatelyEqual para comprobar que cada coordenada de transform.position esté cerca de cero, con tolerancia de 0.001 unidades. Los float pueden acumular pequeñas diferencias por representación y redondeo; una comparación aproximada evita fallos por variaciones mínimas. En (0, 0, 0) se cumple la condición; en (2, 0, 0) falla la comparación de X.",
        "Puede detectar que un objeto fijo o un punto de referencia se desplace por un cálculo incorrecto, una animación o un script de movimiento.",
        "CenterObject en Position (0, 0, 0), durante Play Mode; Console sin fallos.",
        "CenterObject en Position (2, 0, 0), durante Play Mode, y el fallo de PositionAssertion en Console."
    ),
    (
        "Validación del Tag del jugador", "PlayerTagAssertion",
        'Assert.AreEqual("Player", currentTag).',
        'Seleccioné AreEqual porque se necesita igualdad exacta entre dos cadenas. El valor esperado es "Player"; el valor obtenido en el caso correcto es "Player" y en el caso incorrecto es "Untagged". La propiedad gameObject.tag permite obtener el Tag actual. Al no coincidir las cadenas, la aserción falla.',
        "Puede detectar un Tag incorrecto que impida reconocer al jugador en búsquedas por etiqueta, colisiones, enemigos o zonas de activación.",
        "Player con Tag Player, durante Play Mode; Console sin fallos.",
        "Player con Tag Untagged, después de ejecutar nuevamente, y el fallo de PlayerTagAssertion en Console."
    ),
    (
        "Validación de una referencia", "ReferenceAssertion",
        "Assert.IsNull(myClassReference).",
        "Seleccioné IsNull porque el estado esperado inicialmente es una referencia sin instancia. Al crear un objeto mediante new MyClass(), la referencia deja de ser null y la aserción falla. El selector Create Reference On Start permite reproducir las dos variantes del PDF: desmarcado no crea la instancia; marcado ejecuta CreateReference() desde Start. El estado de la referencia se muestra en el Inspector durante Play Mode.",
        "Puede detectar una inicialización prematura o inesperada de una referencia que debía permanecer vacía hasta una etapa determinada del videojuego. En este ejercicio, tener una instancia es el caso incorrecto.",
        "ReferenceValidator con Create Reference On Start desmarcado, myClassReference: null y Console sin fallos, durante Play Mode.",
        "ReferenceValidator con Create Reference On Start marcado antes de iniciar, estado no null durante Play Mode y fallo de ReferenceAssertion en Console."
    ),
]

parts = []
def add(kind, text=""):
    parts.append((kind, text))

add("title", "Laboratorio N.° 06")
add("subtitle", "Testing de Videojuegos · 6 - C26 - Sección A")
add("p", "Sistema de Trabajo de Testing 1 — Validaciones mediante Assertions en Unity")
add("p", "Docente: Bestard Aroche, Yunior")
for i, (title, script, assertion, reason, bug, good, bad) in enumerate(exercises, 1):
    if i > 1:
        add("break")
    add("h1", f"Ejercicio {i} — {title}")
    add("h2", "Assert seleccionado y justificación")
    add("p", assertion)
    add("p", reason)
    add("h2", "Error del videojuego que podría detectar")
    add("p", bug)
    add("h2", f"Script completado: {script}.cs")
    source = (ROOT / "Assets" / "Scripts" / f"{script}.cs").read_text(encoding="utf-8")
    add("code", source.rstrip())
    add("h2", "Evidencias")
    add("p", "Condición correcta: " + good)
    add("placeholder", f"[INSERTAR CAPTURA {i}A — CONDICIÓN CORRECTA]")
    add("p", "Condición incorrecta provocada: " + bad)
    add("placeholder", f"[INSERTAR CAPTURA {i}B — CONDICIÓN INCORRECTA]")

add("break")
add("h1", "Conclusiones")
add("p", "Las aserciones permiten comprobar condiciones esperadas durante la ejecución y localizar estados que podrían causar errores en el videojuego. Cada método debe elegirse según lo que se valida: desigualdad para la vida distinta de cero, una condición booleana para el objeto activo, aproximación para las coordenadas, igualdad para el Tag y nulidad para la referencia.")
add("p", "Provocar intencionalmente una condición incorrecta permite comprobar que la validación detecta el cambio. Estas comprobaciones ayudan durante el desarrollo, pero no reemplazan la lógica del videojuego ni corrigen por sí mismas el estado detectado.")

# Versión Markdown.
md = []
for kind, text in parts:
    if kind in ("title", "h1"):
        md.append("# " + text)
    elif kind in ("h2", "subtitle"):
        md.append("## " + text)
    elif kind == "code":
        md.append("```csharp\n" + text + "\n```")
    elif kind == "break":
        md.append("---")
    elif kind == "placeholder":
        md.append("**" + text + "**")
    else:
        md.append(text)
(OUT / "Informe_Lab06.md").write_text("\n\n".join(md) + "\n", encoding="utf-8")

# Versión HTML para abrir en navegador o Word.
body = []
for kind, text in parts:
    safe = html.escape(text)
    if kind in ("title", "h1"):
        body.append(f"<h1>{safe}</h1>")
    elif kind in ("h2", "subtitle"):
        body.append(f"<h2>{safe}</h2>")
    elif kind == "code":
        body.append(f"<pre>{safe}</pre>")
    elif kind == "break":
        body.append('<div class="page-break"></div>')
    elif kind == "placeholder":
        body.append(f'<div class="capture">{safe}</div>')
    else:
        body.append(f"<p>{safe}</p>")
(OUT / "Informe_Lab06.html").write_text(
    '<!doctype html><html lang="es"><meta charset="utf-8"><title>Laboratorio 06</title>'
    '<style>body{font:11pt Calibri,Arial,sans-serif;max-width:900px;margin:40px auto;color:#202b35}'
    'h1{font-size:20pt;color:#187996}h2{font-size:13pt;color:#187996}'
    'pre{font:9pt Consolas,monospace;background:#f4f6f8;padding:12px;white-space:pre-wrap;overflow-wrap:anywhere}'
    '.capture{border:1px dashed #187996;padding:24px;margin:12px 0;color:#187996}'
    '@media print{.page-break{break-before:page}body{margin:0}}</style><body>'
    + "\n".join(body) + '</body></html>', encoding="utf-8")

# Documento Word editable (OOXML, sin dependencias externas).
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
def paragraph(text, style="Normal"):
    return ('<w:p><w:pPr><w:pStyle w:val="' + style + '"/></w:pPr>'
            '<w:r><w:t xml:space="preserve">' + escape(text) + '</w:t></w:r></w:p>')

doc = []
styles = {"title": "Title", "subtitle": "Subtitle", "h1": "Heading1", "h2": "Heading2", "placeholder": "Capture"}
for kind, text in parts:
    if kind == "break":
        doc.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
    elif kind == "code":
        doc.extend(paragraph(line, "Code") for line in text.splitlines())
    else:
        doc.append(paragraph(text, styles.get(kind, "Normal")))

document = (f'<?xml version="1.0" encoding="UTF-8"?><w:document xmlns:w="{W}"><w:body>'
            + ''.join(doc)
            + '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="900" w:right="900" w:bottom="900" w:left="900"/></w:sectPr></w:body></w:document>')
style_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<w:styles xmlns:w="{W}">
<w:docDefaults><w:rPrDefault><w:rPr><w:rFonts w:ascii="Calibri" w:hAnsi="Calibri"/><w:sz w:val="22"/><w:lang w:val="es-PE"/></w:rPr></w:rPrDefault><w:pPrDefault><w:pPr><w:spacing w:after="100"/></w:pPr></w:pPrDefault></w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:rPr><w:b/><w:color w:val="187996"/><w:sz w:val="40"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Subtitle"><w:name w:val="Subtitle"/><w:rPr><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:pPr><w:keepNext/><w:spacing w:before="180" w:after="120"/></w:pPr><w:rPr><w:b/><w:color w:val="187996"/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:pPr><w:keepNext/><w:spacing w:before="120" w:after="80"/></w:pPr><w:rPr><w:b/><w:color w:val="187996"/><w:sz w:val="24"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:pPr><w:spacing w:after="0" w:line="200" w:lineRule="exact"/><w:shd w:fill="F4F6F8"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="17"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Capture"><w:name w:val="Capture"/><w:pPr><w:spacing w:before="160" w:after="240"/><w:pBdr><w:bottom w:val="dashed" w:sz="6" w:color="187996"/></w:pBdr></w:pPr><w:rPr><w:b/><w:color w:val="187996"/></w:rPr></w:style>
</w:styles>'''
with ZipFile(OUT / "Informe_Lab06.docx", "w", ZIP_DEFLATED) as z:
    z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/><Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/></Types>')
    z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>')
    z.writestr("word/document.xml", document)
    z.writestr("word/styles.xml", style_xml)
    z.writestr("word/_rels/document.xml.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/></Relationships>')

print("Informe generado: Entrega/Informe_Lab06.docx (también HTML y Markdown).")
