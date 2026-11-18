from types import SimpleNamespace
from unittest import TestCase, mock

from pylero.base_polarion import BasePolarion
from pylero.custom_field_type import CustomFieldType
from pylero.project import Project


class ProjectCustomFieldsTest(TestCase):
    def setUp(self):
        self.service = mock.Mock(spec_set=["getDefinedCustomFieldKeys", "getDefinedCustomFieldTypes"])
        session = SimpleNamespace(tracker_client=SimpleNamespace(service=self.service))
        patcher = mock.patch.object(BasePolarion, "_session", session)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.project = Project(suds_object=SimpleNamespace(id="demo", _uri="project-uri"))

    def test_get_defined_custom_field_keys(self):
        self.service.getDefinedCustomFieldKeys.return_value = ["priority", "owner"]
        self.assertEqual(self.project.get_defined_custom_field_keys("task"), ["priority", "owner"])
        self.service.getDefinedCustomFieldKeys.assert_called_once_with("demo", "task")

    def test_get_defined_custom_field_types(self):
        self.service.getDefinedCustomFieldTypes.return_value = [
            SimpleNamespace(id="priority"),
            SimpleNamespace(id="owner"),
        ]
        fields = self.project.get_defined_custom_field_types("task")
        self.assertTrue(all(isinstance(field, CustomFieldType) for field in fields))
        self.assertEqual([field.cft_id for field in fields], ["priority", "owner"])
        self.service.getDefinedCustomFieldTypes.assert_called_once_with("demo", "task")
