/*
The MIT License (MIT)

Copyright (c) 2013-2015 SRS(ossrs)

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#include <srs_app_reload.hpp>

using namespace std;

#include <srs_kernel_error.hpp>

ISrsReloadHandler::ISrsReloadHandler()
{
}

ISrsReloadHandler::~ISrsReloadHandler()
{
}

int ISrsReloadHandler::on_reload_listen()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_utc_time()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_max_conns()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_pid()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_log_tank()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_log_level()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_log_file()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_pithy_print()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_http_api_enabled()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_http_api_disabled()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_http_stream_enabled()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_http_stream_disabled()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_http_stream_updated()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_http_updated()
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_http_remux_updated(string vhost)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_added(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_removed(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_atc(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_gop_cache(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_queue_length(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_time_jitter(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_mix_correct(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_forward(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_hls(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_hds(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_dvr(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_mr(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_mw(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_smi(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_tcp_nodelay(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_realtime(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_p1stpt(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_pnt(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_chunk_size(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_vhost_transcode(string /*vhost*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_ingest_removed(string /*vhost*/, string /*ingest_id*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_ingest_added(string /*vhost*/, string /*ingest_id*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_ingest_updated(string /*vhost*/, string /*ingest_id*/)
{
    return ERROR_SUCCESS;
}

int ISrsReloadHandler::on_reload_user_info()
{
    return ERROR_SUCCESS;
}

