# Laboratorio N.° 06

## Testing de Videojuegos · 6 - C26 - Sección A

Sistema de Trabajo de Testing 1 — Validaciones mediante Assertions en Unity

Docente: Bestard Aroche, Yunior

# Ejercicio 1 — Validación del sistema de vida

## Assert seleccionado y justificación

Assert.AreNotEqual(0, health).

Seleccioné AreNotEqual porque la condición de este ejercicio es que la vida sea distinta de cero. Con health = 100 se cumple; al cambiarla a 0, la aserción falla. Esta comparación comprueba específicamente el valor cero; no establece un rango de vida ni rechaza valores negativos.

## Error del videojuego que podría detectar

Puede detectar que un personaje continúe en un estado que requiere vida cuando su vida ya llegó a cero, por ejemplo, si no se activó la lógica de muerte.

## Script completado: HealthAssertion.cs

```csharp
using UnityEngine;
using UnityEngine.Assertions;

public class HealthAssertion : MonoBehaviour
{
    public int health = 100;

    void Update()
    {
        Assert.AreNotEqual(0, health, "La vida del jugador no debe ser 0 en esta prueba.");
    }
}
```

## Evidencias

Condición correcta: Player con Health = 100, durante Play Mode, y Console sin fallos de esta validación.

**[INSERTAR CAPTURA 1A — CONDICIÓN CORRECTA]**

Condición incorrecta provocada: Player con Health = 0, durante Play Mode, y el fallo de HealthAssertion en Console.

**[INSERTAR CAPTURA 1B — CONDICIÓN INCORRECTA]**

---

# Ejercicio 2 — Validación de un GameObject activo

## Assert seleccionado y justificación

Assert.IsTrue(target.activeInHierarchy).

Seleccioné IsTrue porque el objeto debe estar activo. Utilicé activeInHierarchy, que indica si está activo realmente en la escena y considera el estado de sus padres. A diferencia de activeSelf, también detecta que un padre esté desactivado. Se añadió IsNotNull como validación auxiliar para comprobar que target esté asignado.

## Error del videojuego que podría detectar

Puede detectar la desactivación accidental de un objeto esencial, que impediría ejecutar sus componentes y afectaría el funcionamiento del videojuego.

## Script completado: ActiveObjectAssertion.cs

```csharp
using UnityEngine;
using UnityEngine.Assertions;

public class ActiveObjectAssertion : MonoBehaviour
{
    public GameObject target;

    void Update()
    {
        Assert.IsNotNull(target, "Asigna CriticalObject al campo target.");
        if (target == null)
            return;

        Assert.IsTrue(target.activeInHierarchy, "CriticalObject debe permanecer activo en la escena.");
    }
}
```

## Evidencias

Condición correcta: CriticalObject activo y GameManager con Target asignado a CriticalObject, durante Play Mode; Console sin fallos.

**[INSERTAR CAPTURA 2A — CONDICIÓN CORRECTA]**

Condición incorrecta provocada: CriticalObject desactivado durante Play Mode y el fallo de ActiveObjectAssertion en Console.

**[INSERTAR CAPTURA 2B — CONDICIÓN INCORRECTA]**

---

# Ejercicio 3 — Validación de posición

## Assert seleccionado y justificación

Assert.AreApproximatelyEqual(0f, coordenada, 0.001f), para X, Y y Z.

Seleccioné AreApproximatelyEqual para comprobar que cada coordenada de transform.position esté cerca de cero, con tolerancia de 0.001 unidades. Los float pueden acumular pequeñas diferencias por representación y redondeo; una comparación aproximada evita fallos por variaciones mínimas. En (0, 0, 0) se cumple la condición; en (2, 0, 0) falla la comparación de X.

## Error del videojuego que podría detectar

Puede detectar que un objeto fijo o un punto de referencia se desplace por un cálculo incorrecto, una animación o un script de movimiento.

## Script completado: PositionAssertion.cs

```csharp
using UnityEngine;
using UnityEngine.Assertions;

public class PositionAssertion : MonoBehaviour
{
    void Update()
    {
        float positionX = transform.position.x;
        float positionY = transform.position.y;
        float positionZ = transform.position.z;

        Assert.AreApproximatelyEqual(0f, positionX, 0.001f, "CenterObject: X debe estar aproximadamente en 0.");
        Assert.AreApproximatelyEqual(0f, positionY, 0.001f, "CenterObject: Y debe estar aproximadamente en 0.");
        Assert.AreApproximatelyEqual(0f, positionZ, 0.001f, "CenterObject: Z debe estar aproximadamente en 0.");
    }
}
```

