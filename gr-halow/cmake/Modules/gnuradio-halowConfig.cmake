find_package(PkgConfig)

PKG_CHECK_MODULES(PC_GR_HALOW gnuradio-halow)

FIND_PATH(
    GR_HALOW_INCLUDE_DIRS
    NAMES gnuradio/halow/api.h
    HINTS $ENV{HALOW_DIR}/include
        ${PC_HALOW_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    GR_HALOW_LIBRARIES
    NAMES gnuradio-halow
    HINTS $ENV{HALOW_DIR}/lib
        ${PC_HALOW_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
          )

include("${CMAKE_CURRENT_LIST_DIR}/gnuradio-halowTarget.cmake")

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(GR_HALOW DEFAULT_MSG GR_HALOW_LIBRARIES GR_HALOW_INCLUDE_DIRS)
MARK_AS_ADVANCED(GR_HALOW_LIBRARIES GR_HALOW_INCLUDE_DIRS)
