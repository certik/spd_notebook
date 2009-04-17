
"""
"""
import os, sys, cPickle
import zlib; comp = zlib
import bz2; comp_other = bz2

# changeto import zlib to use zlib instead; but this
# slows down loading any data stored in the other format
base=None

def process(s):
    if not base is None and (len(s) == 0 or s[0] != '/'):
        s = base + '/' + s
    if s[-5:] != '.sobj':
        return s + '.sobj'
    else:
        return s

def load(filename, compress=True, verbose=True):
    """   
    Load Sage object from the file with name filename, which will
    have an .sobj extension added if it doesn't have one.

    .. note::

       There is also a special Sage command (that is not
       available in Python) called load that you use by typing

       ::
       
          sage: load filename.sage           # not tested
                
       The documentation below is not for that command.  The
       documentation for load is almost identical to that for attach.
       Type attach? for help on attach.

    This also loads a ".sobj" file over a network by specifying the full URL.
    (Setting "verbose = False" suppresses the loading progress indicator.)    

    EXAMPLE::
    
        sage: u = 'http://sage.math.washington.edu/home/was/db/test.sobj'  
        sage: s = load(u)                                                  # optional - internet
        Attempting to load remote file: http://sage.math.washington.edu/home/was/db/test.sobj
        Loading: [.]        
        sage: s                                                            # optional - internet
        'hello SAGE'
    """

    ## Check if filename starts with "http://" or "https://"
    lower = filename.lower()
    if lower.startswith("http://") or lower.startswith("https://"):
        from sage.misc.remote_file import get_remote_file
        filename = get_remote_file(filename, verbose=verbose)
        tmpfile_flag = True
    elif lower.endswith('.f') or lower.endswith('.f90'):
        globals()['fortran'](filename)
        return 
    else:
        tmpfile_flag = False	
        filename = process(filename)

    ## Load file by absolute filename
    X = loads(open(filename).read(), compress=compress)
    try:
        X._default_filename = os.path.abspath(filename)
    except AttributeError:
        pass

    ## Delete the tempfile, if it exists
    if tmpfile_flag == True:
        os.unlink(filename)		

    return X


def save(obj, filename=None, compress=True, **kwds):
    """   
    Save obj to the file with name filename, which will 
    have an .sobj extension added if it doesn't have one.
    This will *replace* the contents of filename.

    EXAMPLES::
    
        sage: a = matrix(2, [1,2,3,-5/2])
        sage: save(a, 'test.sobj')
        sage: load('test')
        [   1    2]
        [   3 -5/2]
        sage: E = EllipticCurve([-1,0])
        sage: P = plot(E)
        sage: save(P, 'test')
        sage: save(P, filename="sage.png", xmin=-2)
        sage: print load('test.sobj')
        Graphics object consisting of 2 graphics primitives
        sage: save("A python string", './test')
        sage: load('./test.sobj')
        'A python string'
        sage: load('./test')
        'A python string'
    """
    # Add '.sobj' if the filename currently has no extension
    if os.path.splitext(filename)[1] == '':
        filename += '.sobj'

    if filename.endswith('.sobj'):
        try:
            obj.save(filename=filename, compress=compress, **kwds)
        except (AttributeError, RuntimeError, TypeError):
            s = cPickle.dumps(obj, protocol=2)
            if compress:
                s = comp.compress(s)
            open(process(filename), 'wb').write(s)
    else:
        # Saving an object to an image file. 
        obj.save(filename, **kwds)

def dumps(obj, compress=True):
    """
    Dump obj to a string s.  To recover obj, use ``loads(s)``.

    .. seealso:: :func:`dumps`
    
    EXAMPLES::
    
        sage: a = 2/3
        sage: s = dumps(a)
        sage: print len(s)
        49
        sage: loads(s)
        2/3    
    """
    if make_pickle_jar:
        picklejar(obj)
    try:
        return obj.dumps(compress)
    except (AttributeError, RuntimeError, TypeError):
        if compress:
            return comp.compress(cPickle.dumps(obj, protocol=2))
        else:
            return cPickle.dumps(obj, protocol=2)

def loads(s, compress=True):
    """
    Recover an object x that has been dumped to a string s
    using ``s = dumps(x)``.

    .. seealso:: :func:`dumps`

    EXAMPLES::
    
        sage: a = matrix(2, [1,2,3,-4/3])
        sage: s = dumps(a)
        sage: loads(s)
        [   1    2]
        [   3 -4/3]

    One can load uncompressed data even if one messes up
    and doesn't specify compress=False.  This is slightly
    slower though.

    ::
    
        sage: v = [1..10]
        sage: loads(dumps(v, compress=False)) == v
        True
        sage: loads(dumps(v, compress=False), compress=True) == v
        True
        sage: loads(dumps(v, compress=True), compress=False) == v
        True
    """
    if not isinstance(s, str):
        raise TypeError, "s must be a string"
    if compress:
        try:
            return cPickle.loads(comp.decompress(s))
        except Exception, msg1:
            try:
                return cPickle.loads(comp_other.decompress(s))
            except Exception, msg2:
                # Maybe data is uncompressed?
                try:
                    return cPickle.loads(s)
                except Exception, msg3:
                    try: msg1 = str(msg1)
                    except: msg1 = type(msg1)
                    try: msg2 = str(msg2)
                    except: msg2 = type(msg2)
                    try: msg3 = str(msg3)
                    except: msg3 = type(msg3)
                    raise RuntimeError, "%s\n%s\n%s\nUnable to load pickled data."%(msg1,msg2,msg3)
    else:
        try:
            return cPickle.loads(s)
        except:
            # maybe data is compressed anyways??
            return loads(s, compress=True)


