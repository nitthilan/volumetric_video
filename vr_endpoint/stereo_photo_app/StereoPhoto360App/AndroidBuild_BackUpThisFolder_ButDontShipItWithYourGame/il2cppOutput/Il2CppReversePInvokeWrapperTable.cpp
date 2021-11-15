#include "pch-cpp.hpp"

#ifndef _MSC_VER
# include <alloca.h>
#else
# include <malloc.h>
#endif


#include <stdint.h>
#include <limits>



// System.Char[]
struct CharU5BU5D_t799905CF001DD5F13F7DBB310181FC4D8B7D0AAB;
// System.String
struct String_t;
// System.Void
struct Void_t4861ACF8F4594C3437BB48B6E56783494B843915;



IL2CPP_EXTERN_C_BEGIN
IL2CPP_EXTERN_C_END

#ifdef __clang__
#pragma clang diagnostic push
#pragma clang diagnostic ignored "-Winvalid-offsetof"
#pragma clang diagnostic ignored "-Wunused-variable"
#endif

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

// UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEvent
struct ScriptEvent_t99C1B1F4925AFADF949EC80C822FC611B67B3BD5 
{
	// System.Int32 UnityEngine.XR.OpenXR.Features.Mock.MockDriver/ScriptEvent::value__
	int32_t ___value___2;
};

// UnityEngine.XR.OpenXR.Features.OpenXRFeature/NativeEvent
struct NativeEvent_t2C54A0DE392B348B223984562B66B06F48BC7F04 
{
	// System.Int32 UnityEngine.XR.OpenXR.Features.OpenXRFeature/NativeEvent::value__
	int32_t ___value___2;
};
#ifdef __clang__
#pragma clang diagnostic pop
#endif

extern "C" void DEFAULT_CALL ReversePInvokeWrapper_CultureInfo_OnCultureInfoChangedInAppX_mDBD419B094B2CFE933BB3F63886A5AB4E44D2DC0(Il2CppChar* ___language0);
extern "C" void DEFAULT_CALL ReversePInvokeWrapper_MockDriver_ReceiveScriptEvent_m02DD920C8DD9F0F69295FF330269F1D3C1EBC49C(int32_t ___evt0, uint64_t ___param1);
extern "C" void DEFAULT_CALL ReversePInvokeWrapper_OSSpecificSynchronizationContext_InvocationEntry_mB85BF0265E239960FC963DCA74DC67EBCE9480AC(intptr_t ___arg0);
extern "C" void DEFAULT_CALL ReversePInvokeWrapper_OpenXRLoaderBase_ReceiveNativeEvent_m1B50DCF4E5D74B8395C1B1E64747B1E8A3DE7AD6(int32_t ___e0, uint64_t ___payload1);


IL2CPP_EXTERN_C const Il2CppMethodPointer g_ReversePInvokeWrapperPointers[];
const Il2CppMethodPointer g_ReversePInvokeWrapperPointers[4] = 
{
	reinterpret_cast<Il2CppMethodPointer>(ReversePInvokeWrapper_CultureInfo_OnCultureInfoChangedInAppX_mDBD419B094B2CFE933BB3F63886A5AB4E44D2DC0),
	reinterpret_cast<Il2CppMethodPointer>(ReversePInvokeWrapper_MockDriver_ReceiveScriptEvent_m02DD920C8DD9F0F69295FF330269F1D3C1EBC49C),
	reinterpret_cast<Il2CppMethodPointer>(ReversePInvokeWrapper_OSSpecificSynchronizationContext_InvocationEntry_mB85BF0265E239960FC963DCA74DC67EBCE9480AC),
	reinterpret_cast<Il2CppMethodPointer>(ReversePInvokeWrapper_OpenXRLoaderBase_ReceiveNativeEvent_m1B50DCF4E5D74B8395C1B1E64747B1E8A3DE7AD6),
};
