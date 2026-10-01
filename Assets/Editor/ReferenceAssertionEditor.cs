using UnityEditor;
using UnityEngine;

[CustomEditor(typeof(ReferenceAssertion))]
public class ReferenceAssertionEditor : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();
        var validator = (ReferenceAssertion)target;
        string state = Application.isPlaying
            ? (validator.HasReference ? "Instancia de MyClass (no null)" : "null (sin instancia)")
            : "Entra en Play Mode para observar la referencia.";
        EditorGUILayout.HelpBox("myClassReference: " + state, MessageType.Info);
        EditorGUILayout.HelpBox("Cambia Create Reference On Start antes de Play: desmarcado = caso correcto; marcado = caso incorrecto.", MessageType.None);
        if (Application.isPlaying)
            Repaint();
    }
}
