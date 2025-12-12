#!/usr/bin/env bash
#
# Build a minimal static FFmpeg for ffmpeg-debug-qp
#
# This builds only the components needed:
# - Demuxers: common video containers
# - Decoders: MPEG-2, MPEG-4, H.264 (for QP extraction)
# - No encoders, filters, or output formats
#

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."
FFMPEG_DIR="${PROJECT_ROOT}/external/ffmpeg"
FFMPEG_VERSION="${FFMPEG_VERSION:-8.0.1}"

usage() {
    echo "Usage: $0 [options]"
    echo "  --download          download FFmpeg source (version ${FFMPEG_VERSION})"
    echo "  --reconfigure       reconfigure FFmpeg"
    echo "  --clean             clean FFmpeg build (implies reconfigure)"
    echo "  --help              print this message"
    echo ""
    echo "Environment variables:"
    echo "  FFMPEG_VERSION      FFmpeg version to download (default: ${FFMPEG_VERSION})"
    echo "  MAKE_JOBS           Number of parallel jobs (default: auto)"
    exit 1
}

download=false
reconfigure=false
clean=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --download)
            download=true
            ;;
        --reconfigure)
            reconfigure=true
            ;;
        --clean)
            clean=true
            reconfigure=true
            ;;
        --help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
    shift
done

# Download FFmpeg source if requested or not present
if [[ "$download" = true ]] || [[ ! -d "${FFMPEG_DIR}" ]]; then
    echo "Downloading FFmpeg ${FFMPEG_VERSION}..."
    mkdir -p "${PROJECT_ROOT}/external"
    cd "${PROJECT_ROOT}/external"

    TARBALL="ffmpeg-${FFMPEG_VERSION}.tar.xz"
    URL="https://ffmpeg.org/releases/${TARBALL}"

    if [[ ! -f "${TARBALL}" ]]; then
        curl -LO "${URL}"
    fi

    rm -rf ffmpeg
    tar xf "${TARBALL}"
    mv "ffmpeg-${FFMPEG_VERSION}" ffmpeg
    echo "FFmpeg ${FFMPEG_VERSION} downloaded and extracted."
fi

cd "${FFMPEG_DIR}" || { echo "FFmpeg directory not found!"; exit 1; }

startTime=$(date +%s)

if [[ "$clean" = true ]]; then
    echo "Cleaning FFmpeg build..."
    if [[ -f ffbuild/config.mak ]]; then
        make clean || true
    fi
    rm -f config.h
fi

if [[ ! -f config.h ]] || [[ "$reconfigure" = true ]]; then
    echo "Configuring FFmpeg..."

    configureFlags=(
        # Build static libraries only
        --enable-static
        --disable-shared

        # No programs or docs
        --disable-programs
        --disable-doc

        # Threading
        --enable-pthreads

        # Disable all filters and scaling (not needed for QP extraction)
        --disable-avfilter
        --disable-swscale
        --disable-swresample
        --disable-avdevice

        # Disable hardware acceleration (not needed, reduces dependencies)
        --disable-audiotoolbox
        --disable-videotoolbox
        --disable-vaapi
        --disable-vdpau
        --disable-vulkan
        --disable-cuda
        --disable-cuvid
        --disable-nvenc
        --disable-nvdec

        # Disable optional dependencies
        --disable-securetransport
        --disable-iconv
        --disable-libdrm
        --disable-sdl2
        --disable-xlib
        --disable-zlib
        --disable-bzlib
        --disable-lzma

        # No output needed
        --disable-encoders
        --disable-muxers
        --disable-outdevs
        --disable-bsfs

        # Minimal input
        --disable-indevs
        --disable-protocols
        --enable-protocol=file

        # Only essential demuxers for video files
        --disable-demuxers
        --enable-demuxer=h264
        --enable-demuxer=hevc
        --enable-demuxer=avi
        --enable-demuxer=matroska
        --enable-demuxer=mov
        --enable-demuxer=mpegvideo
        --enable-demuxer=mpegps
        --enable-demuxer=mpegts
        --enable-demuxer=m4v
        --enable-demuxer=rawvideo

        # Only essential parsers
        --disable-parsers
        --enable-parser=h264
        --enable-parser=hevc
        --enable-parser=mpeg4video
        --enable-parser=mpegvideo

        # Only decoders that support QP extraction
        # (MPEG-2, MPEG-4 Part 2, H.264)
        --disable-decoders
        --enable-decoder=h264
        --enable-decoder=mpeg2video
        --enable-decoder=mpeg4
        --enable-decoder=msmpeg4v1
        --enable-decoder=msmpeg4v2
        --enable-decoder=msmpeg4v3
    )

    ./configure "${configureFlags[@]}"
fi

echo "Building FFmpeg..."

# Use MAKE_JOBS env var if set, otherwise detect
if [[ -z "${MAKE_JOBS:-}" ]]; then
    if command -v nproc &>/dev/null; then
        JOBS=$(nproc)
    elif command -v sysctl &>/dev/null; then
        JOBS=$(sysctl -n hw.ncpu)
    else
        JOBS=4
    fi
else
    JOBS="${MAKE_JOBS}"
fi

make "-j${JOBS}"

endTime=$(date +%s)

echo ""
echo "FFmpeg build complete in $((endTime - startTime)) seconds."
echo ""
echo "Static libraries built:"
ls -la libavformat/libavformat.a libavcodec/libavcodec.a libavutil/libavutil.a 2>/dev/null || true
echo ""
echo "Now build ffmpeg_debug_qp with:"
echo "  cd ${PROJECT_ROOT}"
echo "  cmake -B build -DUSE_VENDORED_FFMPEG=ON"
echo "  cmake --build build"
