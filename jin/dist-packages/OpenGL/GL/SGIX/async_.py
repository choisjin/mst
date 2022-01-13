'''OpenGL extension SGIX.async

This module customises the behaviour of the
OpenGL.raw.GL.SGIX.async to provide a more
Python-friendly API

Overview (from the spec)

	This extension provides a framework for asynchronous OpenGL
	commands.  It also provides commands allowing a program to wait
	for the completion of asynchronous commands.

	Asynchronous commands have two properties:

	1) Asynchronous commands are non-blocking.  For example, an
	asynchronous ReadPixels command returns control to the program
	immediately rather than blocking until the command completes.
	This property allows the program to issue other OpenGL commands in
	parallel with the execution of commands that normally block.

	2) Asynchronous commands may complete out-of-order with respect to
	other OpenGL commands.  For example, an asynchronous TexImage
	command may complete after subsequent OpenGL commands issued by
	the program rather than maintaining the normal serial order of the
	OpenGL command stream.  This property allows the graphics
	accelerator to execute asynchronous commands in parallel with the
	normal command stream, for instance using a secondary path to
	transfer data from or to the host, without doing any dependency
	checking.

	Programs that issue asynchronous commands must also be able to
	determine when the commands have completed.  The completion status
	may be needed so that results can be retrieved (e.g. the image
	data from a ReadPixels command) or so that dependent commands can
	be issued (e.g. drawing commands that use texture data downloaded
	by an earlier asynchronous command).  This extension provides
	fine-grain control over asynchronous commands by introducing a
	mechanism for determining the status of individual commands.

	Each invocation of an asynchronous command is associated with an
	integer called a "marker."  A program specifies a marker before it
	issues an asynchronous command.  The program may later issue a
	command to query if any asynchronous commands have completed.  The
	query commands return a marker to identify the command that
	completed.  This extension provides both blocking and non-blocking
	query commands.

	This extension does not define any asynchronous commands.
	See SGIX_async_pixel for the asynchronous pixel commands.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/SGIX/async.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.SGIX.async_ import *
from OpenGL.raw.GL.SGIX.async_ import _EXTENSION_NAME

def glInitAsyncSGIX():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )

glFinishAsyncSGIX=wrapper.wrapper(glFinishAsyncSGIX).setOutput(
    'markerp',size=(1,),orPassIn=True
)
glPollAsyncSGIX=wrapper.wrapper(glPollAsyncSGIX).setOutput(
    'markerp',size=(1,),orPassIn=True
)
### END AUTOGENERATED SECTION
