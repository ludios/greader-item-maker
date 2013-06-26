#!/usr/bin/python

import sys
from collections import defaultdict

DOMAIN, \
FIRST_SLASH, \
SECOND_SLASH, \
THIRD_SLASH, \
FOURTH_SLASH, \
FULL_URL = range(6)

path_to_action = {
	 'tumblr.com': DOMAIN
	,'community.livejournal.com': FIRST_SLASH
	,'www.livejournal.com/users/': SECOND_SLASH
	,'www.livejournal.com/community/': SECOND_SLASH
	,'livejournal.com': DOMAIN
	,'wordpress.com': DOMAIN
	,'blogspot.com': DOMAIN
	,'blogger.com/feeds/': SECOND_SLASH
	,'feeds.feedburner.com': FIRST_SLASH
	,'feeds2.feedburner.com': FIRST_SLASH
	,'feeds.rapidfeeds.com': FIRST_SLASH
	,'posterous.com': DOMAIN
	,'groups.google.com/group/': SECOND_SLASH
	,'groups.yahoo.com/group/': SECOND_SLASH
	,'typepad.com': FIRST_SLASH
	,'typepad.jp': FIRST_SLASH
	,'blog.roodoo.com': FIRST_SLASH
	,'diarynote.jp': DOMAIN
	,'ameblo.jp': FIRST_SLASH
	,'rssblog.ameba.jp': FIRST_SLASH
	,'wretch.cc/blog/': SECOND_SLASH
	,'formspring.me': FIRST_SLASH
	,'blog.shinobi.jp': DOMAIN
	,'rss.exblog.jp/rss/exblog/': THIRD_SLASH
	,'exblog.jp': DOMAIN
	,'blog.hexun.com': DOMAIN
	,'blog.hexun.com.tw': DOMAIN
	,'blog.livedoor.jp': FIRST_SLASH
	,'altervista.org': DOMAIN
	,'feeds.qzone.qq.com/cgi-bin/': FULL_URL
	,'qzone.qq.com': DOMAIN
	,'blog.163.com': DOMAIN
	,'inube.com': DOMAIN
	,'rss.my.nero.com/user/': FULL_URL
	,'my.nero.com': DOMAIN
	,'feed43.com': FIRST_SLASH
	,'static.blog4ever.com': FULL_URL
	,'www.xanga.com': FULL_URL
	,'xanga.com': DOMAIN
	,'feed.pixnet.net/blog/posts/rss/': FOURTH_SLASH
	,'feed.pixnet.net/blog/posts/atom/': FOURTH_SLASH
	,'pixnet.net': DOMAIN
	,'twitter.com': FIRST_SLASH
	,'rss2lj.net': FULL_URL
	,'gplusrss.com': FULL_URL
	,'googleplusfeed.net': FULL_URL
	,'twitter-rss.com': FULL_URL
	,'dreamwidth.org': DOMAIN
	,'blog.com': DOMAIN
	,'pipes.yahoo.com': FULL_URL
	,'page2rss.com': FULL_URL
	,'boards.4chan.org': FIRST_SLASH
	,'dis.4chan.org/atom/': SECOND_SLASH
	,'vox.com': DOMAIN
	,'jux.com': DOMAIN
	,'at.webry.info': DOMAIN
	,'rsspect.com': FULL_URL
	,'buzz.googleapis.com': FULL_URL
	,'craigslist.org': FIRST_SLASH
	,'www.reddit.com/user/': SECOND_SLASH
	,'pay.reddit.com/user/': SECOND_SLASH
	,'www.reddit.com/r/': SECOND_SLASH
	,'pay.reddit.com/r/': SECOND_SLASH
	,'blog.myspace.com/blog/rss.cfm': FULL_URL
	,'spaces.live.com': DOMAIN
	,'rss.searchyc.com': FULL_URL
	,'lesswrong.com/user/': SECOND_SLASH
	,'www.quora.com': FIRST_SLASH
	,'www.google.com/reader/public/': FULL_URL
	# skipped kickstarter
	,'del.icio.us/rss/': FULL_URL
	,'del.icio.us/tag/': SECOND_SLASH
	,'youtube.com/user/': SECOND_SLASH
	,'youtube.com/rss/': FULL_URL
	,'gdata.youtube.com/feeds/': FULL_URL
	,'multiply.com': DOMAIN
	,'bandcamp.com/feed/': FULL_URL
	,'bandcamp.com': DOMAIN
	,'hatena.ne.jp': FIRST_SLASH
	,'vimeo.com': FIRST_SLASH # needs to be filtered afterwards to get usernames and exclude video IDs
	,'flickr.com/services/feeds/': FULL_URL
	,'flickr.com/recent_comments_feed.gne': FULL_URL
	,'api.twitter.com/1/statuses/': FULL_URL
	,'twitter.com/statuses/user_timeline/': FULL_URL
	,'rss.egloos.com': FULL_URL
	,'egloos.com': DOMAIN
}

