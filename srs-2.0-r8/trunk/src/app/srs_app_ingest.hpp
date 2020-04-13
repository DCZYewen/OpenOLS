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

#ifndef SRS_APP_INGEST_HPP
#define SRS_APP_INGEST_HPP

/*
#include <srs_app_ingest.hpp>
*/
#include <srs_core.hpp>

#ifdef SRS_AUTO_INGEST

#include <vector>

#include <srs_app_thread.hpp>
#include <srs_app_reload.hpp>

class SrsFFMPEG;
class SrsConfDirective;
class SrsPithyPrint;

/**
* ingester ffmpeg object.
*/
class SrsIngesterFFMPEG
{
private:
    std::string vhost;
    std::string id;
    SrsFFMPEG* ffmpeg;
    int64_t starttime;
public:
    SrsIngesterFFMPEG();
    virtual ~SrsIngesterFFMPEG();
public:
    virtual int initialize(SrsFFMPEG* ff, std::string v, std::string i);
    // the ingest uri, [vhost]/[ingest id]
    virtual std::string uri();
    // the alive in ms.
    virtual int alive();
    virtual bool equals(std::string v, std::string i);
    virtual bool equals(std::string v);
public:
    virtual int start();
    virtual void stop();
    virtual int cycle();
    // @see SrsFFMPEG.fast_stop().
    virtual void fast_stop();
};

/**
* ingest file/stream/device, 
* encode with FFMPEG(optional),
* push to SRS(or any RTMP server) over RTMP.
*/
class SrsIngester : public ISrsReusableThreadHandler, public ISrsReloadHandler
{
private:
    std::vector<SrsIngesterFFMPEG*> ingesters;
private:
    SrsReusableThread* pthread;
    SrsPithyPrint* pprint;
public:
    SrsIngester();
    virtual ~SrsIngester();
public:
    virtual void dispose();
public:
    virtual int start();
    virtual void stop();
// interface ISrsReusableThreadHandler.
public:
    virtual int cycle();
    virtual void on_thread_stop();
private:
    virtual void clear_engines();
    virtual int parse();
    virtual int parse_ingesters(SrsConfDirective* vhost);
    virtual int parse_engines(SrsConfDirective* vhost, SrsConfDirective* ingest);
    virtual int initialize_ffmpeg(SrsFFMPEG* ffmpeg, SrsConfDirective* vhost, SrsConfDirective* ingest, SrsConfDirective* engine);
    virtual void show_ingest_log_message();
// interface ISrsReloadHandler.
public:
    virtual int on_reload_vhost_removed(std::string vhost);
    virtual int on_reload_vhost_added(std::string vhost);
    virtual int on_reload_ingest_removed(std::string vhost, std::string ingest_id);
    virtual int on_reload_ingest_added(std::string vhost, std::string ingest_id);
    virtual int on_reload_ingest_updated(std::string vhost, std::string ingest_id);
};

#endif
#endif

