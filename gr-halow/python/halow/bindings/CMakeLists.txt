# Copyright 2020 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

########################################################################
# Check if there is C++ code at all
########################################################################
if(NOT halow_sources)
    MESSAGE(STATUS "No C++ sources... skipping python bindings")
    return()
endif(NOT halow_sources)

########################################################################
# Check for pygccxml
########################################################################
GR_PYTHON_CHECK_MODULE_RAW(
    "pygccxml"
    "import pygccxml"
    PYGCCXML_FOUND
    )

include(GrPybind)

########################################################################
# Python Bindings
########################################################################

list(APPEND halow_python_files
    halow_sync_short_python.cc
    halow_sync_long_python.cc
    halow_frame_equalizer_python.cc python_bindings.cc)

GR_PYBIND_MAKE_OOT(halow
   ../../..
   gr::halow
   "${halow_python_files}")

# copy bindings extension for use in QA test module
add_custom_command(TARGET halow_python POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:halow_python>
    ${PROJECT_BINARY_DIR}/test_modules/gnuradio/halow/
)

install(TARGETS halow_python DESTINATION ${GR_PYTHON_DIR}/gnuradio/halow COMPONENT pythonapi)
