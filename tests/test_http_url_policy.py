import unittest


class TestHttpUrlPolicy(unittest.TestCase):
    def test_http_blocked_by_default(self):
        from mcp import SecureMcpLibrary  # type: ignore

        lib = SecureMcpLibrary(db_path=":memory:", allow_http=False)
        with self.assertRaises(ValueError):
            lib._validate_url("http://example.com")

    def test_http_allowed_with_flag(self):
        from mcp import SecureMcpLibrary  # type: ignore

        lib = SecureMcpLibrary(db_path=":memory:", allow_http=True)
        self.assertEqual(lib._validate_url("http://example.com"), "http://example.com")

    def test_no_scheme_defaults_to_https(self):
        from mcp import SecureMcpLibrary  # type: ignore

        lib = SecureMcpLibrary(db_path=":memory:", allow_http=False)
        self.assertEqual(lib._validate_url("example.com"), "https://example.com")


if __name__ == "__main__":
    unittest.main()

