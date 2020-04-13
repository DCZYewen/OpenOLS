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

#include <srs_app_conn.hpp>

using namespace std;

#include <srs_kernel_log.hpp>
#include <srs_kernel_error.hpp>
#include <srs_app_utility.hpp>

IConnectionManager::IConnectionManager()
{
}

IConnectionManager::~IConnectionManager()
{
}

SrsConnection::SrsConnection(IConnectionManager* cm, st_netfd_t c)
{
    id = 0;
    manager = cm;
    stfd = c;
    disposed = false;
    expired = false;
    
    // the client thread should reap itself, 
    // so we never use joinable.
    // TODO: FIXME: maybe other thread need to stop it.
    // @see: https://github.com/ossrs/srs/issues/78
    pthread = new SrsOneCycleThread("conn", this);
}

SrsConnection::~SrsConnection()
{
    dispose();
    
    srs_freep(pthread);
}

void SrsConnection::dispose()
{
    if (disposed) {
        return;
    }
    
    disposed = true;
    
    /**
     * when delete the connection, stop the connection,
     * close the underlayer socket, delete the thread.
     */
    srs_close_stfd(stfd);
}

int SrsConnection::start()
{
    return pthread->start();
}

int SrsConnection::cycle()
{
    int ret = ERROR_SUCCESS;
    
    _srs_context->generate_id();
    id = _srs_context->get_id();
    
    ip = srs_get_peer_ip(st_netfd_fileno(stfd));
    
    ret = do_cycle();
    
    // if socket io error, set to closed.
    if (srs_is_client_gracefully_close(ret)) {
        ret = ERROR_SOCKET_CLOSED;
    }
    
    // success.
    if (ret == ERROR_SUCCESS) {
        srs_trace("client finished.");
    }
    
    // client close peer.
    if (ret == ERROR_SOCKET_CLOSED) {
        srs_warn("client disconnect peer. ret=%d", ret);
    }

    return ERROR_SUCCESS;
}

void SrsConnection::on_thread_stop()
{
    // TODO: FIXME: never remove itself, use isolate thread to do cleanup.
    manager->remove(this);
}

int SrsConnection::srs_id()
{
    return id;
}

string SrsConnection::remote_ip() {
    return ip;
}

void SrsConnection::expire()
{
    expired = true;
}


