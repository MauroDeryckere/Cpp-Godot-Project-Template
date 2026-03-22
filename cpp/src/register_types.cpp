#include <godot_cpp/godot.hpp>
#include <godot_cpp/core/class_db.hpp>

#include "godot/MyNode.hpp"

using namespace godot;

void initialize(ModuleInitializationLevel level)
{
    if (level != MODULE_INITIALIZATION_LEVEL_SCENE)
    {
        return;
    }

    GDREGISTER_CLASS(MyNode);
}

void uninitialize(ModuleInitializationLevel /*level*/)
{
}

extern "C"
{
    GDExtensionBool GDE_EXPORT myextension_init(
        GDExtensionInterfaceGetProcAddress get_proc_address,
        GDExtensionClassLibraryPtr library,
        GDExtensionInitialization* initialization)
    {
        GDExtensionBinding::InitObject init_obj(get_proc_address, library, initialization);

        init_obj.register_initializer(initialize);
        init_obj.register_terminator(uninitialize);
        init_obj.set_minimum_library_initialization_level(MODULE_INITIALIZATION_LEVEL_SCENE);

        return init_obj.init();
    }
}