/*
 * Copyright (c) 2016-2017 Werner Robitza, Fredrik Pihl, Stefano Sabatini
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

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <libavutil/opt.h>
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/video_enc_params.h>
#include <libavutil/avutil.h>
#include <libavutil/motion_vector.h>
#include <libavutil/log.h>

static AVFormatContext *fmt_ctx = NULL;
static AVCodecContext *dec_ctx = NULL;
static const char *src_filename = NULL;
const char macroblock_switch[] = "-m";
static int video_stream_idx = -1;
static int frame_count = 0;
static int debug_level = 48;
static int current_pkt_size = 0;


typedef struct {
    int acc_qp;
    int count;
    int mb_qp;
    char mb_type;
} MBQP;


static void log_callback(void *ptr, int level, const char *fmt, va_list vl)
{
    if (level > AV_LOG_WARNING) {
        return;
    }

    char line[1024];
    vsnprintf(line, sizeof(line), fmt, vl);

    fprintf(stderr, "%s", line);
}

static void compute_macroblock_qp_grid(AVFrame *frame,
                                       int *mb_width, int *mb_height,
                                       MBQP **grid_out)
{
    AVFrameSideData *sd_qp = av_frame_get_side_data(frame, AV_FRAME_DATA_VIDEO_ENC_PARAMS);

    AVFrameSideData *sd_mv = av_frame_get_side_data(frame, AV_FRAME_DATA_MOTION_VECTORS);

    *mb_width = *mb_height = 0;
    *grid_out = NULL;

    if (!sd_qp) return;

    AVVideoEncParams *par = (AVVideoEncParams *)sd_qp->data;
    if (!par) return;

    int w = frame->width;
    int h = frame->height;

    *mb_width  = (w + 15) / 16;
    *mb_height = (h + 15) / 16;

    int total_mb = (*mb_width) * (*mb_height);
    MBQP *grid = calloc(total_mb, sizeof(MBQP));
    if (!grid) return;

    char default_type = (frame->pict_type == AV_PICTURE_TYPE_I) ? 'I' : 'S';
    for(int i=0; i<total_mb; i++) grid[i].mb_type = default_type;

    for (int i = 0; i < par->nb_blocks; i++) {
        AVVideoBlockParams *b = av_video_enc_params_block(par, i);
        if (!b) continue;
        int block_qp = par->qp + b->delta_qp;
        int bx0 = b->src_x;
        int by0 = b->src_y;
        int bx1 = bx0 + b->w;
        int by1 = by0 + b->h;

        if (bx0 < 0) bx0 = 0; if (by0 < 0) by0 = 0;
        if (bx1 > w) bx1 = w; if (by1 > h) by1 = h;
        if (bx0 >= bx1 || by0 >= by1) continue;

        int mb_x0 = bx0 / 16; int mb_y0 = by0 / 16;
        int mb_x1 = (bx1 - 1) / 16; int mb_y1 = (by1 - 1) / 16;

        for (int my = mb_y0; my <= mb_y1; my++) {
            if (my < 0 || my >= *mb_height) continue;
            for (int mx = mb_x0; mx <= mb_x1; mx++) {
                if (mx < 0 || mx >= *mb_width) continue;
                int idx = my * (*mb_width) + mx;
                grid[idx].acc_qp += block_qp;
                grid[idx].count++;
            }
        }
    }

    if (sd_mv) {
        const AVMotionVector *mvs = (const AVMotionVector *)sd_mv->data;
        int num_mvs = sd_mv->size / sizeof(AVMotionVector);

        for (int i = 0; i < num_mvs; i++) {
            const AVMotionVector *mv = &mvs[i];

            int mb_x = (mv->dst_x + mv->w / 2) / 16;
            int mb_y = (mv->dst_y + mv->h / 2) / 16;

            if (mb_x >= *mb_width || mb_y >= *mb_height) continue;

            int idx = mb_y * (*mb_width) + mb_x;

            if (mv->source < 0) {
                if (mv->motion_x == 0 && mv->motion_y == 0)
                     grid[idx].mb_type = 'S';
                else
                     grid[idx].mb_type = 'I';
            } else {
                grid[idx].mb_type = 'P';
            }
        }
    }

    for (int i = 0; i < total_mb; i++) {
        if (grid[i].count > 0)
            grid[i].mb_qp = (grid[i].acc_qp + (grid[i].count/2)) / grid[i].count;
        else
            grid[i].mb_qp = 0;
    }

    *grid_out = grid;
}


static char detect_frame_type_with_skip_using_grid(AVFrame *frame, MBQP *grid, int mb_w, int mb_h, int base_qp)
{
    char type = av_get_picture_type_char(frame->pict_type);

    if (type != 'P') return type;

    if (!grid || mb_w == 0 || mb_h == 0) {
        AVFrameSideData *sd =
            av_frame_get_side_data(frame, AV_FRAME_DATA_VIDEO_ENC_PARAMS);
        if (!sd) return type;
        AVVideoEncParams *par = (AVVideoEncParams *)sd->data;
        if (!par) return type;
        if (par->nb_blocks <= 0) return type;
        if (par->qp != 0) return type;
        for (int i = 0; i < par->nb_blocks; i++) {
            AVVideoBlockParams *b = av_video_enc_params_block(par, i);
            if (b->delta_qp != 0) return type;
        }
        return 'S';
    }
    if (base_qp != 0) return type;

    int total_mb = mb_w * mb_h;
    for (int i = 0; i < total_mb; i++) {
        if (grid[i].mb_qp != 0) return type;
    }
    return 'S';
}

static void print_frame_qp(AVFrame *frame) {
    AVFrameSideData *sd = av_frame_get_side_data(frame, AV_FRAME_DATA_VIDEO_ENC_PARAMS);

    int mb_w = 0, mb_h = 0;
    MBQP *grid = NULL;
    int base_qp = 0;
    int size = current_pkt_size;
    const AVCodec *codec = dec_ctx->codec;

    if (sd) {
        AVVideoEncParams *par = (AVVideoEncParams *)sd->data;
        base_qp = par->qp;
        compute_macroblock_qp_grid(frame, &mb_w, &mb_h, &grid);
    }

    char type = detect_frame_type_with_skip_using_grid(frame, grid, mb_w, mb_h, base_qp);

    av_log(dec_ctx, AV_LOG_WARNING, "[%s @ %p] ", codec->name, (void*) dec_ctx);

    av_log(dec_ctx, AV_LOG_WARNING, "New frame, type: %c\n", type);

    if (grid) {
        for (int y = 0; y < mb_h; y++) {
            av_log(dec_ctx, AV_LOG_WARNING, "[%s @ %p] ", codec->name, (void*) dec_ctx);
            for (int x = 0; x < mb_w; x++) {
                int qp_value = grid[y * mb_w + x].mb_qp;
                char type = grid[y * mb_w + x].mb_type;

                if(debug_level == 48)
                    av_log(dec_ctx, AV_LOG_WARNING, "%d", qp_value);
                else
                    av_log(dec_ctx, AV_LOG_WARNING, "%d%c  ", qp_value, type);
            }
            av_log(dec_ctx, AV_LOG_WARNING, "\n");
        }
    }

    av_log(dec_ctx, AV_LOG_WARNING, "[%s @ %p] ", codec->name, (void*) dec_ctx);
    av_log(dec_ctx, AV_LOG_WARNING, "<< frame_type: %c; pkt_size: %d >>\n", type, size);

    if (grid) free(grid);
}

static int decode_packet(AVPacket *pkt) {
    current_pkt_size = pkt ? pkt->size : 0;

    int ret = avcodec_send_packet(dec_ctx, pkt);
    if (ret < 0) return ret;

    dec_ctx->debug = 56;

    AVFrame *frame = av_frame_alloc();
    while (ret >= 0) {
        ret = avcodec_receive_frame(dec_ctx, frame);
        if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF) break;
        if (ret < 0) {
            av_frame_free(&frame);
            return ret;
        }

        print_frame_qp(frame);
        frame_count++;
        av_frame_unref(frame);
    }
    av_frame_free(&frame);
    return 0;
}

void print_usage_and_exit(char *tool_name) {
    fprintf(stderr, "usage: %s "
        "input_file [-m]\n",
        tool_name);
    exit(1);
}

int main(int argc, char **argv) {

    if (argc < 2 || argc > 3) {
        print_usage_and_exit(argv[0]);
    }

    src_filename = argv[1];

    if (argc == 3) {
        const char *macroblock_arg = argv[2];
        const char *ptr_switch = &macroblock_switch[0];

        if (strcmp(macroblock_arg, ptr_switch) == 0) {
            debug_level = 56;
        }
        else {
            print_usage_and_exit(argv[0]);
        }
    }

    av_log_set_callback(log_callback);
    av_log_set_level(debug_level);

    if (avformat_open_input(&fmt_ctx, argv[1], NULL, NULL) < 0) return 1;
    if (avformat_find_stream_info(fmt_ctx, NULL) < 0) return 1;

    int ret = av_find_best_stream(fmt_ctx, AVMEDIA_TYPE_VIDEO, -1, -1, NULL, 0);
    if (ret < 0) return 1;
    video_stream_idx = ret;
    AVStream *st = fmt_ctx->streams[video_stream_idx];

    const AVCodec *codec = avcodec_find_decoder(st->codecpar->codec_id);
    dec_ctx = avcodec_alloc_context3(codec);
    if (!dec_ctx) return 1;
    if (avcodec_parameters_to_context(dec_ctx, st->codecpar) < 0) return 1;

    dec_ctx->export_side_data |= AV_CODEC_EXPORT_DATA_VIDEO_ENC_PARAMS;
    dec_ctx->thread_count = 1;

    if (avcodec_open2(dec_ctx, codec, NULL) < 0) return 1;

    AVPacket *pkt = av_packet_alloc();
    while (av_read_frame(fmt_ctx, pkt) >= 0) {
        if (pkt->stream_index == video_stream_idx)
            decode_packet(pkt);
        av_packet_unref(pkt);
    }
    decode_packet(NULL);

    av_packet_free(&pkt);
    avcodec_free_context(&dec_ctx);
    avformat_close_input(&fmt_ctx);
    return 0;
}
