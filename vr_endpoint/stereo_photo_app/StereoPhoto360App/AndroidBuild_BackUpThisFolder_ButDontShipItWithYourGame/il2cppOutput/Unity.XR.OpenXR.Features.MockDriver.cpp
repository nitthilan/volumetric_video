#include "pch-cpp.hpp"

#ifndef _MSC_VER
# include <alloca.h>
#else
# include <malloc.h>
#endif


#include <limits>
#include <stdint.h>


template <typename T1, typename T2>
struct InvokerActionInvoker2
{
	static inline void Invoke (Il2CppMethodPointer methodPtr, const RuntimeMethod* method, void* obj, T1 p1, T2 p2)
	{
		void* params[2] = { &p1, &p2 };
		method->invoker_method(methodPtr, method, obj, params, NULL);
	}
};
template <typename T1, typename T2, typename T3>
struct InvokerActionInvoker3;
template <typename T1, typename T2, typename T3>
struct InvokerActionInvoker3<T1*, T2, T3>
{
	static inline void Invoke (Il2CppMethodPointer methodPtr, const RuntimeMethod* method, void* obj, T1* p1, T2 p2, T3 p3)
	{
		void* params[3] = { p1, &p2, &p3 };
		method->invoker_method(methodPtr, method, obj, params, NULL);
	}
};

// System.Char[]
struct CharU5BU5D_t799905CF001DD5F13F7DBB310181FC4D8B7D0AAB;
// System.Delegate[]
struct DelegateU5BU5D_tC5AB7E8F745616680F337909D3A8E6C722CDF771;
// System.AsyncCallback
struct AsyncCallback_t7FEF460CBDCFB9C5FA2EF776984778B9A4145F4C;
// System.Delegate
struct Delegate_t;
// System.DelegateData
struct DelegateData_t9B286B493293CD2D23A5B2B5EF0E5B1324C2B77E;
// System.IAsyncResult
struct IAsyncResult_t7B9B5A0ECB35DCEC31B8A8122C37D687369253B5;
// System.Reflection.MethodInfo
struct MethodInfo_t;
// UnityEngine.XR.OpenXR.Features.Mock.MockDriver
struct MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17;
// UnityEngine.XR.OpenXR.Features.OpenXRFeature
struct OpenXRFeature_tC2F8F480D62C277B2ECDD605F64E45053CD85143;
// System.String
struct String_t;
// System.Void
struct Void_t4861ACF8F4594C3437BB48B6E56783494B843915;
// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate
struct ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1;

IL2CPP_EXTERN_C RuntimeClass* Debug_t8394C7EEAECA3689C2C9B9DE9C7166D73596276F_il2cpp_TypeInfo_var;
IL2CPP_EXTERN_C RuntimeClass* MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var;
IL2CPP_EXTERN_C RuntimeClass* ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1_il2cpp_TypeInfo_var;
IL2CPP_EXTERN_C RuntimeClass* ScriptEvent_t99C1B1F4925AFADF949EC80C822FC611B67B3BD5_il2cpp_TypeInfo_var;
IL2CPP_EXTERN_C RuntimeClass* UInt64_t8F12534CC8FC4B5860F2A2CD1EE79D322E7A41AF_il2cpp_TypeInfo_var;
IL2CPP_EXTERN_C String_t* _stringLiteral1FDC7B050699D12543255FBE775FDDC07F9A1BF3;
IL2CPP_EXTERN_C String_t* _stringLiteral3BFAF67BC1D43F33C94D76E23C8F313BD41DDBFF;
IL2CPP_EXTERN_C const RuntimeMethod* MockDriver_ReceiveScriptEvent_m02DD920C8DD9F0F69295FF330269F1D3C1EBC49C_RuntimeMethod_var;
struct Delegate_t_marshaled_com;
struct Delegate_t_marshaled_pinvoke;

struct DelegateU5BU5D_tC5AB7E8F745616680F337909D3A8E6C722CDF771;

IL2CPP_EXTERN_C_BEGIN
IL2CPP_EXTERN_C_END

#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif

// <Module>
struct U3CModuleU3E_t289CD4460C112A9ED30C044CF56DC4AFE408BC48 
{
};
struct Il2CppArrayBounds;

// System.String
struct String_t  : public RuntimeObject
{
	// System.Int32 System.String::_stringLength
	int32_t ____stringLength_4;
	// System.Char System.String::_firstChar
	Il2CppChar ____firstChar_5;
};

struct String_t_StaticFields
{
	// System.String System.String::Empty
	String_t* ___Empty_6;
};

// System.ValueType
struct ValueType_t6D9B272BD21782F0A9A14F2E41F85A50E97A986F  : public RuntimeObject
{
};
// Native definition for P/Invoke marshalling of System.ValueType
struct ValueType_t6D9B272BD21782F0A9A14F2E41F85A50E97A986F_marshaled_pinvoke
{
};
// Native definition for COM marshalling of System.ValueType
struct ValueType_t6D9B272BD21782F0A9A14F2E41F85A50E97A986F_marshaled_com
{
};

// System.Boolean
struct Boolean_t09A6377A54BE2F9E6985A8149F19234FD7DDFE22 
{
	// System.Boolean System.Boolean::m_value
	bool ___m_value_0;
};

struct Boolean_t09A6377A54BE2F9E6985A8149F19234FD7DDFE22_StaticFields
{
	// System.String System.Boolean::TrueString
	String_t* ___TrueString_5;
	// System.String System.Boolean::FalseString
	String_t* ___FalseString_6;
};

// System.Enum
struct Enum_t2A1A94B24E3B776EEF4E5E485E290BB9D4D072E2  : public ValueType_t6D9B272BD21782F0A9A14F2E41F85A50E97A986F
{
};

struct Enum_t2A1A94B24E3B776EEF4E5E485E290BB9D4D072E2_StaticFields
{
	// System.Char[] System.Enum::enumSeperatorCharArray
	CharU5BU5D_t799905CF001DD5F13F7DBB310181FC4D8B7D0AAB* ___enumSeperatorCharArray_0;
};
// Native definition for P/Invoke marshalling of System.Enum
struct Enum_t2A1A94B24E3B776EEF4E5E485E290BB9D4D072E2_marshaled_pinvoke
{
};
// Native definition for COM marshalling of System.Enum
struct Enum_t2A1A94B24E3B776EEF4E5E485E290BB9D4D072E2_marshaled_com
{
};

// System.Int32
struct Int32_t680FF22E76F6EFAD4375103CBBFFA0421349384C 
{
	// System.Int32 System.Int32::m_value
	int32_t ___m_value_0;
};

// System.IntPtr
struct IntPtr_t 
{
	// System.Void* System.IntPtr::m_value
	void* ___m_value_0;
};

struct IntPtr_t_StaticFields
{
	// System.IntPtr System.IntPtr::Zero
	intptr_t ___Zero_1;
};

// UnityEngine.Quaternion
struct Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974 
{
	// System.Single UnityEngine.Quaternion::x
	float ___x_0;
	// System.Single UnityEngine.Quaternion::y
	float ___y_1;
	// System.Single UnityEngine.Quaternion::z
	float ___z_2;
	// System.Single UnityEngine.Quaternion::w
	float ___w_3;
};

