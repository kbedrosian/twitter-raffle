# twitter-raffle

Script to randomly select users with eligible tweets in a given timeframe e.g. as in a raffle.

Uses the following Twitter API endpoint, which searches tweets within the last 7 days: https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-recent

The script requires an OAuth 2.0 Bearer Token to be provided, in order to call the API.  This is described here: https://developer.twitter.com/en/docs/authentication/oauth-2-0