_domain_to_action = defaultdict(list)
for k, action in path_to_action.iteritems():
	try:
		domain, path = k.split('/', 1)
	except ValueError:
		domain = k
		path = ''
	_domain_to_action[domain].append((path, action))

for k, action in _domain_to_action.iteritems():
	_domain_to_action[k] = sorted(_domain_to_action[k], key=lambda x: len(x), reverse=True)


def up_domain_variants(domain):
	variants = []
	parts = domain.split('.')
	for how_many in xrange(1, len(parts)):
		variant = '.'.join(parts[-how_many:])
		variants.append(variant)

	variants.reverse()
	return [domain] + variants

assert up_domain_variants("blah.cnn.com") == ["blah.cnn.com", "cnn.com", "com"]


def get_action(domain, rest):
	actions = None

	for domain_variant in up_domain_variants(domain):
		actions = _domain_to_action.get(domain_variant)
		if actions:
			break

	if not actions:
		return None

	action = None
	if len(actions) == 1:
		action = actions[0][1]
	else:
		for action_path, maybe_action in actions:
			if rest.startswith(action_path):
				action = maybe_action

	return action


assert get_action("blah.com", "") == None
assert get_action("youtube.com", "user/blah") == SECOND_SLASH
assert get_action("youtube.com", "usx") == None
assert get_action("bandcamp.com", "feed/blah") == FULL_URL
assert get_action("bandcamp.com", "fee") == DOMAIN
assert get_action("x.bandcamp.com", "") == DOMAIN


def without_query(rest):
	rest = rest.split("?", 1)[0]
	rest = rest.split("&", 1)[0]
	return rest


def main():
	if sys.argv[1:] == ["print_paths"]:
		print "\n".join(sorted(path_to_action.keys()))
		sys.exit(0)

	last_printed = None
	for line in sys.stdin:
		url = line.rstrip()
		try:
			schema, _, domain, rest = url.split('/', 3)
		except ValueError:
			try:
				schema, _, domain = url.split('/', 2)
				rest = ""
			except ValueError:
				continue

		action = get_action(domain, rest)
		if action is None:
			# Don't want this URL
			continue
		elif action == FULL_URL:
			maybe_print = url
		elif action == DOMAIN:
			maybe_print = schema + "//" + domain
		elif action == FIRST_SLASH:
			maybe_print = schema + "//" + domain + "/" + without_query(rest.split("/", 1)[0])
		elif action == SECOND_SLASH:
			maybe_print = schema + "//" + domain + "/" + without_query("/".join(rest.split("/", 2)[:2]))
		elif action == THIRD_SLASH:
			maybe_print = schema + "//" + domain + "/" + without_query("/".join(rest.split("/", 2)[:3]))
		elif action == FOURTH_SLASH:
			maybe_print = schema + "//" + domain + "/" + without_query("/".join(rest.split("/", 2)[:4]))

		if last_printed != maybe_print:
			print maybe_print
			last_printed = maybe_print


if __name__ == '__main__':
	main()