struct Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974_StaticFields
{
	// UnityEngine.Quaternion UnityEngine.Quaternion::identityQuaternion
	Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974 ___identityQuaternion_4;
};

// System.UInt64
struct UInt64_t8F12534CC8FC4B5860F2A2CD1EE79D322E7A41AF 
{
	// System.UInt64 System.UInt64::m_value
	uint64_t ___m_value_0;
};

// UnityEngine.Vector2
struct Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7 
{
	// System.Single UnityEngine.Vector2::x
	float ___x_0;
	// System.Single UnityEngine.Vector2::y
	float ___y_1;
};

struct Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7_StaticFields
{
	// UnityEngine.Vector2 UnityEngine.Vector2::zeroVector
	Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7 ___zeroVector_2;
	// UnityEngine.Vector2 UnityEngine.Vector2::oneVector
	Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7 ___oneVector_3;
	// UnityEngine.Vector2 UnityEngine.Vector2::upVector
	Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7 ___upVector_4;
	// UnityEngine.Vector2 UnityEngine.Vector2::downVector
	Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7 ___downVector_5;
	// UnityEngine.Vector2 UnityEngine.Vector2::leftVector
	Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7 ___leftVector_6;
	// UnityEngine.Vector2 UnityEngine.Vector2::rightVector
	Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7 ___rightVector_7;
	// UnityEngine.Vector2 UnityEngine.Vector2::positiveInfinityVector
	Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7 ___positiveInfinityVector_8;
	// UnityEngine.Vector2 UnityEngine.Vector2::negativeInfinityVector
	Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7 ___negativeInfinityVector_9;
};

// UnityEngine.Vector3
struct Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 
{
	// System.Single UnityEngine.Vector3::x
	float ___x_2;
	// System.Single UnityEngine.Vector3::y
	float ___y_3;
	// System.Single UnityEngine.Vector3::z
	float ___z_4;
};

struct Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2_StaticFields
{
	// UnityEngine.Vector3 UnityEngine.Vector3::zeroVector
	Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___zeroVector_5;
	// UnityEngine.Vector3 UnityEngine.Vector3::oneVector
	Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___oneVector_6;
	// UnityEngine.Vector3 UnityEngine.Vector3::upVector
	Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___upVector_7;
	// UnityEngine.Vector3 UnityEngine.Vector3::downVector
	Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___downVector_8;
	// UnityEngine.Vector3 UnityEngine.Vector3::leftVector
	Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___leftVector_9;
	// UnityEngine.Vector3 UnityEngine.Vector3::rightVector
	Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___rightVector_10;
	// UnityEngine.Vector3 UnityEngine.Vector3::forwardVector
	Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___forwardVector_11;
	// UnityEngine.Vector3 UnityEngine.Vector3::backVector
	Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___backVector_12;
	// UnityEngine.Vector3 UnityEngine.Vector3::positiveInfinityVector
	Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___positiveInfinityVector_13;
	// UnityEngine.Vector3 UnityEngine.Vector3::negativeInfinityVector
	Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___negativeInfinityVector_14;
};

// UnityEngine.Vector4
struct Vector4_t58B63D32F48C0DBF50DE2C60794C4676C80EDBE3 
{
	// System.Single UnityEngine.Vector4::x
	float ___x_1;
	// System.Single UnityEngine.Vector4::y
	float ___y_2;
	// System.Single UnityEngine.Vector4::z
	float ___z_3;
	// System.Single UnityEngine.Vector4::w
	float ___w_4;
};

struct Vector4_t58B63D32F48C0DBF50DE2C60794C4676C80EDBE3_StaticFields
{
	// UnityEngine.Vector4 UnityEngine.Vector4::zeroVector
	Vector4_t58B63D32F48C0DBF50DE2C60794C4676C80EDBE3 ___zeroVector_5;
	// UnityEngine.Vector4 UnityEngine.Vector4::oneVector
	Vector4_t58B63D32F48C0DBF50DE2C60794C4676C80EDBE3 ___oneVector_6;
	// UnityEngine.Vector4 UnityEngine.Vector4::positiveInfinityVector
	Vector4_t58B63D32F48C0DBF50DE2C60794C4676C80EDBE3 ___positiveInfinityVector_7;
	// UnityEngine.Vector4 UnityEngine.Vector4::negativeInfinityVector
	Vector4_t58B63D32F48C0DBF50DE2C60794C4676C80EDBE3 ___negativeInfinityVector_8;
};

// System.Void
struct Void_t4861ACF8F4594C3437BB48B6E56783494B843915 
{
	union
	{
		struct
		{
		};
		uint8_t Void_t4861ACF8F4594C3437BB48B6E56783494B843915__padding[1];
	};
};

// System.Delegate
struct Delegate_t  : public RuntimeObject
{
	// System.IntPtr System.Delegate::method_ptr
	Il2CppMethodPointer ___method_ptr_0;
	// System.IntPtr System.Delegate::invoke_impl
	intptr_t ___invoke_impl_1;
	// System.Object System.Delegate::m_target
	RuntimeObject* ___m_target_2;
	// System.IntPtr System.Delegate::method
	intptr_t ___method_3;
	// System.IntPtr System.Delegate::delegate_trampoline
	intptr_t ___delegate_trampoline_4;
	// System.IntPtr System.Delegate::extra_arg
	intptr_t ___extra_arg_5;
	// System.IntPtr System.Delegate::method_code
	intptr_t ___method_code_6;
	// System.IntPtr System.Delegate::interp_method
	intptr_t ___interp_method_7;
	// System.IntPtr System.Delegate::interp_invoke_impl
	intptr_t ___interp_invoke_impl_8;
	// System.Reflection.MethodInfo System.Delegate::method_info
	MethodInfo_t* ___method_info_9;
	// System.Reflection.MethodInfo System.Delegate::original_method_info
	MethodInfo_t* ___original_method_info_10;
	// System.DelegateData System.Delegate::data
	DelegateData_t9B286B493293CD2D23A5B2B5EF0E5B1324C2B77E* ___data_11;
	// System.Boolean System.Delegate::method_is_virtual
	bool ___method_is_virtual_12;
};
// Native definition for P/Invoke marshalling of System.Delegate
struct Delegate_t_marshaled_pinvoke
{
	intptr_t ___method_ptr_0;
	intptr_t ___invoke_impl_1;
	Il2CppIUnknown* ___m_target_2;
	intptr_t ___method_3;
	intptr_t ___delegate_trampoline_4;
	intptr_t ___extra_arg_5;
	intptr_t ___method_code_6;
	intptr_t ___interp_method_7;
	intptr_t ___interp_invoke_impl_8;
	MethodInfo_t* ___method_info_9;
	MethodInfo_t* ___original_method_info_10;
	DelegateData_t9B286B493293CD2D23A5B2B5EF0E5B1324C2B77E* ___data_11;
	int32_t ___method_is_virtual_12;
};
// Native definition for COM marshalling of System.Delegate
struct Delegate_t_marshaled_com
{
	intptr_t ___method_ptr_0;
	intptr_t ___invoke_impl_1;
	Il2CppIUnknown* ___m_target_2;
	intptr_t ___method_3;
	intptr_t ___delegate_trampoline_4;
	intptr_t ___extra_arg_5;
	intptr_t ___method_code_6;
	intptr_t ___interp_method_7;
	intptr_t ___interp_invoke_impl_8;
	MethodInfo_t* ___method_info_9;
	MethodInfo_t* ___original_method_info_10;
	DelegateData_t9B286B493293CD2D23A5B2B5EF0E5B1324C2B77E* ___data_11;
	int32_t ___method_is_virtual_12;
};

