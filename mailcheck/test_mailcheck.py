import unittest
import mailcheck

DOMAINS = (
    "google.com",
    "gmail.com",
    "emaildomain.com",
    "comcast.net",
    "facebook.com",
    "msn.com",
    "gmx.de",
)

SECOND_LEVEL_DOMAINS = (
    "yahoo",
    "hotmail",
    "mail",
    "live",
    "outlook",
    "gmx",
)

TOP_LEVEL_DOMAINS = (
    "co.uk",
    "com",
    "org",
    "info",
    "fr",
)


class Sift3DistanceTestCase(unittest.TestCase):
    def test_sift3_distance(self):
        self.assertEqual(mailcheck.sift3_distance("boat", "boot"), 1)
        self.assertEqual(mailcheck.sift3_distance("boat", "bat"), 1.5)
        self.assertEqual(mailcheck.sift3_distance("ifno", "info"), 2)
        self.assertEqual(mailcheck.sift3_distance("hotmial", "hotmail"), 2)


class SplitEmailTestCase(unittest.TestCase):
    def test_one_level_domain(self):
        parts = mailcheck.split_email("postbox@com")
        expected = {
            "address": "postbox",
            "domain": "com",
            "top_level_domain": "com",
            "second_level_domain": "",
        }
        self.assertEqual(parts, expected)

    def test_two_level_domain(self):
        parts = mailcheck.split_email("test@example.com")
        expected = {
            "address": "test",
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_three_level_domain(self):
        parts = mailcheck.split_email("test@example.co.uk")
        expected = {
            "address": "test",
            "domain": "example.co.uk",
            "top_level_domain": "co.uk",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_four_level_domain(self):
        parts = mailcheck.split_email("test@mail.randomsmallcompany.co.uk")
        expected = {
            "address": "test",
            "domain": "mail.randomsmallcompany.co.uk",
            "top_level_domain": "randomsmallcompany.co.uk",
            "second_level_domain": "mail",
        }
        self.assertEqual(parts, expected)

    def test_rfc_compliant(self):
        parts = mailcheck.split_email('"foo@bar"@example.com')
        expected = {
            "address": '"foo@bar"',
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_numbers(self):
        parts = mailcheck.split_email("containsnumbers1234567890@example.com")
        expected = {
            "address": "containsnumbers1234567890",
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_plus(self):
        parts = mailcheck.split_email("contains+symbol@example.com")
        expected = {
            "address": "contains+symbol",
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_hyphen(self):
        parts = mailcheck.split_email("contains-symbol@example.com")
        expected = {
            "address": "contains-symbol",
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_periods(self):
        parts = mailcheck.split_email("contains.symbol@domain.contains.symbol")
        expected = {
            "address": "contains.symbol",
            "domain": "domain.contains.symbol",
            "top_level_domain": "contains.symbol",
            "second_level_domain": "domain",
        }
        self.assertEqual(parts, expected)

    def test_contains_period_backslash(self):
        parts = mailcheck.split_email('"contains.and\ symbols"@example.com')
        expected = {
            "address": '"contains.and\ symbols"',
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_period_at_sign(self):
        parts = mailcheck.split_email('"contains.and.@.symbols.com"@example.com')
        expected = {
            "address": '"contains.and.@.symbols.com"',
            "domain": "example.com",
            "top_level_domain": "com",
            "second_level_domain": "example",
        }
        self.assertEqual(parts, expected)

    def test_contains_all_symbols(self):
        parts = mailcheck.split_email('"()<>[]:;@,\\\"!#$%&\'*+-/=?^_`{}|\ \ \ \ \ ~\ \ \ \ \ \ \ ?\ \ \ \ \ \ \ \ \ \ \ \ ^_`{}|~.a"@allthesymbols.com')
        expected = {
            "address": '"()<>[]:;@,\\\"!#$%&\'*+-/=?^_`{}|\ \ \ \ \ ~\ \ \ \ \ \ \ ?\ \ \ \ \ \ \ \ \ \ \ \ ^_`{}|~.a"',
            "domain": "allthesymbols.com",
            "top_level_domain": "com",
            "second_level_domain": "allthesymbols",
        }
        self.assertEqual(parts, expected)

    def test_not_rfc_compliant(self):
        self.assertFalse(mailcheck.split_email("example.com"))
        self.assertFalse(mailcheck.split_email("abc.example.com"))
        self.assertFalse(mailcheck.split_email("@example.com"))
        self.assertFalse(mailcheck.split_email("test@"))

    def test_trim_spaces(self):
        parts = mailcheck.split_email(" postbox@com")
        expected = {
            "address": "postbox",
            "domain": "com",
            "top_level_domain": "com",
            "second_level_domain": "",
        }
        self.assertEqual(parts, expected)
        parts = mailcheck.split_email("postbox@com ")
        self.assertEqual(parts, expected)

    def test_most_similar_domain(self):
        self.assertEqual(
            mailcheck.find_closest_domain("google.com", DOMAINS),
            "google.com"
        )
        self.assertEqual(
            mailcheck.find_closest_domain("gmail.com", DOMAINS),
            "gmail.com"
        )
        self.assertEqual(
            mailcheck.find_closest_domain("emaildomain.com", DOMAINS),
            "emaildomain.com"
        )
        self.assertEqual(
            mailcheck.find_closest_domain("gmsn.com", DOMAINS),
            "msn.com"
        )
        self.assertEqual(
            mailcheck.find_closest_domain("gmaik.com", DOMAINS),
            "gmail.com"
        )

    def test_most_similar_second_level_domain(self):
        self.assertEqual(
            mailcheck.find_closest_domain("hotmial", SECOND_LEVEL_DOMAINS),
            "hotmail"
        )
        self.assertEqual(
            mailcheck.find_closest_domain("tahoo", SECOND_LEVEL_DOMAINS),
            "yahoo"
        )
        self.assertEqual(
            mailcheck.find_closest_domain("livr", SECOND_LEVEL_DOMAINS),
            "live"
        )
        self.assertEqual(
            mailcheck.find_closest_domain("outllok", SECOND_LEVEL_DOMAINS),
            "outlook"
        )

    def test_most_similar_top_level_domain(self):
        self.assertEqual(
            mailcheck.find_closest_domain("cmo", TOP_LEVEL_DOMAINS),
            "com"
        )
        self.assertEqual(
            mailcheck.find_closest_domain("ogr", TOP_LEVEL_DOMAINS),
            "org"
        )
        self.assertEqual(
            mailcheck.find_closest_domain("ifno", TOP_LEVEL_DOMAINS),
            "info"
        )
        self.assertEqual(
            mailcheck.find_closest_domain("com.uk", TOP_LEVEL_DOMAINS),
            "co.uk"
        )


class SuggestTestCast(unittest.TestCase):
    def test_returns_array(self):
        expected = {
            "address": "test",
            "domain": "gmail.com",
            "full": "test@gmail.com",
        }
        self.assertEqual(
            mailcheck.suggest("test@gmail.co", DOMAINS),
            expected
        )

    def test_no_suggestion_returns_false(self):
        self.assertFalse(
            mailcheck.suggest("contact@kicksend.com", DOMAINS),
        )

    def test_incomplete_email_returns_false(self):
        self.assertFalse(
            mailcheck.suggest("", DOMAINS),
        )
        self.assertFalse(
            mailcheck.suggest("test@", DOMAINS),
        )
        self.assertFalse(
            mailcheck.suggest("test", DOMAINS),
        )

    def test_returns_valid_suggestions(self):
        self.assertEqual(
            mailcheck.suggest("test@gmailc.om", DOMAINS)["domain"],
            "gmail.com"
        )
        self.assertEqual(
            mailcheck.suggest("test@emaildomain.co", DOMAINS)["domain"],
            "emaildomain.com"
        )
        self.assertEqual(
            mailcheck.suggest("test@gmail.con", DOMAINS)["domain"],
            "gmail.com"
        )
        self.assertEqual(
            mailcheck.suggest("test@gnail.con", DOMAINS)["domain"],
            "gmail.com"
        )
        self.assertEqual(
            mailcheck.suggest("test@GNAIL.con", DOMAINS)["domain"],
            "gmail.com"
        )
        self.assertEqual(
            mailcheck.suggest("test@#gmail.com", DOMAINS)["domain"],
            "gmail.com"
        )
        self.assertEqual(
            mailcheck.suggest("test@comcast.nry", DOMAINS)["domain"],
            "comcast.net"
        )
        self.assertEqual(
            mailcheck.suggest(
                "test@homail.con",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )["domain"],
            "hotmail.com"
        )
        self.assertEqual(
            mailcheck.suggest(
                "test@hotmail.co",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )["domain"],
            "hotmail.com"
        )
        self.assertEqual(
            mailcheck.suggest(
                "test@yajoo.com",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )["domain"],
            "yahoo.com"
        )
        self.assertEqual(
            mailcheck.suggest(
                "test@randomsmallcompany.cmo",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )["domain"],
            "randomsmallcompany.com"
        )

    def test_idempotent_suggestions(self):
        self.assertEqual(
            mailcheck.suggest(
                "test@yahooo.cmo",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )["domain"],
            "yahoo.com"
        )

    def test_no_suggestions_valid_2ld_tld(self):
        self.assertFalse(
            mailcheck.suggest(
                "test@yahoo.co.uk",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )
        )

    def test_no_suggestions_valid_2ld_tld_close_domain(self):
        self.assertFalse(
            mailcheck.suggest(
                "test@gmx.fr",
                DOMAINS,
                SECOND_LEVEL_DOMAINS,
                TOP_LEVEL_DOMAINS
            )
        )