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