// UnityEngine.Object
struct Object_tC12DECB6760A7F2CBF65D9DCF18D044C2D97152C  : public RuntimeObject
{
	// System.IntPtr UnityEngine.Object::m_CachedPtr
	intptr_t ___m_CachedPtr_0;
};

struct Object_tC12DECB6760A7F2CBF65D9DCF18D044C2D97152C_StaticFields
{
	// System.Int32 UnityEngine.Object::OffsetOfInstanceIDInCPlusPlusObject
	int32_t ___OffsetOfInstanceIDInCPlusPlusObject_1;
};
// Native definition for P/Invoke marshalling of UnityEngine.Object
struct Object_tC12DECB6760A7F2CBF65D9DCF18D044C2D97152C_marshaled_pinvoke
{
	intptr_t ___m_CachedPtr_0;
};
// Native definition for COM marshalling of UnityEngine.Object
struct Object_tC12DECB6760A7F2CBF65D9DCF18D044C2D97152C_marshaled_com
{
	intptr_t ___m_CachedPtr_0;
};

// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEvent
struct ScriptEvent_t99C1B1F4925AFADF949EC80C822FC611B67B3BD5 
{
	// System.Int32 UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEvent::value__
	int32_t ___value___2;
};

// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrReferenceSpaceType
struct XrReferenceSpaceType_t1F7AE35F2D9956E6006842BB668076C14C6F08F4 
{
	// System.Int32 UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrReferenceSpaceType::value__
	int32_t ___value___2;
};

// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrResult
struct XrResult_t2E9D9D205AECA14A94D48DF740EBA58A07B4DD30 
{
	// System.Int32 UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrResult::value__
	int32_t ___value___2;
};

// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrSessionState
struct XrSessionState_t64014D061EAD9023ACF11A5E8C8955E7986FF101 
{
	// System.Int32 UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrSessionState::value__
	int32_t ___value___2;
};

// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrSpaceLocationFlags
struct XrSpaceLocationFlags_tE83E31AE3890DB3F3308A21139CB1B9F1407A1F7 
{
	// System.Int32 UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrSpaceLocationFlags::value__
	int32_t ___value___2;
};

// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrViewConfigurationType
struct XrViewConfigurationType_t6987DA4DCB9280F85693473478FFB16D4D77E284 
{
	// System.Int32 UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrViewConfigurationType::value__
	int32_t ___value___2;
};

// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrViewStateFlags
struct XrViewStateFlags_tDC9D85E2A0BF44C22A588473F1E4B2C5A4F87D93 
{
	// System.Int32 UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrViewStateFlags::value__
	int32_t ___value___2;
};

// System.MulticastDelegate
struct MulticastDelegate_t  : public Delegate_t
{
	// System.Delegate[] System.MulticastDelegate::delegates
	DelegateU5BU5D_tC5AB7E8F745616680F337909D3A8E6C722CDF771* ___delegates_13;
};
// Native definition for P/Invoke marshalling of System.MulticastDelegate
struct MulticastDelegate_t_marshaled_pinvoke : public Delegate_t_marshaled_pinvoke
{
	Delegate_t_marshaled_pinvoke** ___delegates_13;
};
// Native definition for COM marshalling of System.MulticastDelegate
struct MulticastDelegate_t_marshaled_com : public Delegate_t_marshaled_com
{
	Delegate_t_marshaled_com** ___delegates_13;
};

// UnityEngine.ScriptableObject
struct ScriptableObject_tB3BFDB921A1B1795B38A5417D3B97A89A140436A  : public Object_tC12DECB6760A7F2CBF65D9DCF18D044C2D97152C
{
};
// Native definition for P/Invoke marshalling of UnityEngine.ScriptableObject
struct ScriptableObject_tB3BFDB921A1B1795B38A5417D3B97A89A140436A_marshaled_pinvoke : public Object_tC12DECB6760A7F2CBF65D9DCF18D044C2D97152C_marshaled_pinvoke
{
};
// Native definition for COM marshalling of UnityEngine.ScriptableObject
struct ScriptableObject_tB3BFDB921A1B1795B38A5417D3B97A89A140436A_marshaled_com : public Object_tC12DECB6760A7F2CBF65D9DCF18D044C2D97152C_marshaled_com
{
};

// System.AsyncCallback
struct AsyncCallback_t7FEF460CBDCFB9C5FA2EF776984778B9A4145F4C  : public MulticastDelegate_t
{
};

// UnityEngine.XR.OpenXR.Features.OpenXRFeature
struct OpenXRFeature_tC2F8F480D62C277B2ECDD605F64E45053CD85143  : public ScriptableObject_tB3BFDB921A1B1795B38A5417D3B97A89A140436A
{
	// System.Boolean UnityEngine.XR.OpenXR.Features.OpenXRFeature::m_enabled
	bool ___m_enabled_4;
	// System.Boolean UnityEngine.XR.OpenXR.Features.OpenXRFeature::<failedInitialization>k__BackingField
	bool ___U3CfailedInitializationU3Ek__BackingField_5;
	// System.String UnityEngine.XR.OpenXR.Features.OpenXRFeature::nameUi
	String_t* ___nameUi_7;
	// System.String UnityEngine.XR.OpenXR.Features.OpenXRFeature::version
	String_t* ___version_8;
	// System.String UnityEngine.XR.OpenXR.Features.OpenXRFeature::featureIdInternal
	String_t* ___featureIdInternal_9;
	// System.String UnityEngine.XR.OpenXR.Features.OpenXRFeature::openxrExtensionStrings
	String_t* ___openxrExtensionStrings_10;
	// System.String UnityEngine.XR.OpenXR.Features.OpenXRFeature::company
	String_t* ___company_11;
	// System.Int32 UnityEngine.XR.OpenXR.Features.OpenXRFeature::priority
	int32_t ___priority_12;
	// System.Boolean UnityEngine.XR.OpenXR.Features.OpenXRFeature::required
	bool ___required_13;
};

struct OpenXRFeature_tC2F8F480D62C277B2ECDD605F64E45053CD85143_StaticFields
{
	// System.Boolean UnityEngine.XR.OpenXR.Features.OpenXRFeature::<requiredFeatureFailed>k__BackingField
	bool ___U3CrequiredFeatureFailedU3Ek__BackingField_6;
};

// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate
struct ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1  : public MulticastDelegate_t
{
};

// UnityEngine.XR.OpenXR.Features.Mock.MockDriver
struct MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17  : public OpenXRFeature_tC2F8F480D62C277B2ECDD605F64E45053CD85143
{
};

struct MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_StaticFields
{
	// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate UnityEngine.XR.OpenXR.Features.Mock.MockDriver::onScriptEvent
	ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* ___onScriptEvent_16;
};
#ifdef __clang__
#pragma clang diagnostic pop
#endif
// System.Delegate[]
struct DelegateU5BU5D_tC5AB7E8F745616680F337909D3A8E6C722CDF771  : public RuntimeArray
{
	ALIGN_FIELD (8) Delegate_t* m_Items[1];

