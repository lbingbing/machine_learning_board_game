cmake_minimum_required(VERSION 3.21)

project(machine_learning_board_game)

set(CMAKE_VERBOSE_MAKEFILE OFF)

set(release_dir .)

install(DIRECTORY python/board_game DESTINATION ${release_dir})
