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
