using System;
using System.IO;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Assertions;
using UnityEngine.SceneManagement;

[InitializeOnLoad]
public static class Lab06Setup
{
    public const string ScenePath = "Assets/Scenes/Lab06Assertions.unity";
    private const string ValidationPath = "Entrega/Verificacion_Unity.txt";

    static Lab06Setup()
    {
        EditorApplication.delayCall += Prepare;
    }

    private static void Prepare()
    {
        if (EditorApplication.isPlayingOrWillChangePlaymode)
            return;

        if (!File.Exists(ScenePath))
            CreateScene();

        if (!File.Exists(ValidationPath))
            Verify();
    }

    [MenuItem("Laboratorio 06/Abrir escena preparada")]
    public static void OpenScene()
    {
        if (EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
            EditorSceneManager.OpenScene(ScenePath);
    }

    private static void CreateScene()
    {
        Scene previous = SceneManager.GetActiveScene();
        bool canOpen = previous.IsValid() && !previous.isDirty;
        Scene scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Additive);
        SceneManager.SetActiveScene(scene);

        GameObject player = new GameObject("Player");
        player.tag = "Player";
        player.AddComponent<HealthAssertion>();
        player.AddComponent<PlayerTagAssertion>();

        GameObject critical = new GameObject("CriticalObject");
        GameObject manager = new GameObject("GameManager");
        manager.AddComponent<ActiveObjectAssertion>().target = critical;

        GameObject center = new GameObject("CenterObject");
        center.transform.position = Vector3.zero;
        center.AddComponent<PositionAssertion>();

        GameObject reference = new GameObject("ReferenceValidator");
        reference.AddComponent<ReferenceAssertion>();

        EditorSceneManager.SaveScene(scene, ScenePath);
        EditorSceneManager.CloseScene(scene, true);
        if (previous.IsValid())
            SceneManager.SetActiveScene(previous);

        EditorBuildSettings.scenes = new[] { new EditorBuildSettingsScene(ScenePath, true) };
        if (canOpen)
            EditorSceneManager.OpenScene(ScenePath);

        Debug.Log("Laboratorio 06: escena preparada. Abrela desde el menu Laboratorio 06.");
    }

    [MenuItem("Laboratorio 06/Verificar validaciones")]
    public static void Verify()
    {
        if (EditorApplication.isPlayingOrWillChangePlaymode)
            return;

        string result = "Laboratorio 06 - Verificacion real de los scripts en Unity " + Application.unityVersion + "\n";
        bool previousRaise = Assert.raiseExceptions;
        Scene previousScene = SceneManager.GetActiveScene();
        Scene testScene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Additive);
        SceneManager.SetActiveScene(testScene);
        Assert.raiseExceptions = true;
        try
        {
            var player = new GameObject("TestPlayer");
            var health = player.AddComponent<HealthAssertion>();
            Check(health, false);
            health.health = 0;
            Check(health, true);
            result += "PASS 1: health=100 aceptado; health=0 detectado.\n";

            var critical = new GameObject("TestCritical");
            var active = new GameObject("TestManager").AddComponent<ActiveObjectAssertion>();
            active.target = critical;
            Check(active, false);
            critical.SetActive(false);
            Check(active, true);
            critical.SetActive(true);
            var parent = new GameObject("TestParent");
            critical.transform.SetParent(parent.transform);
            parent.SetActive(false);
            Check(active, true);
            active.target = null;
            Check(active, true);
            result += "PASS 2: activo aceptado; objeto/ancestro inactivo y referencia faltante detectados.\n";

            var position = new GameObject("TestCenter").AddComponent<PositionAssertion>();
            Check(position, false);
            position.transform.position = new Vector3(0.0005f, 0f, 0f);
            Check(position, false);
            foreach (Vector3 value in new[] { new Vector3(2f, 0f, 0f), new Vector3(0f, 2f, 0f), new Vector3(0f, 0f, 2f) })
            {
                position.transform.position = value;
                Check(position, true);
            }
            result += "PASS 3: origen y pequena variacion aceptados; desplazamientos en X/Y/Z detectados.\n";

            var tag = player.AddComponent<PlayerTagAssertion>();
            player.tag = "Player";
            Check(tag, false);
            player.tag = "Untagged";
            Check(tag, true);
            result += "PASS 4: Player aceptado; Untagged detectado.\n";

            var reference = new GameObject("TestReference").AddComponent<ReferenceAssertion>();
            Invoke(reference, "Start");
            Check(reference, false);
            reference.createReferenceOnStart = true;
            Invoke(reference, "Start");
            Check(reference, true);
            result += "PASS 5: null aceptado; instancia creada desde Start detectada.\n";

            Scene saved = SceneManager.GetSceneByPath(ScenePath);
            bool openedForCheck = !saved.IsValid() || !saved.isLoaded;
            if (openedForCheck)
                saved = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Additive);
            try
            {
                GameObject[] roots = saved.GetRootGameObjects();
                GameObject savedPlayer = Array.Find(roots, obj => obj.name == "Player");
                GameObject savedManager = Array.Find(roots, obj => obj.name == "GameManager");
                GameObject savedCritical = Array.Find(roots, obj => obj.name == "CriticalObject");
                GameObject savedCenter = Array.Find(roots, obj => obj.name == "CenterObject");
                GameObject savedReference = Array.Find(roots, obj => obj.name == "ReferenceValidator");
                if (savedPlayer == null || savedManager == null || savedCritical == null || savedCenter == null || savedReference == null)
                    throw new Exception("Falta un objeto requerido en la escena guardada.");
                if (savedPlayer.tag != "Player" || savedPlayer.GetComponent<HealthAssertion>().health != 100 ||
                    savedPlayer.GetComponent<PlayerTagAssertion>() == null ||
                    savedManager.GetComponent<ActiveObjectAssertion>().target != savedCritical || !savedCritical.activeInHierarchy ||
                    savedCenter.transform.position != Vector3.zero || savedCenter.GetComponent<PositionAssertion>() == null ||
                    savedReference.GetComponent<ReferenceAssertion>().createReferenceOnStart)
                    throw new Exception("La escena guardada no tiene la configuracion inicial correcta.");
                result += "PASS: escena guardada con objetos, scripts, Tag y referencia target correctos.\n";
            }
            finally
            {
                if (openedForCheck)
                    EditorSceneManager.CloseScene(saved, true);
            }
            result += "Resultado: todas las verificaciones completadas. Las capturas de Play Mode se incorporan por separado.\n";
        }
        catch (Exception exception)
        {
            result += "FAIL: " + exception + "\n";
            Debug.LogException(exception);
        }
        finally
        {
            Assert.raiseExceptions = previousRaise;
            EditorSceneManager.CloseScene(testScene, true);
            if (previousScene.IsValid())
                SceneManager.SetActiveScene(previousScene);
        }
        Directory.CreateDirectory("Entrega");
        File.WriteAllText(ValidationPath, result);
        Debug.Log(result);
    }

    private static void Invoke(MonoBehaviour component, string method)
    {
        component.GetType().GetMethod(method, BindingFlags.Instance | BindingFlags.NonPublic).Invoke(component, null);
    }

    private static void Check(MonoBehaviour component, bool shouldFail)
    {
        bool failed = false;
        try
        {
            Invoke(component, "Update");
        }
        catch (TargetInvocationException exception) when (exception.InnerException is AssertionException)
        {
            failed = true;
        }
        if (failed != shouldFail)
            throw new Exception(component.GetType().Name + ": resultado inesperado.");
    }
}
