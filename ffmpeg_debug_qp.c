/*
 * Copyright (c) 2016 Werner Robitza, Fredrik Pihl, Stefano Sabatini
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
 * THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

/**
 * @file
 * FFmpeg QP debugging script
 */

#include <libavutil/imgutils.h>
#include <libavutil/samplefmt.h>
#include <libavutil/timestamp.h>
#include <libavformat/avformat.h>

static AVFormatContext *fmt_ctx = NULL;
static AVCodecContext *video_dec_ctx = NULL;
static int width, height;
static enum AVPixelFormat pix_fmt;
static AVStream *video_stream = NULL;
static const char *src_filename = NULL;

static uint8_t *video_dst_data[4] = {NULL};
static int      video_dst_linesize[4];
static int video_dst_bufsize;

static int video_stream_idx = -1;
static AVFrame *frame = NULL;
static AVPacket pkt;
static int video_frame_count = 0;

/* The different ways of decoding and managing data memory. You are not
 * supposed to support all the modes in your application but pick the one most
 * appropriate to your needs. Look for the use of api_mode in this example to
 * see what are the differences of API usage between them */
enum {
    API_MODE_OLD                  = 0, /* old method, deprecated */
    API_MODE_NEW_API_REF_COUNT    = 1, /* new method, using the frame reference counting */
    API_MODE_NEW_API_NO_REF_COUNT = 2, /* new method, without reference counting */
};

static int api_mode = API_MODE_OLD;

static int decode_packet(int *got_frame, int cached)
{
    int ret = 0;
    int decoded = pkt.size;
    int x, y;
    int mb_width = (video_dec_ctx->width + 15) / 16;
    int mb_height = (video_dec_ctx->height + 15) / 16;
    int mb_stride = mb_width + 1;

    *got_frame = 0;

    if (pkt.stream_index == video_stream_idx) {
        /* decode video frame */
        ret = avcodec_decode_video2(video_dec_ctx, frame, got_frame, &pkt);
        if (ret < 0) {
            fprintf(stderr, "Error decoding video frame (%s)\n", av_err2str(ret));
            return ret;
        }
        if (video_dec_ctx->width != width || video_dec_ctx->height != height ||
            video_dec_ctx->pix_fmt != pix_fmt) {
            /* To handle this change, one could call av_image_alloc again and
             * decode the following frames into another rawvideo file. */
            fprintf(stderr, "Error: Width, height and pixel format have to be "
                    "constant in a rawvideo file, but the width, height or "
                    "pixel format of the input video changed:\n"
                    "old: width = %d, height = %d, format = %s\n"
                    "new: width = %d, height = %d, format = %s\n",
                    width, height, av_get_pix_fmt_name(pix_fmt),
                    video_dec_ctx->width, video_dec_ctx->height,
                    av_get_pix_fmt_name(video_dec_ctx->pix_fmt));
            return -1;
        }

        if (*got_frame) {

            fprintf(stderr,"Frame_type: %c ; pkt_size: %d\n",
                    av_get_picture_type_char(frame->pict_type),
                    av_frame_get_pkt_size(frame));

#if 0
// This code does not work, see mailing list for more info
            AVBufferRef* qp_table_buf = av_buffer_ref(frame->qp_table_buf);
//            qscale_table = qscale_table_buf->data + 2 * s->mb_stride + 1;
            int8_t* qscale_table = qp_table_buf->data;

            for (y = 0; y < mb_height; y++) {
                for (x = 0; x < mb_width; x++) {
//                        printf("%2d", qscale_table[x + y * mb_stride]);
                        printf("%2d", qscale_table[x + y * mb_stride]);
                }
            }

#endif
        }
    }

    /* If we use the new API with reference counting, we own the data and need
     * to de-reference it when we don't use it anymore */
    if (*got_frame && api_mode == API_MODE_NEW_API_REF_COUNT)
        av_frame_unref(frame);

    return decoded;
}

