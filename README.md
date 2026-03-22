# Godot C++ Project Template

A ready-to-use template for Godot 4.6 projects with C++ GDExtension support. Includes CMake build system, cross-platform presets, unit testing, CI workflows, and release automation.

## Prerequisites

- [Godot 4.6+](https://godotengine.org/download)
- [CMake 3.20+](https://cmake.org/download/)
- [Ninja](https://ninja-build.org/) (or another CMake-supported generator)
- A C++20 compiler (MSVC, GCC, Clang)
- (Optional) [ccache](https://ccache.dev/) or [sccache](https://github.com/mozilla/sccache) for faster rebuilds — auto-detected by CMake

For mobile builds:
- **Android**: [Android NDK](https://developer.android.com/ndk) with `ANDROID_NDK_ROOT` environment variable set
- **iOS**: Xcode with iOS SDK

## Getting Started

```bash
git clone --recursive https://github.com/MauroDeryckere/Godot-Project-Template.git
cd Godot-Project-Template
```

Rename the extension and project to match yours:
```bash
python tools/rename_extension.py myextension your_extension_name
python tools/rename_project.py "Your Project Name"
```

The extension name is defined once in `CMakeLists.txt` as `EXTENSION_NAME`. The `.gdextension` file is auto-generated from `extension.gdextension.in` at configure time — no manual editing needed.

## Building

### Desktop

```bash
cmake --preset debug
cmake --build --preset debug
```

Available presets: `debug`, `release`, `dist` (RelWithDebInfo)

### Android

```bash
cmake --preset android-arm64
cmake --build --preset android-arm64
```

Available presets: `android-arm64`, `android-arm32`, `android-x86_64` (and `-debug` variants for each)

### iOS

```bash
cmake --preset ios
cmake --build --preset ios
```

Available presets: `ios`, `ios-debug`

Built binaries are output to `godot/bin/` with platform and build type suffixes (e.g. `libmyextension.windows.template_debug.x86_64.dll`).

## Running

Open `godot/project/project.godot` in the Godot editor.

## Testing

```bash
cmake --preset debug -DBUILD_TESTS=ON
cmake --build --preset debug
ctest --preset debug
```

Tests use [Catch2](https://github.com/catchorg/Catch2) and cover pure C++ code (non-Godot classes). Add test files to `tests/src/`.

## Project Structure

```
├── cpp/                           C++ extension source code
│   ├── include/                   Headers
│   ├── src/                       Implementation + register_types.cpp
│   └── doc_classes/               XML class docs (compiled into extension)
├── godot/
│   ├── bin/                       Compiled extension binaries (generated)
│   └── project/
│       ├── project.godot          Godot project configuration
│       └── extension.gdextension.in   .gdextension template (CMake generates the final file)
├── tests/                         Unit tests (Catch2)
├── third_party/godot-cpp/         Godot C++ bindings (submodule)
├── tools/
│   ├── rename_extension.py        Rename the GDExtension throughout the project
│   └── rename_project.py          Rename the Godot project
├── CMakeLists.txt                 Top-level CMake configuration (EXTENSION_NAME defined here)
└── CMakePresets.json              Build presets (desktop, mobile, debug + release)
```

## Adding a New Class

1. Create your header in `cpp/include/` and source in `cpp/src/`
2. If it's a Godot class, register it in `cpp/src/register_types.cpp`:
   ```cpp
   GDREGISTER_CLASS(YourClass);
   ```
3. (Optional) Add a documentation XML file in `cpp/doc_classes/YourClass.xml` to show help in the Godot editor
4. Rebuild — the extension is automatically output to the Godot project

## CI Workflows

- **CI** (`ci.yml`) — Builds and tests on all desktop platforms, cross-compiles for Android and iOS, and validates the extension loads in headless Godot. Triggered on push to `main` and on pull requests.
- **Build** (`build.yml`) — Builds debug + release binaries for all platforms and collects them as a downloadable artifact. Triggered manually or by pushing a version tag (e.g. `git tag v1.0.0 && git push --tags`) which also creates a GitHub Release.

Both workflows use [sccache](https://github.com/mozilla/sccache) and godot-cpp build caching for faster runs.

## License

[MIT](LICENSE)
