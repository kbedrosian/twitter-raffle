#!/usr/bin/env python2.7

import argparse
import json
import random
import requests
import sys

def get_next_recent_tweets(tweet_query, start_time, end_time, bearer_token, next_token=None, verbose=False):
    params={'query': tweet_query,
            'expansions': 'author_id',
            'start_time': start_time,
            'end_time': end_time,
            'max_results': 100}
    if next_token is not None:
        params['next_token'] = next_token

    if verbose:
        print >>sys.stderr, 'Requesting with params:', params

    response = requests.get(
        'https://api.twitter.com/2/tweets/search/recent',
        params=params,
        headers={'Authorization': 'Bearer {}'.format(bearer_token)})
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_time', required=True,
                        help='Earliest timestamp for eligible tweets, in ISO 8601 format e.g. "2021-05-21T18:50:00-07:00"')
    parser.add_argument('--end_time', required=True,
                        help='Latest timestamp for eligible tweets, in ISO 8601 format e.g. "2021-05-21T21:00:00-07:00"')
    parser.add_argument('--all', action='store_true',
                        help='If true, don\'t make any selections, just return all eligible tweets')
    parser.add_argument('--num_selections', type=int, required=True,
                        help='Number of random selections to make from the eligible tweets')
    parser.add_argument('--bearer_token', required=True,
                        help='Bearer token for Twitter API. See documentation here for details: https://developer.twitter.com/en/docs/authentication/oauth-2-0/bearer-tokens')
    parser.add_argument('--tweet_query', required=True,
                        help='Query to pass to Twitter API e.g. "#myraffle -is:retweet". See documentation here for details: https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query\nExample: "#foo #bar -is:retweet"')
    parser.add_argument('--verbose', action='store_true')
    args = parser.parse_args()

    tweets_by_author_id = {}
    next_token = None
    while True:
        response = get_next_recent_tweets(
            tweet_query=args.tweet_query,
            start_time=args.start_time,
            end_time=args.end_time,
            bearer_token=args.bearer_token,
            next_token=next_token,
            verbose=args.verbose)
        assert response.ok, response
        response_json = response.json()
        data = response_json['data']
        for user in response_json['includes']['users']:
            author_id = user['id']
            tweets_by_author_id[user['username']] = [d['text'] for d in data if d['author_id'] == author_id]

        next_token = response_json['meta'].get('next_token')
        if args.verbose:
            print >>sys.stderr, 'Received {} results'.format(response_json['meta'].get('result_count'))

        if next_token is None:
            break

    if args.verbose:
        print >>sys.stderr, 'Total results:', len(tweets_by_author_id)

    if args.all:
        selections = tweets_by_author_id.items()
    else:
        selections = random.sample(tweets_by_author_id.items(), k=args.num_selections)

    print json.dumps(selections, indent=4, sort_keys=True)
