using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

public class UserInput : MonoBehaviour
{
	public static UnityEvent OnTouchStart = new UnityEvent();
	public static UnityEvent OnTouchEnd = new UnityEvent(); 
	public static UnityEvent OnTouchpadLeftUp = new UnityEvent();
	public static UnityEvent OnTouchpadRightEnd = new UnityEvent(); 

    // Update is called once per frame
    private void Update(){
#if UNITY_EDITOR
    	KeyboardInput();
#endif
        
    }
    private void KeyboardInput(){
		if(Input.GetKeyDown(KeyCode.Space)){
			if(OnTouchStart != null){
				OnTouchStart.Invoke();
			}
		}
		if(Input.GetKeyUp(KeyCode.Space)){
			if(OnTouchEnd != null){
				OnTouchEnd.Invoke();
			}
		}
		if(Input.GetKeyDown(KeyCode.LeftArrow)){
			if(OnTouchpadLeftUp != null){
				OnTouchpadLeftUp.Invoke();
			}
		}
		if(Input.GetKeyUp(KeyCode.RightArrow)){
			if(OnTouchpadRightEnd != null){
				OnTouchpadRightEnd.Invoke();
			}
		}
	}
}



