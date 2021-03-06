import re
import unittest
from conans.model.settings import Settings
from conans.model.conan_file import ConanFile
from conans.client.generators.scons import SConsGenerator
from conans.model.build_info import DepsCppInfo
from conans.model.ref import ConanFileReference


class SConsGeneratorTest(unittest.TestCase):
    def variables_setup_test(self):
        conanfile = ConanFile(None, None, Settings({}), None)
        ref = ConanFileReference.loads("MyPkg/0.1@lasote/stables")
        cpp_info = DepsCppInfo()
        cpp_info.defines = ["MYDEFINE1"]
        conanfile.deps_cpp_info.update(cpp_info, ref)
        ref = ConanFileReference.loads("MyPkg2/0.1@lasote/stables")
        cpp_info = DepsCppInfo()
        cpp_info.defines = ["MYDEFINE2"]
        conanfile.deps_cpp_info.update(cpp_info, ref)
        generator = SConsGenerator(conanfile)
        content = generator.content
        scons_lines = content.splitlines()
        self.assertIn("        \"CPPDEFINES\"  : [\'MYDEFINE2\', \'MYDEFINE1\'],", scons_lines)
        self.assertIn("        \"CPPDEFINES\"  : [\'MYDEFINE1\'],", scons_lines)
        self.assertIn("        \"CPPDEFINES\"  : [\'MYDEFINE2\'],", scons_lines)