## Evidencias

Condición correcta: CenterObject en Position (0, 0, 0), durante Play Mode; Console sin fallos.

**[INSERTAR CAPTURA 3A — CONDICIÓN CORRECTA]**

Condición incorrecta provocada: CenterObject en Position (2, 0, 0), durante Play Mode, y el fallo de PositionAssertion en Console.

**[INSERTAR CAPTURA 3B — CONDICIÓN INCORRECTA]**

---

# Ejercicio 4 — Validación del Tag del jugador

## Assert seleccionado y justificación

Assert.AreEqual("Player", currentTag).

Seleccioné AreEqual porque se necesita igualdad exacta entre dos cadenas. El valor esperado es "Player"; el valor obtenido en el caso correcto es "Player" y en el caso incorrecto es "Untagged". La propiedad gameObject.tag permite obtener el Tag actual. Al no coincidir las cadenas, la aserción falla.

## Error del videojuego que podría detectar

Puede detectar un Tag incorrecto que impida reconocer al jugador en búsquedas por etiqueta, colisiones, enemigos o zonas de activación.

## Script completado: PlayerTagAssertion.cs

```csharp
using UnityEngine;
using UnityEngine.Assertions;

public class PlayerTagAssertion : MonoBehaviour
{
    void Update()
    {
        string currentTag = gameObject.tag;
        Assert.AreEqual("Player", currentTag, "El Tag del jugador debe ser Player.");
    }
}
```

## Evidencias

Condición correcta: Player con Tag Player, durante Play Mode; Console sin fallos.

**[INSERTAR CAPTURA 4A — CONDICIÓN CORRECTA]**

Condición incorrecta provocada: Player con Tag Untagged, después de ejecutar nuevamente, y el fallo de PlayerTagAssertion en Console.

**[INSERTAR CAPTURA 4B — CONDICIÓN INCORRECTA]**

---

# Ejercicio 5 — Validación de una referencia

## Assert seleccionado y justificación

Assert.IsNull(myClassReference).

Seleccioné IsNull porque el estado esperado inicialmente es una referencia sin instancia. Al crear un objeto mediante new MyClass(), la referencia deja de ser null y la aserción falla. El selector Create Reference On Start permite reproducir las dos variantes del PDF: desmarcado no crea la instancia; marcado ejecuta CreateReference() desde Start. El estado de la referencia se muestra en el Inspector durante Play Mode.

## Error del videojuego que podría detectar

Puede detectar una inicialización prematura o inesperada de una referencia que debía permanecer vacía hasta una etapa determinada del videojuego. En este ejercicio, tener una instancia es el caso incorrecto.

## Script completado: ReferenceAssertion.cs

```csharp
using UnityEngine;
using UnityEngine.Assertions;

public class ReferenceAssertion : MonoBehaviour
{
    private MyClass myClassReference;

    [Tooltip("Desactivado: referencia null (caso correcto). Activado: Start crea una instancia (caso incorrecto). Cambiar antes de Play.")]
    public bool createReferenceOnStart = false;

    public bool HasReference => myClassReference != null;

    void Start()
    {
        // Permite probar las dos variantes del PDF sin tener que editar el script.
        if (createReferenceOnStart)
            CreateReference();
    }

    void Update()
    {
        Assert.IsNull(myClassReference, "La referencia debe ser null antes de su inicializacion.");
    }

    public void CreateReference()
    {
        myClassReference = new MyClass();
    }
}

public class MyClass
{
}
```

## Evidencias

Condición correcta: ReferenceValidator con Create Reference On Start desmarcado, myClassReference: null y Console sin fallos, durante Play Mode.

**[INSERTAR CAPTURA 5A — CONDICIÓN CORRECTA]**

Condición incorrecta provocada: ReferenceValidator con Create Reference On Start marcado antes de iniciar, estado no null durante Play Mode y fallo de ReferenceAssertion en Console.

**[INSERTAR CAPTURA 5B — CONDICIÓN INCORRECTA]**

---

# Conclusiones

Las aserciones permiten comprobar condiciones esperadas durante la ejecución y localizar estados que podrían causar errores en el videojuego. Cada método debe elegirse según lo que se valida: desigualdad para la vida distinta de cero, una condición booleana para el objeto activo, aproximación para las coordenadas, igualdad para el Tag y nulidad para la referencia.

Provocar intencionalmente una condición incorrecta permite comprobar que la validación detecta el cambio. Estas comprobaciones ayudan durante el desarrollo, pero no reemplazan la lógica del videojuego ni corrigen por sí mismas el estado detectado.
