cmake_minimum_required(VERSION 3.16)
project(ffmpeg_debug_qp VERSION 0.2.0 LANGUAGES C)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Options
option(STATIC_BUILD "Build with static FFmpeg libraries" OFF)
option(USE_VENDORED_FFMPEG "Use vendored FFmpeg from external/ffmpeg" OFF)

# Source files
set(SOURCES ffmpeg_debug_qp.c)

# Create executable
add_executable(ffmpeg_debug_qp ${SOURCES})

target_compile_options(ffmpeg_debug_qp PRIVATE -Wall)

if(USE_VENDORED_FFMPEG)
    # Use vendored FFmpeg built by util/build-ffmpeg.sh
    set(FFMPEG_DIR "${CMAKE_SOURCE_DIR}/external/ffmpeg")

    if(NOT EXISTS "${FFMPEG_DIR}/libavformat/libavformat.a")
        message(FATAL_ERROR
            "Vendored FFmpeg not found. Run: ./util/build-ffmpeg.sh first")
    endif()

    # Include paths
    target_include_directories(ffmpeg_debug_qp PRIVATE
        ${FFMPEG_DIR}
    )

    # Static libraries - order matters for static linking!
    # Higher-level libs first, then their dependencies
    set(FFMPEG_LIBS
        "${FFMPEG_DIR}/libavformat/libavformat.a"
        "${FFMPEG_DIR}/libavcodec/libavcodec.a"
        "${FFMPEG_DIR}/libavutil/libavutil.a"
    )

    target_link_libraries(ffmpeg_debug_qp PRIVATE ${FFMPEG_LIBS})

    # Platform-specific system libraries needed for static FFmpeg
    if(APPLE)
        find_library(SECURITY_FRAMEWORK Security)
        find_library(COREFOUNDATION_FRAMEWORK CoreFoundation)
        find_library(COREVIDEO_FRAMEWORK CoreVideo)
        find_library(COREMEDIA_FRAMEWORK CoreMedia)
        find_library(VIDEOTOOLBOX_FRAMEWORK VideoToolbox OPTIONAL)

        target_link_libraries(ffmpeg_debug_qp PRIVATE
            ${SECURITY_FRAMEWORK}
            ${COREFOUNDATION_FRAMEWORK}
            ${COREVIDEO_FRAMEWORK}
            ${COREMEDIA_FRAMEWORK}
            z
            bz2
            iconv
            m
        )

        # Only link VideoToolbox if it was enabled during FFmpeg build
        if(VIDEOTOOLBOX_FRAMEWORK)
            # target_link_libraries(ffmpeg_debug_qp PRIVATE ${VIDEOTOOLBOX_FRAMEWORK})
        endif()
    elseif(UNIX)
        # Linux
        target_link_libraries(ffmpeg_debug_qp PRIVATE
            m
            pthread
        )

        if(STATIC_BUILD)
            # For fully static Linux builds (e.g., Alpine/musl)
            set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -static")
        endif()
    endif()

else()
    # Use system FFmpeg via pkg-config
    find_package(PkgConfig REQUIRED)

    pkg_check_modules(AVFORMAT REQUIRED libavformat)
    pkg_check_modules(AVCODEC REQUIRED libavcodec)
    pkg_check_modules(AVUTIL REQUIRED libavutil)

    target_include_directories(ffmpeg_debug_qp PRIVATE
        ${AVFORMAT_INCLUDE_DIRS}
        ${AVCODEC_INCLUDE_DIRS}
        ${AVUTIL_INCLUDE_DIRS}
    )

    if(STATIC_BUILD)
        # Static linking with system FFmpeg (requires static libs installed)
        target_link_libraries(ffmpeg_debug_qp PRIVATE
            ${AVFORMAT_STATIC_LIBRARIES}
            ${AVCODEC_STATIC_LIBRARIES}
            ${AVUTIL_STATIC_LIBRARIES}
        )
    else()
        # Dynamic linking (default)
        target_link_libraries(ffmpeg_debug_qp PRIVATE
            ${AVFORMAT_LIBRARIES}
            ${AVCODEC_LIBRARIES}
            ${AVUTIL_LIBRARIES}
        )
        target_link_directories(ffmpeg_debug_qp PRIVATE
            ${AVFORMAT_LIBRARY_DIRS}
            ${AVCODEC_LIBRARY_DIRS}
            ${AVUTIL_LIBRARY_DIRS}
        )
    endif()
endif()

# Installation
install(TARGETS ffmpeg_debug_qp RUNTIME DESTINATION bin)
