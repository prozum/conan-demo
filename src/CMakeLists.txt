set(HEADERS gen.hpp src.hpp)

set(MESSAGE "Generated string")
configure_file("gen.cpp.in" "gen.cpp" @ONLY)
add_library(src gen.cpp)

add_library(gen src.cpp)

add_executable(main main.cpp)
target_link_libraries(main src gen)

set(DEST_DIR "${CMAKE_INSTALL_PREFIX}")
CONFIGURE_FILE("gen.pc.in" "gen.pc" @ONLY)
CONFIGURE_FILE("src.pc.in" "src.pc" @ONLY)

install(TARGETS src gen
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib)
install(FILES ${HEADERS} DESTINATION include)
install(FILES "${CMAKE_CURRENT_BINARY_DIR}/src.pc" "${CMAKE_CURRENT_BINARY_DIR}/gen.pc" DESTINATION lib/pkgconfig)
