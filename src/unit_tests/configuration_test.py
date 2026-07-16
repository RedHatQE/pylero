# -*- coding: utf-8 -*-
"""Offline tests for pylero.base_polarion.Configuration.

Unlike the other test modules, these tests do not require a live
Polarion instance; they only exercise config file/env var parsing.
Run with: nose2 -s src/unit_tests configuration_test
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import tempfile
import unittest
from unittest import mock

from pylero.base_polarion import Configuration
from pylero.exceptions import PyleroLibException

CONFIG_TEMPLATE = """[webservice]
url={url}
svn_repo=https://polarion.example.com/repo
user={user}
password={password}
token=
{default_project_line}
"""

POLARION_ENV_VARS = [
    "POLARION_URL",
    "POLARION_REPO",
    "POLARION_USERNAME",
    "POLARION_PASSWORD",
    "POLARION_TOKEN",
    "POLARION_PROJECT",
    "POLARION_TIMEOUT",
    "POLARION_CERT_PATH",
    "POLARION_DISABLE_MANUAL_AUTH",
]


class ConfigurationTest(unittest.TestCase):
    def _make_config(
        self,
        default_project_line,
        url="https://polarion.example.com/polarion",
        user="test_user",
        password="test_password",
    ):
        """Writes a config file and patches Configuration to only read it,
        ignoring the packaged/user/curdir config files and POLARION_* env
        vars of the environment running the tests.
        """
        cfg_file = tempfile.NamedTemporaryFile(mode="w", suffix=".pylero", delete=False)
        self.addCleanup(os.unlink, cfg_file.name)
        cfg_file.write(
            CONFIG_TEMPLATE.format(
                default_project_line=default_project_line,
                url=url,
                user=user,
                password=password,
            )
        )
        cfg_file.close()
        for attr in ("GLOBAL_CONFIG", "LOCAL_CONFIG", "CURDIR_CONFIG"):
            patcher = mock.patch.object(Configuration, attr, cfg_file.name)
            patcher.start()
            self.addCleanup(patcher.stop)
        env = {var: "" for var in POLARION_ENV_VARS}
        env_patcher = mock.patch.dict(os.environ, env)
        env_patcher.start()
        self.addCleanup(env_patcher.stop)

    def test_default_project_set(self):
        self._make_config("default_project=PROJ1")
        self.assertEqual(Configuration().proj, "PROJ1")

    def test_default_project_empty(self):
        self._make_config("default_project=")
        with self.assertRaises(PyleroLibException) as cm:
            Configuration()
        self.assertIn("default_project", str(cm.exception))
        self.assertIn("POLARION_PROJECT", str(cm.exception))

    def test_default_project_missing(self):
        self._make_config("")
        with self.assertRaises(PyleroLibException) as cm:
            Configuration()
        self.assertIn("default_project", str(cm.exception))

    def test_default_project_from_env(self):
        self._make_config("default_project=")
        with mock.patch.dict(os.environ, {"POLARION_PROJECT": "PROJ2"}):
            self.assertEqual(Configuration().proj, "PROJ2")

    def test_missing_url_and_credentials(self):
        self._make_config("default_project=PROJ1", url="", user="", password="")
        with self.assertRaises(PyleroLibException) as cm:
            Configuration()
        self.assertIn("url", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
