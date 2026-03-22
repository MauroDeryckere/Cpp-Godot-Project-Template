file(GLOB_RECURSE SRC CONFIGURE_DEPENDS src/*.cpp)

add_library(myextension SHARED ${SRC})

target_compile_features(myextension PRIVATE cxx_std_20)
set_target_properties(myextension PROPERTIES CXX_EXTENSIONS OFF)

if(WIN32)
    set_target_properties(myextension PROPERTIES PREFIX "")
endif()

target_include_directories(myextension PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)


target_link_libraries(myextension PRIVATE
    godot-cpp
)

# Suppress warnings from godot-cpp headers
get_target_property(GODOT_CPP_INCLUDE_DIRS godot-cpp INTERFACE_INCLUDE_DIRECTORIES)
target_include_directories(myextension SYSTEM PRIVATE ${GODOT_CPP_INCLUDE_DIRS})

if(CMAKE_SYSTEM_NAME STREQUAL "iOS")
    set_target_properties(myextension PROPERTIES
        XCODE_ATTRIBUTE_CODE_SIGNING_ALLOWED "NO"
    )
endif()

# Determine output directory based on platform
if(ANDROID)
    set(BIN_OUTPUT_DIR ${PROJECT_SOURCE_DIR}/godot/bin/android/${ANDROID_ABI})
elseif(CMAKE_SYSTEM_NAME STREQUAL "iOS")
    set(BIN_OUTPUT_DIR ${PROJECT_SOURCE_DIR}/godot/bin/ios)
else()
    set(BIN_OUTPUT_DIR ${PROJECT_SOURCE_DIR}/godot/bin)
endif()

# Output directly to Godot project
add_custom_command(TARGET myextension POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E make_directory ${BIN_OUTPUT_DIR}
    COMMAND ${CMAKE_COMMAND} -E copy_if_different
    $<TARGET_FILE:myextension>
    ${BIN_OUTPUT_DIR}/
)

if(MSVC)
    add_custom_command(TARGET myextension POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different
        $<TARGET_PDB_FILE:myextension>
        ${BIN_OUTPUT_DIR}/
    )
endif()
