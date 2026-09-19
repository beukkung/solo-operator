"""Check realistic packaging failures and standalone installation contents."""

from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import validate_links, validate_skill


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.skill = self.root / "solo-operator"
        shutil.copytree(ROOT / "skills/solo-operator", self.skill)

    def test_standalone_install_contains_valid_skill_and_license(self):
        self.assertEqual(validate_skill(self.skill), [])
        self.assertEqual(validate_links(self.skill), [])
        self.assertEqual((self.skill / "LICENSE").read_bytes(), (ROOT / "LICENSE").read_bytes())

    def test_malformed_pasted_frontmatter_is_rejected(self):
        path = self.skill / "SKILL.md"
        path.write_text(path.read_text(encoding="utf-8").replace("\n---\n", "\n------\n", 1), encoding="utf-8")
        self.assertTrue(any("frontmatter" in message for message in validate_skill(self.skill)))

    def test_missing_interface_file_is_rejected(self):
        (self.skill / "agents/openai.yaml").unlink()
        self.assertTrue(any("missing" in message for message in validate_skill(self.skill)))

    def test_missing_license_is_rejected(self):
        (self.skill / "LICENSE").unlink()
        self.assertTrue(any("LICENSE" in message for message in validate_skill(self.skill)))

    def test_wrong_invocation_is_rejected(self):
        path = self.skill / "agents/openai.yaml"
        path.write_text(path.read_text(encoding="utf-8").replace("$solo-operator", "$wrong-skill"), encoding="utf-8")
        self.assertTrue(any("default_prompt" in message for message in validate_skill(self.skill)))

    def test_disabled_automatic_selection_is_rejected(self):
        path = self.skill / "agents/openai.yaml"
        path.write_text(path.read_text(encoding="utf-8").replace("true", "false"), encoding="utf-8")
        self.assertTrue(any("automatic" in message for message in validate_skill(self.skill)))

    def test_links_detect_missing_and_escaping_files(self):
        (self.root / "README.md").write_text("[missing](missing.md)\n[escape](../outside.md)\n", encoding="utf-8")
        self.assertEqual(len(validate_links(self.root)), 2)

    def test_links_accept_existing_files_and_external_urls(self):
        (self.root / "README.md").write_text("[skill](solo-operator/SKILL.md)\n[web](https://example.com)\n", encoding="utf-8")
        self.assertEqual(validate_links(self.root), [])


if __name__ == "__main__":
    unittest.main()
