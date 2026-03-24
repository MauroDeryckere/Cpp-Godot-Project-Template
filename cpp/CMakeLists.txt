file(GLOB_RECURSE SRC CONFIGURE_DEPENDS src/*.cpp)

add_library(${EXTENSION_NAME} SHARED ${SRC})

target_compile_features(${EXTENSION_NAME} PRIVATE cxx_std_20)

target_compile_options(${EXTENSION_NAME} PRIVATE
    $<$<CXX_COMPILER_ID:MSVC>:/W4>
    $<$<NOT:$<CXX_COMPILER_ID:MSVC>>:-Wall -Wextra -Wpedantic>
)

# Optional static analysis (enable with -DUSE_CPPCHECK=ON or -DUSE_IWYU=ON)
if(USE_CPPCHECK)
    find_program(CPPCHECK_PROGRAM cppcheck)
    if(CPPCHECK_PROGRAM)
        set_target_properties(${EXTENSION_NAME} PROPERTIES
            CXX_CPPCHECK "${CPPCHECK_PROGRAM};--std=c++20;--quiet;--suppress=missingIncludeSystem"
        )
    endif()
endif()

if(USE_IWYU)
    find_program(IWYU_PROGRAM include-what-you-use)
    if(IWYU_PROGRAM)
        set_target_properties(${EXTENSION_NAME} PROPERTIES
            CXX_INCLUDE_WHAT_YOU_USE "${IWYU_PROGRAM}"
        )
    endif()
endif()

target_include_directories(${EXTENSION_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(${EXTENSION_NAME} PRIVATE
    godot-cpp
)

# Suppress warnings from godot-cpp headers
get_target_property(GODOT_CPP_INCLUDE_DIRS godot-cpp INTERFACE_INCLUDE_DIRECTORIES)
target_include_directories(${EXTENSION_NAME} SYSTEM PRIVATE ${GODOT_CPP_INCLUDE_DIRS})

# Compile class documentation into debug builds (shows in Godot's built-in help)
if(GODOTCPP_TARGET MATCHES "editor|template_debug")
    file(GLOB_RECURSE DOC_XML CONFIGURE_DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/doc_classes/*.xml)
    if(DOC_XML)
        # Generate at configure time to avoid sccache race conditions with build-time generation
        set(DOC_SOURCE_FILE "${CMAKE_CURRENT_BINARY_DIR}/gen/doc_source.cpp")
        file(MAKE_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/gen")

        set(PYTHON_LIST "")
        foreach(XML_FILE ${DOC_XML})
            if(PYTHON_LIST)
                string(APPEND PYTHON_LIST ",")
            endif()
            string(APPEND PYTHON_LIST "'${XML_FILE}'")
        endforeach()

        execute_process(
            COMMAND "${Python3_EXECUTABLE}" "-c"
                "from doc_source_generator import generate_doc_source; generate_doc_source('${DOC_SOURCE_FILE}', [${PYTHON_LIST}])"
            WORKING_DIRECTORY "${PROJECT_SOURCE_DIR}/third_party/godot-cpp"
            RESULT_VARIABLE DOC_GEN_RESULT
        )

        if(DOC_GEN_RESULT EQUAL 0 AND EXISTS "${DOC_SOURCE_FILE}")
            target_sources(${EXTENSION_NAME} PRIVATE "${DOC_SOURCE_FILE}")
        else()
            message(WARNING "Failed to generate doc sources, skipping documentation compilation")
        endif()
    endif()
endif()

# Generate .gdextension file from template
configure_file(
    ${PROJECT_SOURCE_DIR}/godot/project/extension.gdextension.in
    ${PROJECT_SOURCE_DIR}/godot/project/${EXTENSION_NAME}.gdextension
    @ONLY
)

# Use godot-cpp suffix for output naming (e.g. myextension.linux.template_debug.x86_64.so)
get_target_property(GODOTCPP_SUFFIX godot-cpp GODOTCPP_SUFFIX)

# Determine output directory based on platform
if(ANDROID)
    set(BIN_OUTPUT_DIR ${PROJECT_SOURCE_DIR}/godot/bin/android/${ANDROID_ABI})
elseif(CMAKE_SYSTEM_NAME STREQUAL "iOS")
    set(BIN_OUTPUT_DIR ${PROJECT_SOURCE_DIR}/godot/bin/ios)
else()
    set(BIN_OUTPUT_DIR ${PROJECT_SOURCE_DIR}/godot/bin)
endif()

set_target_properties(${EXTENSION_NAME} PROPERTIES
    CXX_EXTENSIONS OFF
    POSITION_INDEPENDENT_CODE ON
    CXX_VISIBILITY_PRESET hidden
    VISIBILITY_INLINES_HIDDEN ON

    PREFIX "lib"
    OUTPUT_NAME "${EXTENSION_NAME}${GODOTCPP_SUFFIX}"

    LIBRARY_OUTPUT_DIRECTORY "$<1:${BIN_OUTPUT_DIR}>"
    RUNTIME_OUTPUT_DIRECTORY "$<1:${BIN_OUTPUT_DIR}>"
    PDB_OUTPUT_DIRECTORY "$<1:${BIN_OUTPUT_DIR}>"
)

if(CMAKE_SYSTEM_NAME STREQUAL "iOS")
    set_target_properties(${EXTENSION_NAME} PROPERTIES
        XCODE_ATTRIBUTE_CODE_SIGNING_ALLOWED "NO"
    )
endif()

# Copy MinGW runtime DLLs next to the extension so Godot can find them
if(MINGW)
    foreach(DLL_NAME libgcc_s_seh-1.dll libstdc++-6.dll libwinpthread-1.dll)
        find_file(${DLL_NAME}_PATH ${DLL_NAME} PATHS ${CMAKE_CXX_COMPILER}/../ NO_DEFAULT_PATH)
        if(${DLL_NAME}_PATH)
            add_custom_command(TARGET ${EXTENSION_NAME} POST_BUILD
                COMMAND ${CMAKE_COMMAND} -E copy_if_different
                    "${${DLL_NAME}_PATH}" "${BIN_OUTPUT_DIR}"
            )
        endif()
    endforeach()
endif()