static int open_codec_context(int *stream_idx,
                              AVFormatContext *fmt_ctx, enum AVMediaType type)
{
    int ret, stream_index;
    AVStream *st;
    AVCodecContext *dec_ctx = NULL;
    AVCodec *dec = NULL;
    AVDictionary *opts = NULL;

    ret = av_find_best_stream(fmt_ctx, type, -1, -1, NULL, 0);
    if (ret < 0) {
        fprintf(stderr, "Could not find %s stream in input file '%s'\n",
                av_get_media_type_string(type), src_filename);
        return ret;
    } else {
        stream_index = ret;
        st = fmt_ctx->streams[stream_index];

        /* find decoder for the stream */
        dec_ctx = st->codec;
        dec = avcodec_find_decoder(dec_ctx->codec_id);
        if (!dec) {
            fprintf(stderr, "Failed to find %s codec\n",
                    av_get_media_type_string(type));
            return AVERROR(EINVAL);
        }

        /* Init the decoders, with or without reference counting */
        if (api_mode == API_MODE_NEW_API_REF_COUNT)
            av_dict_set(&opts, "refcounted_frames", "1", 0);
        if ((ret = avcodec_open2(dec_ctx, dec, &opts)) < 0) {
            fprintf(stderr, "Failed to open %s codec\n",
                    av_get_media_type_string(type));
            return ret;
        }
        *stream_idx = stream_index;
    }

    return 0;
}

int main (int argc, char **argv)
{
    int ret = 0, got_frame;

    if (argc != 2 ) {
        fprintf(stderr, "usage: %s "
                "input_file\n"
                "\n", argv[0]);
        exit(1);
    }
    src_filename = argv[1];

    /* register all formats and codecs */
    av_register_all();

    /* open input file, and allocate format context */
    if (avformat_open_input(&fmt_ctx, src_filename, NULL, NULL) < 0) {
        fprintf(stderr, "Could not open source file %s\n", src_filename);
        exit(1);
    }

    /* retrieve stream information */
    if (avformat_find_stream_info(fmt_ctx, NULL) < 0) {
        fprintf(stderr, "Could not find stream information\n");
        exit(1);
    }

    if (open_codec_context(&video_stream_idx, fmt_ctx, AVMEDIA_TYPE_VIDEO) >= 0) {
        video_stream = fmt_ctx->streams[video_stream_idx];
        video_dec_ctx = video_stream->codec;

        /* enable QP-debug, FF_DEBUG_QP
         * libavcodec/avcodec.h +2569 */
        printf("Default log level: %d\n", av_log_get_level());
        av_log_set_level(48);
        printf("New log level: %d\n", av_log_get_level());
        video_dec_ctx->debug = 48;
        /* Single threaded or else the output will be distorted */
        video_dec_ctx->thread_count = 1;

        /* allocate image where the decoded image will be put */
        width = video_dec_ctx->width;
        height = video_dec_ctx->height;
        pix_fmt = video_dec_ctx->pix_fmt;
        ret = av_image_alloc(video_dst_data, video_dst_linesize,
                             width, height, pix_fmt, 1);
        if (ret < 0) {
            fprintf(stderr, "Could not allocate raw video buffer\n");
            goto end;
        }
        video_dst_bufsize = ret;
    }

    /* dump input information to stderr */
    //av_dump_format(fmt_ctx, 0, src_filename, 0);

    if (!video_stream) {
        fprintf(stderr, "Could not find video stream in the input, aborting\n");
        ret = 1;
        goto end;
    }

    /* When using the new API, you need to use the libavutil/frame.h API, while
     * the classic frame management is available in libavcodec */
    if (api_mode == API_MODE_OLD)
        frame = av_frame_alloc();
    else
        frame = av_frame_alloc();
    if (!frame) {
        fprintf(stderr, "Could not allocate frame\n");
        ret = AVERROR(ENOMEM);
        goto end;
    }

    /* initialize packet, set data to NULL, let the demuxer fill it */
    av_init_packet(&pkt);
    pkt.data = NULL;
    pkt.size = 0;

    if (video_stream)
        printf("Demuxing video from file '%s'\n", src_filename);

    /* read frames from the file */
    while (av_read_frame(fmt_ctx, &pkt) >= 0) {
        AVPacket orig_pkt = pkt;
        do {
            ret = decode_packet(&got_frame, 0);
            if (ret < 0)
                break;
            pkt.data += ret;
            pkt.size -= ret;
        } while (pkt.size > 0);
        av_free_packet(&orig_pkt);
    }

    /* flush cached frames */
    pkt.data = NULL;
    pkt.size = 0;
    do {
        decode_packet(&got_frame, 1);
    } while (got_frame);

end:
    avcodec_close(video_dec_ctx);
    avformat_close_input(&fmt_ctx);
    if (api_mode == API_MODE_OLD)
        av_frame_free(&frame);
    else
        av_frame_free(&frame);
    av_free(video_dst_data[0]);

    return ret < 0;
}
