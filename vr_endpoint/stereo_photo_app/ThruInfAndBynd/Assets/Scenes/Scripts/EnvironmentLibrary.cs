using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.InputSystem;

public class EnvironmentLibrary : MonoBehaviour
{
    public SkyboxController m_SkyboxController;
	public List<Environment> m_Environments = null;
    public int m_CurEnv = 0;
    public int m_TotalNumEnv = 10;

    private void Start()
    {
        m_Environments = new List<Environment>();
        // Load the environments
        for (int i=0; i< m_TotalNumEnv; i++){
            var texture = Resources.Load<Texture>("MediaClips/ods_output_"+i.ToString());
            Environment env = new Environment();
            env.m_Background = texture;
            print("Texture object value "+texture+ " Filename "+ "MediaClips/ods_output_" + i.ToString());
            m_Environments.Add(env);
        }
    }

    // Update is called once per frame
    private void Update(){
        if (Input.GetKeyDown(KeyCode.DownArrow))
        {
            m_SkyboxController.NewEnvironment(m_Environments[m_CurEnv]);
            m_CurEnv += 1;
            if (m_CurEnv >= m_TotalNumEnv)
                m_CurEnv = 0;
        }
    }
}

[Serializable]
public class Environment{
	public int m_WorldRotation = 0;
	public Texture m_Background = null;
	public AudioClip m_AmbientNoise = null;
}
