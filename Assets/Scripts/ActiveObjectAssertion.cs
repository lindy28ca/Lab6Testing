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