	inline Delegate_t* GetAt(il2cpp_array_size_t index) const
	{
		IL2CPP_ARRAY_BOUNDS_CHECK(index, (uint32_t)(this)->max_length);
		return m_Items[index];
	}
	inline Delegate_t** GetAddressAt(il2cpp_array_size_t index)
	{
		IL2CPP_ARRAY_BOUNDS_CHECK(index, (uint32_t)(this)->max_length);
		return m_Items + index;
	}
	inline void SetAt(il2cpp_array_size_t index, Delegate_t* value)
	{
		IL2CPP_ARRAY_BOUNDS_CHECK(index, (uint32_t)(this)->max_length);
		m_Items[index] = value;
		Il2CppCodeGenWriteBarrier((void**)m_Items + index, (void*)value);
	}
	inline Delegate_t* GetAtUnchecked(il2cpp_array_size_t index) const
	{
		return m_Items[index];
	}
	inline Delegate_t** GetAddressAtUnchecked(il2cpp_array_size_t index)
	{
		return m_Items + index;
	}
	inline void SetAtUnchecked(il2cpp_array_size_t index, Delegate_t* value)
	{
		m_Items[index] = value;
		Il2CppCodeGenWriteBarrier((void**)m_Items + index, (void*)value);
	}
};



// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::ReceiveScriptEvent(UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEvent,System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_ReceiveScriptEvent_m02DD920C8DD9F0F69295FF330269F1D3C1EBC49C (int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method) ;
// System.Delegate System.Delegate::Combine(System.Delegate,System.Delegate)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR Delegate_t* Delegate_Combine_m8B9D24CED35033C7FC56501DFE650F5CB7FF012C (Delegate_t* ___a0, Delegate_t* ___b1, const RuntimeMethod* method) ;
// System.Delegate System.Delegate::Remove(System.Delegate,System.Delegate)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR Delegate_t* Delegate_Remove_m40506877934EC1AD4ADAE57F5E97AF0BC0F96116 (Delegate_t* ___source0, Delegate_t* ___value1, const RuntimeMethod* method) ;
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate::Invoke(UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEvent,System.UInt64)
IL2CPP_MANAGED_FORCE_INLINE IL2CPP_METHOD_ATTR void ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_inline (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method) ;
// System.Boolean UnityEngine.XR.OpenXR.OpenXRRuntime::IsExtensionEnabled(System.String)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR bool OpenXRRuntime_IsExtensionEnabled_m843EDD466C2EFA0E1C1350621411522290C74716 (String_t* ___extensionName0, const RuntimeMethod* method) ;
// System.Void UnityEngine.Debug::LogWarning(System.Object)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void Debug_LogWarning_mEF15C6B17CE4E1FA7E379CDB82CE40FCD89A3F28 (RuntimeObject* ___message0, const RuntimeMethod* method) ;
// System.IntPtr UnityEngine.XR.OpenXR.Features.OpenXRFeature::get_xrGetInstanceProcAddr()
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR intptr_t OpenXRFeature_get_xrGetInstanceProcAddr_m616F5709A63844DA12D409E8FEF4929EFA9F5B22 (const RuntimeMethod* method) ;
// System.IntPtr UnityEngine.XR.OpenXR.Features.Mock.MockDriver::InitializeNative(System.IntPtr,System.UInt64,System.UInt64,System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR intptr_t MockDriver_InitializeNative_mFF63260B5E7354460BFFA8654A178000C65CA0F2 (intptr_t ___xrGetInstanceProcAddr0, uint64_t ___xrInstance1, uint64_t ___session2, uint64_t ___sceneSpace3, const RuntimeMethod* method) ;
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate::.ctor(System.Object,System.IntPtr)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void ScriptEventDelegate__ctor_mD5F27EA5643A1BD3D22D66C3D4FE89799B70930E (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, RuntimeObject* ___object0, intptr_t ___method1, const RuntimeMethod* method) ;
// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrResult UnityEngine.XR.OpenXR.Features.Mock.MockDriver::MockDriver_RegisterScriptEventCallback(UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR int32_t MockDriver_MockDriver_RegisterScriptEventCallback_m39C8E09B89D20375AF2DD3C8ACAD633B053C9779 (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* ___callback0, const RuntimeMethod* method) ;
// System.IntPtr UnityEngine.XR.OpenXR.Features.Mock.MockDriver::ShutdownNative(System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR intptr_t MockDriver_ShutdownNative_m9DEB4E32813F4F3AB8E57262727EA0366BEF5CF1 (uint64_t ___xrInstance0, const RuntimeMethod* method) ;
// System.Void UnityEngine.XR.OpenXR.Features.OpenXRFeature::.ctor()
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void OpenXRFeature__ctor_m120460E34ECC22ED2DB96797A6DCB5C870E78852 (OpenXRFeature_tC2F8F480D62C277B2ECDD605F64E45053CD85143* __this, const RuntimeMethod* method) ;
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C intptr_t DEFAULT_CALL script_initialize(intptr_t, uint64_t, uint64_t, uint64_t);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C intptr_t DEFAULT_CALL script_shutdown(uint64_t);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C int32_t DEFAULT_CALL MockDriver_TransitionMockToState(uint64_t, int32_t, int32_t);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C void DEFAULT_CALL MockDriver_SetReturnCodeForFunction(char*, int32_t);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C void DEFAULT_CALL MockDriver_RequestExitSession(uint64_t);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C void DEFAULT_CALL MockDriver_SetBlendModeOpaque(int32_t);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C void DEFAULT_CALL MockDriver_SetReferenceSpaceBoundsRect(uint64_t, int32_t, Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C void DEFAULT_CALL MockDriver_CauseInstanceLoss(uint64_t);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C int32_t DEFAULT_CALL MockDriver_SetSpacePose(Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974, Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2, int32_t);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C int32_t DEFAULT_CALL MockDriver_SetViewPose(int32_t, Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974, Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2, Vector4_t58B63D32F48C0DBF50DE2C60794C4676C80EDBE3, int32_t);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C int32_t DEFAULT_CALL MockDriver_GetEndFrameStats(int32_t*, int32_t*);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C int32_t DEFAULT_CALL MockDriver_ActivateSecondaryView(int32_t, int32_t);
#endif
#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
IL2CPP_EXTERN_C int32_t DEFAULT_CALL MockDriver_RegisterScriptEventCallback(Il2CppMethodPointer);
#endif
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif
#ifdef __clang__
#pragma clang diagnostic pop
#endif
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif
extern "C" void DEFAULT_CALL ReversePInvokeWrapper_MockDriver_ReceiveScriptEvent_m02DD920C8DD9F0F69295FF330269F1D3C1EBC49C(int32_t ___evt0, uint64_t ___param1)
{
	il2cpp::vm::ScopedThreadAttacher _vmThreadHelper;

	// Managed method invocation
	MockDriver_ReceiveScriptEvent_m02DD920C8DD9F0F69295FF330269F1D3C1EBC49C(___evt0, ___param1, NULL);

}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::add_onScriptEvent(UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_add_onScriptEvent_m1F5089594E6AC6A2D68781362B16E31A8A3F54D6 (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* ___value0, const RuntimeMethod* method) 
{
	static bool s_Il2CppMethodInitialized;
	if (!s_Il2CppMethodInitialized)
	{
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var);
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1_il2cpp_TypeInfo_var);
		s_Il2CppMethodInitialized = true;
	}
	ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* V_0 = NULL;
	ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* V_1 = NULL;
	ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* V_2 = NULL;
	{
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_0 = ((MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_StaticFields*)il2cpp_codegen_static_fields_for(MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var))->___onScriptEvent_16;
		V_0 = L_0;
	}

IL_0006:
	{
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_1 = V_0;
		V_1 = L_1;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_2 = V_1;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_3 = ___value0;
		Delegate_t* L_4;
		L_4 = Delegate_Combine_m8B9D24CED35033C7FC56501DFE650F5CB7FF012C(L_2, L_3, NULL);
		V_2 = ((ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*)CastclassSealed((RuntimeObject*)L_4, ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1_il2cpp_TypeInfo_var));
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_5 = V_2;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_6 = V_1;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_7;
		L_7 = InterlockedCompareExchangeImpl<ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*>((&((MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_StaticFields*)il2cpp_codegen_static_fields_for(MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var))->___onScriptEvent_16), L_5, L_6);
		V_0 = L_7;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_8 = V_0;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_9 = V_1;
		if ((!(((RuntimeObject*)(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*)L_8) == ((RuntimeObject*)(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*)L_9))))
		{
			goto IL_0006;
		}
	}
	{
		return;
	}
}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::remove_onScriptEvent(UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_remove_onScriptEvent_mD088B03109E2D439460802F6C9010CCBA5696C0E (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* ___value0, const RuntimeMethod* method) 
{
	static bool s_Il2CppMethodInitialized;
	if (!s_Il2CppMethodInitialized)
	{
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var);
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1_il2cpp_TypeInfo_var);
		s_Il2CppMethodInitialized = true;
	}
	ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* V_0 = NULL;
	ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* V_1 = NULL;
	ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* V_2 = NULL;
	{
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_0 = ((MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_StaticFields*)il2cpp_codegen_static_fields_for(MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var))->___onScriptEvent_16;
		V_0 = L_0;
	}

