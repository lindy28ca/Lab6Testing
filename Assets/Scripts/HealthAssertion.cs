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
