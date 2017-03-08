# use pkg-config for getting CFLAGS and LDLIBS
FFMPEG_LIBS=    libavdevice                        \
                libavformat                        \
                libavfilter                        \
                libavcodec                         \
                libswresample                      \
                libswscale                         \
                libavutil                          \

CFLAGS += -Wall -g
CFLAGS := $(shell pkg-config --cflags $(FFMPEG_LIBS)) $(CFLAGS)
LDLIBS := $(shell pkg-config --libs $(FFMPEG_LIBS)) $(LDLIBS)

TOOL=ffmpeg_debug_qp

OBJS=$(addsuffix .o,$(TOOL))

.PHONY: clean

all: $(OBJS) $(TOOL)
clean:
	rm -f $(TOOL) $(OBJS)
