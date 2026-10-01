# Laboratorio 06 — Solo falta incorporar las capturas

## Archivos

- **Informe_Lab06.docx**: abre este archivo en Word y sustituye los diez marcadores `[INSERTAR CAPTURA ...]` por tus imágenes. Ya contiene los scripts, los métodos seleccionados, las explicaciones y las conclusiones.
- `Informe_Lab06.html` y `Informe_Lab06.md`: versiones alternativas del mismo informe.
- Escena: `Assets/Scenes/Lab06Assertions.unity`.
- Scripts: `Assets/Scripts/`.

## Preparación

1. Abre el proyecto en Unity 6000.3.10f1 y espera a que termine de compilar.
2. Abre **Laboratorio 06 > Abrir escena preparada**. También puedes abrir la escena desde `Assets/Scenes`.
3. Abre **Window > General > Console** y deja visibles el Inspector y Console. Activa **Collapse**, deja visible el filtro de errores/aserciones y desactiva **Error Pause** para que la ejecución no se pause al provocar un fallo.
4. Para cada captura correcta, pulsa **Clear** en Console. Las aserciones correctas no generan mensajes: la evidencia es Play Mode activo, el estado correcto en el Inspector y la ausencia de fallos.
5. Para cada captura incorrecta, muestra el valor alterado y selecciona el fallo de aserción en Console para que se lea el mensaje y el script. No cambies varios casos a la vez.

## Las diez capturas

| Captura | Condición y pasos |
|---|---|
| **1A** | Entra en Play. Selecciona `Player`: `Health = 100`. Captura Inspector y Console sin fallos. |
| **1B** | Sin salir de Play, cambia `Health` a `0`. Captura el fallo de `HealthAssertion`. Después detén Play: la vida vuelve a 100. |
| **2A** | Limpia Console y entra en Play. Selecciona `GameManager`: `Target = CriticalObject`. Muestra que `CriticalObject` está activo. |
| **2B** | En Play, selecciona `CriticalObject` y desmarca la casilla de activación junto a su nombre (no desactives GameManager). Captura el fallo de `ActiveObjectAssertion`. Detén Play. |
| **3A** | Limpia Console, entra en Play y selecciona `CenterObject`: `Transform > Position = (0, 0, 0)`. |
| **3B** | En Play, cambia Position a `(2, 0, 0)`. Captura el fallo de la coordenada X en `PositionAssertion`. Detén Play. |
| **4A** | Fuera de Play, comprueba que `Player` tenga `Tag = Player`. Limpia Console, entra en Play y captura el estado correcto. Detén Play. |
| **4B** | Fuera de Play, cambia el Tag de `Player` a `Untagged`. Limpia Console y vuelve a entrar en Play. Captura el fallo de `PlayerTagAssertion`. Detén Play y restaura el Tag `Player`. |
| **5A** | Fuera de Play, selecciona `ReferenceValidator` y deja **Create Reference On Start** desmarcado. Limpia Console, entra en Play y captura el estado `myClassReference: null (sin instancia)` del Inspector. Detén Play. |
| **5B** | Fuera de Play, marca **Create Reference On Start**. Limpia Console y entra en Play. Captura `Instancia de MyClass (no null)` y el fallo de `ReferenceAssertion`. Detén Play y desmarca el selector. |

El selector del ejercicio 5 se consulta en `Start()`: cambiarlo mientras ya estás en Play no recrea automáticamente la referencia. Marcándolo antes de Play se reproduce la adición temporal de `Start() { CreateReference(); }` que solicita el PDF.

## Entrega

Inserta las capturas en `Informe_Lab06.docx` y guarda el documento. Si te solicitan PDF, usa **Archivo > Exportar > Crear PDF** en Word. Mantén los scripts del proyecto como parte de la entrega si los solicitan por separado.

La carpeta `Entrega` contiene también `Verificacion_Unity.txt`, generado por una comprobación de los casos correctos e incorrectos con los scripts reales. Puedes repetirla, fuera de Play, desde **Laboratorio 06 > Verificar validaciones**.
