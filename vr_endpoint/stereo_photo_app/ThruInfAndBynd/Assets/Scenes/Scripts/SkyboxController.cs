using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SkyboxController : Controller
{
	protected override IEnumerator Apply(Environment environment) {
		//Fade Out
		float startValue = RenderSettings.skybox.GetFloat("_Exposure");
		yield return StartCoroutine(Interpolate(0.25f, startValue, 0.0f, UpdateExposureCallback));

		//Set new texture
		RenderSettings.skybox.SetFloat("_Rotation", environment.m_WorldRotation);
		RenderSettings.skybox.mainTexture = environment.m_Background;

		//Fade In
		yield return StartCoroutine(Interpolate(0.25f, startValue, 1.0f, UpdateExposureCallback));

		//Debug
		Debug.Log("Skybox Applied");
	}

	private void UpdateExposureCallback(float value) {
		RenderSettings.skybox.SetFloat("_Exposure", value);
	}
}
