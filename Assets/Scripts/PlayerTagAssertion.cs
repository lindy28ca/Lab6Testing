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
