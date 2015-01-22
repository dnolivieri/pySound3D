import numpy,os,wave
import matplotlib.pyplot as p

def read_wavfile(filename,gain=None):
    assert os.path.exists(filename),"file %s doesn't exist" % filename
    wav = wave.open(filename,'rb')
    nframes = wav.getnframes()
    assert nframes > 0,"%s doesn't have any audio data!" % filename
    nchan = wav.getnchannels()
    sample_rate = wav.getframerate()
    sample_width = wav.getsampwidth()

#    print nframes
#    print nchan
#    print sample_rate
#    print sample_width

    # see http://ccrma.stanford.edu/courses/422/projects/WaveFormat/
    g = 1.0 if gain is None else gain
    if sample_width == 1:
        # data is unsigned bytes, 0 to 255
        dtype = numpy.uint8
        scale = g / 127.0
        offset = -1.0
    elif sample_width == 2:
        # data is signed 2's complement 16-bit samples (little-endian byte order)
        dtype = numpy.int16
        scale = g / 32767.0
        offset = 0.0
    elif sample_width == 4:
        # data is signed 2's complement 32-bit samples (little-endian byte order)
        dtype = numpy.int32
        scale = g / 2147483647.0
        offset = 0.0
    else:
        assert False,"unrecognized sample width %d" % sample_width

    outputs = [numpy.zeros(nframes,dtype=numpy.float64)
               for i in xrange(nchan)]

    count = 0
    while count < nframes:
        audio = numpy.frombuffer(wav.readframes(nframes-count),dtype=dtype)
        end = count + (len(audio) / nchan)
        for i in xrange(nchan):
            outputs[i][count:end] = audio[i::nchan]
        count = end
        
    # scale data appropriately
    for i in xrange(nchan):
        numpy.multiply(outputs[i],scale,outputs[i])
        if offset != 0: numpy.add(outputs[i],offset,outputs[i])

    # apply auto gain
    if gain is None:
        maxmag = max([max(numpy.absolute(outputs[i])) for i in xrange(nchan)])
        for i in xrange(nchan):
            numpy.multiply(outputs[i],1.0/maxmag,outputs[i])


    return [outputs[i] for i in xrange(nchan)]

def read_sound(filename):
    return read_wavfile(filename)[0]