make_pickle_jar = os.environ.has_key('SAGE_PICKLE_JAR')

def picklejar(obj, dir=None):
    """
    Create pickled sobj of obj in dir, with name the absolute value of
    the hash of the pickle of obj.  This is used in conjection with
    sage.structure.sage_object.unpickle_all.

    To use this to test the whole Sage library right now, set the
    environment variable SAGE_PICKLE_JAR, which will make it so dumps
    will by default call picklejar with the default dir.  Once you do
    that and doctest Sage, you'll find that the SAGE_ROOT/tmp/
    contains a bunch of pickled objects along with corresponding txt
    descriptions of them.  Use the
    sage.structure.sage_object.unpickle_all to see if they unpickle
    later.

    INPUTS:

    - ``obj`` - a pickleable object

    - ``dir`` - a string or None; if None defaults to
      ``SAGE_ROOT/tmp/pickle_jar-version``

    EXAMPLES::
    
        sage: dir = tmp_dir()
        sage: sage.structure.sage_object.picklejar(1,dir)
        sage: len(os.listdir(dir))
        2
    """
    if dir is None:
        from sage.version import version
        dir = os.environ['SAGE_ROOT'] + '/tmp/pickle_jar-%s/'%version
    if not os.path.exists(dir):
        os.makedirs(dir)

    s = comp.compress(cPickle.dumps(obj,protocol=2))

    typ = str(type(obj))
    name = ''.join([x if (x.isalnum() or x == '_') else '_' for x in typ])
    base = '%s/%s'%(dir, name)
    if os.path.exists(base):
        i = 0
        while os.path.exists(base + '-%s'%i):
            i += 1
        base += '-%s'%i

    open(base + '.sobj', 'wb').write(s)
    txt = "type(obj) = %s\n"%typ
    import sage.version
    txt += "version = %s\n"%sage.version.version
    txt += "obj =\n'%s'\n"%str(obj)

    open(base + '.txt', 'w').write(txt)
    
def unpickle_all(dir, debug=False):
    """
    Unpickle all sobj's in the given directory, reporting failures as
    they occur.  Also printed the number of successes and failure.
    
    INPUT:

    - ``dir`` - string; a directory or name of a .tar.bz2 file that
      decompresses to give a directo pickirectory.

    EXAMPLES::
    
        sage: dir = tmp_dir()
        sage: sage.structure.sage_object.picklejar('hello', dir)
        sage: sage.structure.sage_object.unpickle_all(dir)
        Successfully unpickled 1 objects.
        Failed to unpickle 0 objects.

    We unpickle the standard pickle jar. This doctest tests that
    all "standard pickles" unpickle.  Every so often the standard pickle jar
    should be updated by running the doctest suite with the environment variable
    SAGE_PICKLE_JAR set, then copying the files from SAGE_ROOT/tmp/pickle_jar*
    into the standard pickle jar.

    ::
    
        sage: std = os.environ['SAGE_DATA'] + '/extcode/pickle_jar/pickle_jar.tar.bz2'
        sage: sage.structure.sage_object.unpickle_all(std)
        doctest:...: DeprecationWarning: RQDF is deprecated; use RealField(212) instead.
        Successfully unpickled 487 objects.
        Failed to unpickle 0 objects.
    """
    i = 0
    j = 0
    failed = []
    tracebacks = []
    if dir.endswith('.tar.bz2'):
        # create a temporary directory
        from sage.misc.all import tmp_dir
        T = tmp_dir()
        # extract tarball to it
        os.system('cd "%s"; bunzip2 -c "%s" | tar fx - '%(T, os.path.abspath(dir)))
        # Now use the directory in the tarball instead of dir
        dir = T + "/" + os.listdir(T)[0]
        
    for A in sorted(os.listdir(dir)):
        if A.endswith('.sobj'):
            try:
                load(dir + '/' + A)
                i += 1
            except Exception, msg:
                j += 1
                print "** failed: ", A
                failed.append(A)
                if debug:
                    tracebacks.append(sys.exc_info())

    if len(failed) > 0:
        print "Failed:\n%s"%('\n'.join(failed))
    print "Successfully unpickled %s objects."%i
    print "Failed to unpickle %s objects."%j
    if debug:
        return tracebacks
