from __future__ import absolute_import, division, print_function

__metaclass__ = type

import unittest

from ansible_collections.cisco.mso.plugins.module_utils.mso import MSOModule, parse_version, version_compare, version_greater_than_or_equal


class TestMSOVersionUtils(unittest.TestCase):
    def test_parse_version_with_numeric_segments(self):
        self.assertEqual(parse_version("5.2.1.5"), [5, 2, 1, 5])
        self.assertEqual(parse_version("4.2"), [4, 2])

    def test_parse_version_with_non_numeric_segments(self):
        self.assertEqual(parse_version("5.2.1a"), [5, 2, 1])
        self.assertEqual(parse_version("5.2-build.1"), [5, 2, 1])
        self.assertEqual(parse_version("5.2.beta"), [5, 2])

    def test_parse_version_with_empty_or_invalid_values(self):
        self.assertEqual(parse_version(""), [])
        self.assertEqual(parse_version(None), [])
        self.assertEqual(parse_version("beta"), [])

    def test_version_compare_pads_with_zeros(self):
        self.assertEqual(version_compare("5.2", "5.2.0"), 0)
        self.assertEqual(version_compare("5.2.1", "5.2"), 1)
        self.assertEqual(version_compare("5.1.9", "5.2"), -1)

    def test_version_compare_with_non_numeric_suffix(self):
        self.assertEqual(version_compare("5.2.1a", "5.2.1"), 0)
        self.assertEqual(version_compare("5.2.1-build", "5.2.0"), 1)

    def test_version_greater_than_or_equal(self):
        self.assertTrue(version_greater_than_or_equal("5.2", "5.2"))
        self.assertTrue(version_greater_than_or_equal("5.2.1a", "5.2"))
        self.assertFalse(version_greater_than_or_equal("5.1.9", "5.2"))
        self.assertFalse(version_greater_than_or_equal("5.1", "5.2"))
        self.assertFalse(version_greater_than_or_equal("", "5.2"))


class TestMSOLegacyUserLookup(unittest.TestCase):
    """Covers the untouched legacy get_user_from_list_of_users() (ND < 4.2 / NDO < 5.2)."""

    def test_lookup_user_from_legacy_items_spec_shape(self):
        users = {"items": [{"spec": {"loginID": "admin", "loginDomain": None, "userID": "user-1"}}]}
        result = MSOModule.get_user_from_list_of_users(None, "admin", users)
        self.assertEqual(result, {"loginID": "admin", "loginDomain": None, "userID": "user-1"})

    def test_lookup_user_from_legacy_list_lower_case_keys(self):
        users = [{"loginid": "user2", "logindomain": "ldap", "userID": "user-2"}]
        result = MSOModule.get_user_from_list_of_users(None, "user2", users, "ldap")
        self.assertEqual(result, {"loginid": "user2", "logindomain": "ldap", "userID": "user-2"})

    def test_lookup_user_returns_none_when_not_found(self):
        users = {"items": [{"spec": {"loginID": "admin", "loginDomain": None, "userID": "user-1"}}]}
        result = MSOModule.get_user_from_list_of_users(None, "user2", users)
        self.assertIsNone(result)


class TestMSOV1UserLookup(unittest.TestCase):
    """Covers the new, fully separate v1 infra API lookups (ND 4.2+ / NDO 5.2+)."""

    def test_lookup_user_from_v1_localusers_shape(self):
        users = {"localusers": [{"loginID": "admin", "userID": "user-1"}]}
        result = MSOModule.get_user_from_list_of_nd_users_v1(None, "admin", users, "localusers")
        self.assertEqual(result, {"loginID": "admin", "userID": "user-1"})

    def test_lookup_user_from_v1_remoteusers_shape_with_domain(self):
        users = {"remoteUsers": [{"loginID": "user2", "loginDomain": "LDAP", "userID": "user-2"}]}
        result = MSOModule.get_user_from_list_of_nd_users_v1(None, "user2", users, "remoteUsers", "LDAP")
        self.assertEqual(result, {"loginID": "user2", "loginDomain": "LDAP", "userID": "user-2"})

    def test_lookup_user_returns_none_when_not_found(self):
        users = {"localusers": [{"loginID": "admin", "userID": "user-1"}]}
        result = MSOModule.get_user_from_list_of_nd_users_v1(None, "user2", users, "localusers")
        self.assertIsNone(result)

    def test_lookup_user_handles_missing_key_without_error(self):
        users = {"localusers": None}
        result = MSOModule.get_user_from_list_of_nd_users_v1(None, "admin", users, "localusers")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
