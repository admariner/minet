# =============================================================================
# Minet Instagram Location CLI Action
# =============================================================================
#
# Logic of the `instagram location` action.
#
from itertools import islice

from minet.cli.utils import with_enricher_and_loading_bar
from minet.cli.instagram.utils import with_instagram_fatal_errors
from minet.instagram import InstagramAPIScraper
from minet.instagram.types import InstagramLocationPost
from minet.instagram.exceptions import (
    InstagramInvalidTargetError,
    InstagramNoPublicationError,
)


@with_instagram_fatal_errors
@with_enricher_and_loading_bar(
    headers=InstagramLocationPost,
    title="Scraping posts",
    unit="location",
    nested=True,
    sub_unit="posts",
)
def action(cli_args, enricher, loading_bar):
    client = InstagramAPIScraper(cookie=cli_args.cookie)

    for i, row, location in enricher.enumerate_cells(
        cli_args.column, with_rows=True, start=1
    ):
        with loading_bar.step(location):
            try:
                generator = client.search_location(location)

                if cli_args.limit:
                    generator = islice(generator, cli_args.limit)

                for post in generator:
                    enricher.writerow(row, post)
                    loading_bar.nested_advance()

            except InstagramInvalidTargetError:
                loading_bar.print(
                    "Given user (line %i) is probably not an Instagram location: %s"
                    % (i, location)
                )

            except InstagramNoPublicationError:
                loading_bar.print(
                    "Given location (line %i) has probably no publication: %s"
                    % (i, location)
                )
