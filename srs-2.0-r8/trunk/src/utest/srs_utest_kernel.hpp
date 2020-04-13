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

#ifndef SRS_UTEST_KERNEL_HPP
#define SRS_UTEST_KERNEL_HPP

/*
#include <srs_utest_kernel.hpp>
*/
#include <srs_utest.hpp>

#include <string>
#include <srs_kernel_file.hpp>
#include <srs_protocol_buffer.hpp>

class MockBufferReader: public ISrsBufferReader
{
private:
    std::string str;
public:
    MockBufferReader(const char* data);
    virtual ~MockBufferReader();
public:
    virtual int read(void* buf, size_t size, ssize_t* nread);
};

class MockSrsFileWriter : public SrsFileWriter
{
public:
    char* data;
    int offset;
public:
    MockSrsFileWriter();
    virtual ~MockSrsFileWriter();
public:
    virtual int open(std::string file);
    virtual void close();
public:
    virtual bool is_open();
    virtual int64_t tellg();
public:
    virtual int write(void* buf, size_t count, ssize_t* pnwrite);
// for mock
public:
    void mock_reset_offset();
};

class MockSrsFileReader : public SrsFileReader
{
public:
    char* data;
    int size;
    int offset;
public:
    MockSrsFileReader();
    virtual ~MockSrsFileReader();
public:
    virtual int open(std::string file);
    virtual void close();
public:
    virtual bool is_open();
    virtual int64_t tellg();
    virtual void skip(int64_t size);
    virtual int64_t lseek(int64_t offset);
    virtual int64_t filesize();
public:
    virtual int read(void* buf, size_t count, ssize_t* pnread);
// for mock
public:
    // append data to current offset, modify the offset and size.
    void mock_append_data(const char* _data, int _size);
    void mock_reset_offset();
};

#endif

