import parse
import logging


log = logging.getLogger("payment.{}".format(__name__))


# PT-BR
@parse.with_pattern(r'[^"]*')
def parse_unquoted(text):
    """Parse/match string(s) that do not contain double-quote characters."""
    return text

