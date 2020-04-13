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

#include <srs_app_async_call.hpp>

using namespace std;

#include <srs_kernel_error.hpp>
#include <srs_kernel_log.hpp>

// the sleep interval for http async callback.
#define SRS_AUTO_ASYNC_CALLBACL_SLEEP_US 300000

ISrsAsyncCallTask::ISrsAsyncCallTask()
{
}

ISrsAsyncCallTask::~ISrsAsyncCallTask()
{
}

SrsAsyncCallWorker::SrsAsyncCallWorker()
{
    pthread = new SrsReusableThread("async", this, SRS_AUTO_ASYNC_CALLBACL_SLEEP_US);
}

SrsAsyncCallWorker::~SrsAsyncCallWorker()
{
    srs_freep(pthread);

    std::vector<ISrsAsyncCallTask*>::iterator it;
    for (it = tasks.begin(); it != tasks.end(); ++it) {
        ISrsAsyncCallTask* task = *it;
        srs_freep(task);
    }
    tasks.clear();
}

int SrsAsyncCallWorker::execute(ISrsAsyncCallTask* t)
{
    int ret = ERROR_SUCCESS;

    tasks.push_back(t);

    return ret;
}

int SrsAsyncCallWorker::start()
{
    return pthread->start();
}

void SrsAsyncCallWorker::stop()
{
    pthread->stop();
}

int SrsAsyncCallWorker::cycle()
{
    int ret = ERROR_SUCCESS;
    
    std::vector<ISrsAsyncCallTask*> copies = tasks;
    tasks.clear();

    std::vector<ISrsAsyncCallTask*>::iterator it;
    for (it = copies.begin(); it != copies.end(); ++it) {
        ISrsAsyncCallTask* task = *it;
        if ((ret = task->call()) != ERROR_SUCCESS) {
            srs_warn("ignore async callback %s, ret=%d", task->to_string().c_str(), ret);
        }
        srs_freep(task);
    }

    return ret;
}