IL_0006:
	{
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_1 = V_0;
		V_1 = L_1;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_2 = V_1;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_3 = ___value0;
		Delegate_t* L_4;
		L_4 = Delegate_Remove_m40506877934EC1AD4ADAE57F5E97AF0BC0F96116(L_2, L_3, NULL);
		V_2 = ((ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*)CastclassSealed((RuntimeObject*)L_4, ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1_il2cpp_TypeInfo_var));
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_5 = V_2;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_6 = V_1;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_7;
		L_7 = InterlockedCompareExchangeImpl<ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*>((&((MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_StaticFields*)il2cpp_codegen_static_fields_for(MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var))->___onScriptEvent_16), L_5, L_6);
		V_0 = L_7;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_8 = V_0;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_9 = V_1;
		if ((!(((RuntimeObject*)(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*)L_8) == ((RuntimeObject*)(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*)L_9))))
		{
			goto IL_0006;
		}
	}
	{
		return;
	}
}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::ReceiveScriptEvent(UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEvent,System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_ReceiveScriptEvent_m02DD920C8DD9F0F69295FF330269F1D3C1EBC49C (int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method) 
{
	static bool s_Il2CppMethodInitialized;
	if (!s_Il2CppMethodInitialized)
	{
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var);
		s_Il2CppMethodInitialized = true;
	}
	ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* G_B2_0 = NULL;
	ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* G_B1_0 = NULL;
	{
		// private static void ReceiveScriptEvent (ScriptEvent evt, ulong param) => onScriptEvent?.Invoke(evt, param);
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_0 = ((MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_StaticFields*)il2cpp_codegen_static_fields_for(MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var))->___onScriptEvent_16;
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_1 = L_0;
		G_B1_0 = L_1;
		if (L_1)
		{
			G_B2_0 = L_1;
			goto IL_000a;
		}
	}
	{
		return;
	}

IL_000a:
	{
		int32_t L_2 = ___evt0;
		uint64_t L_3 = ___param1;
		NullCheck(G_B2_0);
		ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_inline(G_B2_0, L_2, L_3, NULL);
		return;
	}
}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::ResetDefaults()
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_ResetDefaults_m984AC5CC5DF2D8D18685841223D92A731E09EFFE (const RuntimeMethod* method) 
{
	static bool s_Il2CppMethodInitialized;
	if (!s_Il2CppMethodInitialized)
	{
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var);
		s_Il2CppMethodInitialized = true;
	}
	{
		// onScriptEvent = null;
		((MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_StaticFields*)il2cpp_codegen_static_fields_for(MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var))->___onScriptEvent_16 = (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*)NULL;
		Il2CppCodeGenWriteBarrier((void**)(&((MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_StaticFields*)il2cpp_codegen_static_fields_for(MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17_il2cpp_TypeInfo_var))->___onScriptEvent_16), (void*)(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*)NULL);
		// }
		return;
	}
}
// System.Boolean UnityEngine.XR.OpenXR.Features.Mock.MockDriver::OnInstanceCreate(System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR bool MockDriver_OnInstanceCreate_m01CA03B92AB32798628277CF52491CDFEDF62007 (MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17* __this, uint64_t ___instance0, const RuntimeMethod* method) 
{
	static bool s_Il2CppMethodInitialized;
	if (!s_Il2CppMethodInitialized)
	{
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&Debug_t8394C7EEAECA3689C2C9B9DE9C7166D73596276F_il2cpp_TypeInfo_var);
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&MockDriver_ReceiveScriptEvent_m02DD920C8DD9F0F69295FF330269F1D3C1EBC49C_RuntimeMethod_var);
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1_il2cpp_TypeInfo_var);
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&_stringLiteral1FDC7B050699D12543255FBE775FDDC07F9A1BF3);
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&_stringLiteral3BFAF67BC1D43F33C94D76E23C8F313BD41DDBFF);
		s_Il2CppMethodInitialized = true;
	}
	{
		// if (!OpenXRRuntime.IsExtensionEnabled("XR_UNITY_mock_driver"))
		bool L_0;
		L_0 = OpenXRRuntime_IsExtensionEnabled_m843EDD466C2EFA0E1C1350621411522290C74716(_stringLiteral3BFAF67BC1D43F33C94D76E23C8F313BD41DDBFF, NULL);
		if (L_0)
		{
			goto IL_0018;
		}
	}
	{
		// Debug.LogWarning("XR_UNITY_mock_driver is not enabled, disabling Mock Driver.");
		il2cpp_codegen_runtime_class_init_inline(Debug_t8394C7EEAECA3689C2C9B9DE9C7166D73596276F_il2cpp_TypeInfo_var);
		Debug_LogWarning_mEF15C6B17CE4E1FA7E379CDB82CE40FCD89A3F28(_stringLiteral1FDC7B050699D12543255FBE775FDDC07F9A1BF3, NULL);
		// return false;
		return (bool)0;
	}

