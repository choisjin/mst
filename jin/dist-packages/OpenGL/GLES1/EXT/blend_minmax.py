'''OpenGL extension EXT.blend_minmax

This module customises the behaviour of the 
OpenGL.raw.GLES1.EXT.blend_minmax to provide a more 
Python-friendly API

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/blend_minmax.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES1 import _types, _glgets
from OpenGL.raw.GLES1.EXT.blend_minmax import *
from OpenGL.raw.GLES1.EXT.blend_minmax import _EXTENSION_NAME

def glInitBlendMinmaxEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION