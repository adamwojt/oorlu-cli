# pylint: disable=superfluous-parens,super-with-arguments,raise-missing-from
"""
This is copied from Django source code as the same validation is used in oor.lu API
https://docs.djangoproject.com/en/1.11/_modules/django/core/validators
"""

import re
from urllib.parse import urlsplit, urlunsplit


class ValidationError(Exception):
    pass


def check_and_update_url_schema(url):
    """Credit : https://stackoverflow.com/questions/49983328
    I realize this is quite cheap.
    """
    if "://" not in url:
        url = "http://" + url
    return url


def validate_long_url(value):
    """
    Append schema if needed and validate.
    """
    long_url = check_and_update_url_schema(value)
    if len(long_url) >= 500:
        raise ValidationError("Length of URL should be below 500 chars")
    URLValidator()(long_url)
    return long_url


class RegexValidator:
    regex = ""
    message = "Enter a valid value."
    code = "invalid"
    inverse_match = False
    flags = 0

    def __init__(self, regex=None, message=None, code=None, inverse_match=None, flags=None):
        if regex is not None:
            self.regex = regex
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if inverse_match is not None:
            self.inverse_match = inverse_match
        if flags is not None:
            self.flags = flags

        self.regex = re.compile(self.regex, self.flags)

    def __call__(self, value):
        """
        Validate that the input contains a match for the regular expression
        if inverse_match is False, otherwise raise ValidationError.
        """
        if not (self.inverse_match is not bool(self.regex.search(value))):
            raise ValidationError(self.message)

    def __eq__(self, other):
        return (
            isinstance(other, RegexValidator)
            and self.regex.pattern == other.regex.pattern
            and self.regex.flags == other.regex.flags
            and (self.message == other.message)
            and (self.code == other.code)
            and (self.inverse_match == other.inverse_match)
        )

    def __ne__(self, other):
        return not (self == other)


class URLValidator(RegexValidator):
    ul = "\u00a1-\uffff"  # unicode letters range (must be a unicode string, not a raw string)

    # IP patterns
    ipv4_re = r"(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)(?:\.(?:25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}"
    ipv6_re = r"\[[0-9a-f:\.]+\]"  # (simple regex, validated later)

    # Host patterns
    hostname_re = r"[a-z" + ul + r"0-9](?:[a-z" + ul + r"0-9-]{0,61}[a-z" + ul + r"0-9])?"
    # Max length for domain name labels is 63 characters per RFC 1034 sec. 3.1
    domain_re = r"(?:\.(?!-)[a-z" + ul + r"0-9-]{1,63}(?<!-))*"
    tld_re = (
        r"\."  # dot
        r"(?!-)"  # can't start with a dash
        r"(?:[a-z" + ul + "-]{2,63}"  # domain label
        r"|xn--[a-z0-9]{1,59})"  # or punycode label
        r"(?<!-)"  # can't end with a dash
        r"\.?"  # may have a trailing dot
    )
    host_re = "(" + hostname_re + domain_re + tld_re + "|localhost)"

    regex = re.compile(
        r"^(?:[a-z0-9\.\-\+]*)://"  # scheme is validated separately
        r"(?:\S+(?::\S*)?@)?"  # user:pass authentication
        r"(?:" + ipv4_re + "|" + ipv6_re + "|" + host_re + ")"
        r"(?::\d{2,5})?"  # port
        r"(?:[/?#][^\s]*)?"  # resource path
        r"\Z",
        re.IGNORECASE,
    )
    message = "Enter a valid URL."
    schemes = ["http", "https", "ftp", "ftps"]

    def __init__(self, schemes=None, **kwargs):
        super(URLValidator, self).__init__(**kwargs)
        if schemes is not None:
            self.schemes = schemes

    def __call__(self, value):
        # Check first if the scheme is valid
        scheme = value.split("://")[0].lower()
        if scheme not in self.schemes:
            raise ValidationError(self.message)

        # Then check full URL
        try:
            super(URLValidator, self).__call__(value)
        except ValidationError as e:
            # Trivial case failed. Try for possible IDN domain
            if value:
                try:
                    scheme, netloc, path, query, fragment = urlsplit(value)
                except ValueError:  # for example, "Invalid IPv6 URL"
                    raise ValidationError(self.message)
                try:
                    netloc = netloc.encode("idna").decode("ascii")  # IDN -> ACE
                except UnicodeError:  # invalid domain part
                    raise e
                url = urlunsplit((scheme, netloc, path, query, fragment))
                super(URLValidator, self).__call__(url)
            else:
                raise
        # The maximum length of a full host name is 253 characters per RFC 1034
        # section 3.1. It's defined to be 255 bytes or less, but this includes
        # one byte for the length of the name and one byte for the trailing dot
        # that's used to indicate absolute names in DNS.
        if len(urlsplit(value).netloc) > 253:
            raise ValidationError(self.message)
