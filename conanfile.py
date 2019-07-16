#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from conans import ConanFile, tools, CMake

def get_version():
    git = tools.Git()
    try:
        if git.get_tag() and not git.get_branch():
            return git.get_tag()
        else:
            return "master"
    except:
        return None

class DemoConan(ConanFile):
    name = "demo"
    version = get_version()
    url = "http://gitlab.com/aivero/public/conan/conan-demo"
    license = "MIT"
    description = ("Demo conan package")
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = ["CMakeLists.txt", "src/*"]

    def build(self):
        vars = {
            "CFLAGS": "-fdebug-prefix-map=%s=." % self.source_folder,
            "CXXFLAGS": "-fdebug-prefix-map=%s=." % self.source_folder,
        }
        with tools.environment_append(vars):
            cmake = CMake(self)
            cmake.configure()
            cmake.build()
            cmake.install()

    def package(self):
        if self.settings.build_type == "Debug":
            self.copy("*.c*", "src")
            self.copy("*.h*", "src")

    def package_info(self):
        self.cpp_info.srcdirs.append("src")
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.env_info.PKG_CONFIG_PATH.append(os.path.join(self.package_folder, "lib", "pkgconfig"))
        for pc_file in os.listdir(os.path.join(self.package_folder, "lib", "pkgconfig")):
            setattr(self.env_info, "PKG_CONFIG_%s_PREFIX" % pc_file[:-3].replace(".", "_").replace("-", "_").upper(), self.package_folder)