IL_0018:
	{
		// InitializeNative(xrGetInstanceProcAddr, instance, 0ul, 0ul);
		intptr_t L_1;
		L_1 = OpenXRFeature_get_xrGetInstanceProcAddr_m616F5709A63844DA12D409E8FEF4929EFA9F5B22(NULL);
		uint64_t L_2 = ___instance0;
		intptr_t L_3;
		L_3 = MockDriver_InitializeNative_mFF63260B5E7354460BFFA8654A178000C65CA0F2(L_1, L_2, ((int64_t)0), ((int64_t)0), NULL);
		// MockDriver_RegisterScriptEventCallback(ReceiveScriptEvent);
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* L_4 = (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*)il2cpp_codegen_object_new(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1_il2cpp_TypeInfo_var);
		NullCheck(L_4);
		ScriptEventDelegate__ctor_mD5F27EA5643A1BD3D22D66C3D4FE89799B70930E(L_4, NULL, (intptr_t)((void*)MockDriver_ReceiveScriptEvent_m02DD920C8DD9F0F69295FF330269F1D3C1EBC49C_RuntimeMethod_var), NULL);
		int32_t L_5;
		L_5 = MockDriver_MockDriver_RegisterScriptEventCallback_m39C8E09B89D20375AF2DD3C8ACAD633B053C9779(L_4, NULL);
		// return true;
		return (bool)1;
	}
}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::OnInstanceDestroy(System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_OnInstanceDestroy_m2DC29C9BCC7AFBD22828418B655E30A582A55BBE (MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17* __this, uint64_t ___xrInstance0, const RuntimeMethod* method) 
{
	{
		// ShutdownNative(0);
		intptr_t L_0;
		L_0 = MockDriver_ShutdownNative_m9DEB4E32813F4F3AB8E57262727EA0366BEF5CF1(((int64_t)0), NULL);
		// }
		return;
	}
}
// System.IntPtr UnityEngine.XR.OpenXR.Features.Mock.MockDriver::InitializeNative(System.IntPtr,System.UInt64,System.UInt64,System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR intptr_t MockDriver_InitializeNative_mFF63260B5E7354460BFFA8654A178000C65CA0F2 (intptr_t ___xrGetInstanceProcAddr0, uint64_t ___xrInstance1, uint64_t ___session2, uint64_t ___sceneSpace3, const RuntimeMethod* method) 
{
	typedef intptr_t (DEFAULT_CALL *PInvokeFunc) (intptr_t, uint64_t, uint64_t, uint64_t);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(intptr_t) + sizeof(uint64_t) + sizeof(uint64_t) + sizeof(uint64_t);
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "script_initialize", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	intptr_t returnValue = reinterpret_cast<PInvokeFunc>(script_initialize)(___xrGetInstanceProcAddr0, ___xrInstance1, ___session2, ___sceneSpace3);
	#else
	intptr_t returnValue = il2cppPInvokeFunc(___xrGetInstanceProcAddr0, ___xrInstance1, ___session2, ___sceneSpace3);
	#endif

	return returnValue;
}
// System.IntPtr UnityEngine.XR.OpenXR.Features.Mock.MockDriver::ShutdownNative(System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR intptr_t MockDriver_ShutdownNative_m9DEB4E32813F4F3AB8E57262727EA0366BEF5CF1 (uint64_t ___xrInstance0, const RuntimeMethod* method) 
{
	typedef intptr_t (DEFAULT_CALL *PInvokeFunc) (uint64_t);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(uint64_t);
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "script_shutdown", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	intptr_t returnValue = reinterpret_cast<PInvokeFunc>(script_shutdown)(___xrInstance0);
	#else
	intptr_t returnValue = il2cppPInvokeFunc(___xrInstance0);
	#endif

	return returnValue;
}
// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrResult UnityEngine.XR.OpenXR.Features.Mock.MockDriver::TransitionToState(System.UInt64,UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrSessionState,System.Boolean)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR int32_t MockDriver_TransitionToState_mEDE90B52FD274B965A9BEF9347E9888380F21FF6 (uint64_t ___xrSession0, int32_t ___state1, bool ___forceTransition2, const RuntimeMethod* method) 
{
	typedef int32_t (DEFAULT_CALL *PInvokeFunc) (uint64_t, int32_t, int32_t);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(uint64_t) + sizeof(int32_t) + 4;
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_TransitionMockToState", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	int32_t returnValue = reinterpret_cast<PInvokeFunc>(MockDriver_TransitionMockToState)(___xrSession0, ___state1, static_cast<int32_t>(___forceTransition2));
	#else
	int32_t returnValue = il2cppPInvokeFunc(___xrSession0, ___state1, static_cast<int32_t>(___forceTransition2));
	#endif

	return returnValue;
}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::SetReturnCodeForFunction(System.String,UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrResult)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_SetReturnCodeForFunction_m85907D6CB58649AF5146563F46DFD008D03846A8 (String_t* ___functionName0, int32_t ___result1, const RuntimeMethod* method) 
{
	typedef void (DEFAULT_CALL *PInvokeFunc) (char*, int32_t);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(char*) + sizeof(int32_t);
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_SetReturnCodeForFunction", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Marshaling of parameter '___functionName0' to native representation
	char* ____functionName0_marshaled = NULL;
	____functionName0_marshaled = il2cpp_codegen_marshal_string(___functionName0);

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	reinterpret_cast<PInvokeFunc>(MockDriver_SetReturnCodeForFunction)(____functionName0_marshaled, ___result1);
	#else
	il2cppPInvokeFunc(____functionName0_marshaled, ___result1);
	#endif

	// Marshaling cleanup of parameter '___functionName0' native representation
	il2cpp_codegen_marshal_free(____functionName0_marshaled);
	____functionName0_marshaled = NULL;

}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::RequestExitSession(System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_RequestExitSession_m5B91A45E4A2C818F39A35DE3DA20F6A43A0F64C3 (uint64_t ___session0, const RuntimeMethod* method) 
{
	typedef void (DEFAULT_CALL *PInvokeFunc) (uint64_t);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(uint64_t);
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_RequestExitSession", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	reinterpret_cast<PInvokeFunc>(MockDriver_RequestExitSession)(___session0);
	#else
	il2cppPInvokeFunc(___session0);
	#endif

}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::SetBlendModeOpaque(System.Boolean)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_SetBlendModeOpaque_m79B09E6E1EE4F7C3ACC674D81DBB35F646890EFE (bool ___opaque0, const RuntimeMethod* method) 
{
	typedef void (DEFAULT_CALL *PInvokeFunc) (int32_t);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = 4;
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_SetBlendModeOpaque", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	reinterpret_cast<PInvokeFunc>(MockDriver_SetBlendModeOpaque)(static_cast<int32_t>(___opaque0));
	#else
	il2cppPInvokeFunc(static_cast<int32_t>(___opaque0));
	#endif

}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::SetReferenceSpaceBoundsRect(System.UInt64,UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrReferenceSpaceType,UnityEngine.Vector2)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_SetReferenceSpaceBoundsRect_mCBC4272D25E7760EFC481525B735370B3342C7E4 (uint64_t ___session0, int32_t ___referenceSpace1, Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7 ___bounds2, const RuntimeMethod* method) 
{
	typedef void (DEFAULT_CALL *PInvokeFunc) (uint64_t, int32_t, Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(uint64_t) + sizeof(int32_t) + sizeof(Vector2_t1FD6F485C871E832B347AB2DC8CBA08B739D8DF7);
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_SetReferenceSpaceBoundsRect", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	reinterpret_cast<PInvokeFunc>(MockDriver_SetReferenceSpaceBoundsRect)(___session0, ___referenceSpace1, ___bounds2);
	#else
	il2cppPInvokeFunc(___session0, ___referenceSpace1, ___bounds2);
	#endif

}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::CauseInstanceLoss(System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver_CauseInstanceLoss_m4D094A34CF798E26DF0903E9EA53A40E50669963 (uint64_t ___instance0, const RuntimeMethod* method) 
{
	typedef void (DEFAULT_CALL *PInvokeFunc) (uint64_t);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(uint64_t);
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_CauseInstanceLoss", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	reinterpret_cast<PInvokeFunc>(MockDriver_CauseInstanceLoss)(___instance0);
	#else
	il2cppPInvokeFunc(___instance0);
	#endif

}
// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrResult UnityEngine.XR.OpenXR.Features.Mock.MockDriver::SetSpacePose(UnityEngine.Quaternion,UnityEngine.Vector3,UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrSpaceLocationFlags)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR int32_t MockDriver_SetSpacePose_mA8C0172899597D0AC690EAC0765000F77B5E5CCA (Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974 ___orientation0, Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___position1, int32_t ___locationSpaceFlags2, const RuntimeMethod* method) 
{
	typedef int32_t (DEFAULT_CALL *PInvokeFunc) (Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974, Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2, int32_t);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974) + sizeof(Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2) + sizeof(int32_t);
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_SetSpacePose", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	int32_t returnValue = reinterpret_cast<PInvokeFunc>(MockDriver_SetSpacePose)(___orientation0, ___position1, ___locationSpaceFlags2);
	#else
	int32_t returnValue = il2cppPInvokeFunc(___orientation0, ___position1, ___locationSpaceFlags2);
	#endif

	return returnValue;
}
// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrResult UnityEngine.XR.OpenXR.Features.Mock.MockDriver::SetViewPose(System.Int32,UnityEngine.Quaternion,UnityEngine.Vector3,UnityEngine.Vector4,UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrViewStateFlags)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR int32_t MockDriver_SetViewPose_mF7C2DE8F433394B478E0C9EF2A340B75AB23AF1A (int32_t ___viewIndex0, Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974 ___orientation1, Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2 ___position2, Vector4_t58B63D32F48C0DBF50DE2C60794C4676C80EDBE3 ___fov3, int32_t ___viewStateFlags4, const RuntimeMethod* method) 
{
	typedef int32_t (DEFAULT_CALL *PInvokeFunc) (int32_t, Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974, Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2, Vector4_t58B63D32F48C0DBF50DE2C60794C4676C80EDBE3, int32_t);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(int32_t) + sizeof(Quaternion_tDA59F214EF07D7700B26E40E562F267AF7306974) + sizeof(Vector3_t24C512C7B96BBABAD472002D0BA2BDA40A5A80B2) + sizeof(Vector4_t58B63D32F48C0DBF50DE2C60794C4676C80EDBE3) + sizeof(int32_t);
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_SetViewPose", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	int32_t returnValue = reinterpret_cast<PInvokeFunc>(MockDriver_SetViewPose)(___viewIndex0, ___orientation1, ___position2, ___fov3, ___viewStateFlags4);
	#else
	int32_t returnValue = il2cppPInvokeFunc(___viewIndex0, ___orientation1, ___position2, ___fov3, ___viewStateFlags4);
	#endif

	return returnValue;
}
// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrResult UnityEngine.XR.OpenXR.Features.Mock.MockDriver::GetEndFrameStats(System.Int32&,System.Int32&)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR int32_t MockDriver_GetEndFrameStats_m2E2210BA154A3C1C5AB7EAD47F1D661E7AB11F74 (int32_t* ___primaryLayerCount0, int32_t* ___secondaryLayerCount1, const RuntimeMethod* method) 
{
	typedef int32_t (DEFAULT_CALL *PInvokeFunc) (int32_t*, int32_t*);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(int32_t*) + sizeof(int32_t*);
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_GetEndFrameStats", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	int32_t returnValue = reinterpret_cast<PInvokeFunc>(MockDriver_GetEndFrameStats)(___primaryLayerCount0, ___secondaryLayerCount1);
	#else
	int32_t returnValue = il2cppPInvokeFunc(___primaryLayerCount0, ___secondaryLayerCount1);
	#endif

	return returnValue;
}
// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrResult UnityEngine.XR.OpenXR.Features.Mock.MockDriver::ActivateSecondaryView(UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrViewConfigurationType,System.Boolean)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR int32_t MockDriver_ActivateSecondaryView_m95E311D16A9D44C118773AFE9431005F1AA6EE49 (int32_t ___viewConfigurationType0, bool ___activate1, const RuntimeMethod* method) 
{
	typedef int32_t (DEFAULT_CALL *PInvokeFunc) (int32_t, int32_t);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(int32_t) + 4;
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_ActivateSecondaryView", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	int32_t returnValue = reinterpret_cast<PInvokeFunc>(MockDriver_ActivateSecondaryView)(___viewConfigurationType0, static_cast<int32_t>(___activate1));
	#else
	int32_t returnValue = il2cppPInvokeFunc(___viewConfigurationType0, static_cast<int32_t>(___activate1));
	#endif

	return returnValue;
}
// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/XrResult UnityEngine.XR.OpenXR.Features.Mock.MockDriver::MockDriver_RegisterScriptEventCallback(UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR int32_t MockDriver_MockDriver_RegisterScriptEventCallback_m39C8E09B89D20375AF2DD3C8ACAD633B053C9779 (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* ___callback0, const RuntimeMethod* method) 
{
	typedef int32_t (DEFAULT_CALL *PInvokeFunc) (Il2CppMethodPointer);
	#if !FORCE_PINVOKE_INTERNAL && !FORCE_PINVOKE_mock_driver_INTERNAL
	static PInvokeFunc il2cppPInvokeFunc;
	if (il2cppPInvokeFunc == NULL)
	{
		int parameterSize = sizeof(void*);
		il2cppPInvokeFunc = il2cpp_codegen_resolve_pinvoke<PInvokeFunc>(IL2CPP_NATIVE_STRING("mock_driver"), "MockDriver_RegisterScriptEventCallback", IL2CPP_CALL_DEFAULT, CHARSET_NOT_SPECIFIED, parameterSize, false);
		IL2CPP_ASSERT(il2cppPInvokeFunc != NULL);
	}
	#endif

	// Marshaling of parameter '___callback0' to native representation
	Il2CppMethodPointer ____callback0_marshaled = NULL;
	____callback0_marshaled = il2cpp_codegen_marshal_delegate(reinterpret_cast<MulticastDelegate_t*>(___callback0));

	// Native function invocation
	#if FORCE_PINVOKE_INTERNAL || FORCE_PINVOKE_mock_driver_INTERNAL
	int32_t returnValue = reinterpret_cast<PInvokeFunc>(MockDriver_RegisterScriptEventCallback)(____callback0_marshaled);
	#else
	int32_t returnValue = il2cppPInvokeFunc(____callback0_marshaled);
	#endif

	return returnValue;
}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver::.ctor()
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void MockDriver__ctor_mE889E30F05CE8D83BBD6BF503808F1B7FB58912D (MockDriver_tC0F7ED242EF63DA7803BDB4A5DA7121BE53DEC17* __this, const RuntimeMethod* method) 
{
	{
		OpenXRFeature__ctor_m120460E34ECC22ED2DB96797A6DCB5C870E78852(__this, NULL);
		return;
	}
}
#ifdef __clang__
#pragma clang diagnostic pop
#endif
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif
#ifdef __clang__
#pragma clang diagnostic pop
#endif
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif
void ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_Multicast(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method)
{
	il2cpp_array_size_t length = __this->___delegates_13->max_length;
	Delegate_t** delegatesToInvoke = reinterpret_cast<Delegate_t**>(__this->___delegates_13->GetAddressAtUnchecked(0));
	typedef void (*FunctionPointerType) (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method);
	for (il2cpp_array_size_t i = 0; i < length; i++)
	{
		ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* currentDelegate = reinterpret_cast<ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1*>(delegatesToInvoke[i]);
		((FunctionPointerType)currentDelegate->___invoke_impl_1)(currentDelegate, ___evt0, ___param1, method);
	}
}
void ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_Open(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method)
{
	typedef void (*FunctionPointerType) (int32_t, uint64_t, const RuntimeMethod*);
	((FunctionPointerType)__this->___method_ptr_0)(___evt0, ___param1, method);
}
void ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_Closed(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method)
{
	typedef void (*FunctionPointerType) (RuntimeObject*, int32_t, uint64_t, const RuntimeMethod*);
	((FunctionPointerType)__this->___method_ptr_0)(__this->___m_target_2, ___evt0, ___param1, method);
}
void ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_OpenStaticInvoker(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method)
{
	InvokerActionInvoker2< int32_t, uint64_t >::Invoke(__this->___method_ptr_0, method, NULL, ___evt0, ___param1);
}
void ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_ClosedStaticInvoker(ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method)
{
	InvokerActionInvoker3< RuntimeObject*, int32_t, uint64_t >::Invoke(__this->___method_ptr_0, method, NULL, __this->___m_target_2, ___evt0, ___param1);
}
IL2CPP_EXTERN_C  void DelegatePInvokeWrapper_ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1 (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method)
{
	typedef void (DEFAULT_CALL *PInvokeFunc)(int32_t, uint64_t);
	PInvokeFunc il2cppPInvokeFunc = reinterpret_cast<PInvokeFunc>(il2cpp_codegen_get_reverse_pinvoke_function_ptr(__this));
	// Native function invocation
	il2cppPInvokeFunc(___evt0, ___param1);

}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate::.ctor(System.Object,System.IntPtr)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void ScriptEventDelegate__ctor_mD5F27EA5643A1BD3D22D66C3D4FE89799B70930E (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, RuntimeObject* ___object0, intptr_t ___method1, const RuntimeMethod* method) 
{
	__this->___method_ptr_0 = il2cpp_codegen_get_virtual_call_method_pointer((RuntimeMethod*)___method1);
	__this->___method_3 = ___method1;
	__this->___m_target_2 = ___object0;
	Il2CppCodeGenWriteBarrier((void**)(&__this->___m_target_2), (void*)___object0);
	int methodCount = il2cpp_codegen_method_parameter_count((RuntimeMethod*)___method1);
	if (MethodIsStatic((RuntimeMethod*)___method1))
	{
		bool isOpen = methodCount == 2;
		if (il2cpp_codegen_call_method_via_invoker((RuntimeMethod*)___method1))
			if (isOpen)
				__this->___invoke_impl_1 = (intptr_t)&ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_OpenStaticInvoker;
			else
				__this->___invoke_impl_1 = (intptr_t)&ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_ClosedStaticInvoker;
		else
			if (isOpen)
				__this->___invoke_impl_1 = (intptr_t)&ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_Open;
			else
				__this->___invoke_impl_1 = (intptr_t)&ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_Closed;
	}
	else
	{
		__this->___invoke_impl_1 = (intptr_t)&ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_Closed;
	}
	__this->___extra_arg_5 = (intptr_t)&ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_Multicast;
}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate::Invoke(UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEvent,System.UInt64)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290 (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method) 
{
	typedef void (*FunctionPointerType) (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method);
	((FunctionPointerType)__this->___invoke_impl_1)(__this, ___evt0, ___param1, reinterpret_cast<RuntimeMethod*>(__this->___method_3));
}
// System.IAsyncResult UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate::BeginInvoke(UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEvent,System.UInt64,System.AsyncCallback,System.Object)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR RuntimeObject* ScriptEventDelegate_BeginInvoke_mBD33067DC810E8403C0A181C32F5C25827C39F7B (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, AsyncCallback_t7FEF460CBDCFB9C5FA2EF776984778B9A4145F4C* ___callback2, RuntimeObject* ___object3, const RuntimeMethod* method) 
{
	static bool s_Il2CppMethodInitialized;
	if (!s_Il2CppMethodInitialized)
	{
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&ScriptEvent_t99C1B1F4925AFADF949EC80C822FC611B67B3BD5_il2cpp_TypeInfo_var);
		il2cpp_codegen_initialize_runtime_metadata((uintptr_t*)&UInt64_t8F12534CC8FC4B5860F2A2CD1EE79D322E7A41AF_il2cpp_TypeInfo_var);
		s_Il2CppMethodInitialized = true;
	}
	void *__d_args[3] = {0};
	__d_args[0] = Box(ScriptEvent_t99C1B1F4925AFADF949EC80C822FC611B67B3BD5_il2cpp_TypeInfo_var, &___evt0);
	__d_args[1] = Box(UInt64_t8F12534CC8FC4B5860F2A2CD1EE79D322E7A41AF_il2cpp_TypeInfo_var, &___param1);
	return (RuntimeObject*)il2cpp_codegen_delegate_begin_invoke((RuntimeDelegate*)__this, __d_args, (RuntimeDelegate*)___callback2, (RuntimeObject*)___object3);;
}
// System.Void UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEventDelegate::EndInvoke(System.IAsyncResult)
IL2CPP_EXTERN_C IL2CPP_METHOD_ATTR void ScriptEventDelegate_EndInvoke_m171A46B00641A3F417792C9C4B0DCF8DE6F4EA73 (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, RuntimeObject* ___result0, const RuntimeMethod* method) 
{
	il2cpp_codegen_delegate_end_invoke((Il2CppAsyncResult*) ___result0, 0);
}
#ifdef __clang__
#pragma clang diagnostic pop
#endif
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif
#ifdef __clang__
#pragma clang diagnostic pop
#endif
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif
#ifdef __clang__
#pragma clang diagnostic pop
#endif
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif
#ifdef __clang__
#pragma clang diagnostic pop
#endif
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif
#ifdef __clang__
#pragma clang diagnostic pop
#endif
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif
#ifdef __clang__
#pragma clang diagnostic pop
#endif
#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif
#ifdef __clang__
#pragma clang diagnostic pop
#endif
IL2CPP_MANAGED_FORCE_INLINE IL2CPP_METHOD_ATTR void ScriptEventDelegate_Invoke_mF63E757B2FD4E7B9D821D78385550716E7A20290_inline (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method) 
{
	typedef void (*FunctionPointerType) (ScriptEventDelegate_tAB5700EBE916CEAE5D6AC378A39A837AC2BC90B1* __this, int32_t ___evt0, uint64_t ___param1, const RuntimeMethod* method);
	((FunctionPointerType)__this->___invoke_impl_1)(__this, ___evt0, ___param1, reinterpret_cast<RuntimeMethod*>(__this->___method_3));
}
