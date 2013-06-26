#!/usr/bin/python

import sys
import pprint
from collections import defaultdict, namedtuple

DOMAIN, \
FIRST_SLASH, \
SECOND_SLASH, \
THIRD_SLASH, \
FOURTH_SLASH, \
FULL_URL = range(6)

Extraction = namedtuple('Extraction', 'keep feedfn')

path_to_extraction = {
	 'tumblr.com': Extraction(keep=DOMAIN, feedfn=None)
	,'community.livejournal.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'www.livejournal.com/users/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'www.livejournal.com/community/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'livejournal.com': Extraction(keep=DOMAIN, feedfn=None)
	,'wordpress.com': Extraction(keep=DOMAIN, feedfn=None)
	,'blogspot.com': Extraction(keep=DOMAIN, feedfn=None)
	,'blogger.com/feeds/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'feeds.feedburner.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'feeds2.feedburner.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'feeds.rapidfeeds.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'posterous.com': Extraction(keep=DOMAIN, feedfn=None)
	,'groups.google.com/group/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'groups.yahoo.com/group/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'typepad.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'typepad.jp': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'blog.roodoo.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'diarynote.jp': Extraction(keep=DOMAIN, feedfn=None)
	,'ameblo.jp': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'rssblog.ameba.jp': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'wretch.cc/blog/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'formspring.me': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'blog.shinobi.jp': Extraction(keep=DOMAIN, feedfn=None)
	,'rss.exblog.jp/rss/exblog/': Extraction(keep=THIRD_SLASH, feedfn=None)
	,'exblog.jp': Extraction(keep=DOMAIN, feedfn=None)
	,'blog.hexun.com': Extraction(keep=DOMAIN, feedfn=None)
	,'blog.hexun.com.tw': Extraction(keep=DOMAIN, feedfn=None)
	,'blog.livedoor.jp': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'altervista.org': Extraction(keep=DOMAIN, feedfn=None)
	,'feeds.qzone.qq.com/cgi-bin/': Extraction(keep=FULL_URL, feedfn=None)
	,'qzone.qq.com': Extraction(keep=DOMAIN, feedfn=None)
	,'blog.163.com': Extraction(keep=DOMAIN, feedfn=None)
	,'inube.com': Extraction(keep=DOMAIN, feedfn=None)
	,'rss.my.nero.com/user/': Extraction(keep=FULL_URL, feedfn=None)
	,'my.nero.com': Extraction(keep=DOMAIN, feedfn=None)
	,'feed43.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'static.blog4ever.com': Extraction(keep=FULL_URL, feedfn=None)
	,'www.xanga.com': Extraction(keep=FULL_URL, feedfn=None)
	,'xanga.com': Extraction(keep=DOMAIN, feedfn=None)
	,'feed.pixnet.net/blog/posts/rss/': Extraction(keep=FOURTH_SLASH, feedfn=None)
	,'feed.pixnet.net/blog/posts/atom/': Extraction(keep=FOURTH_SLASH, feedfn=None)
	,'pixnet.net': Extraction(keep=DOMAIN, feedfn=None)
	,'twitter.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'rss2lj.net': Extraction(keep=FULL_URL, feedfn=None)
	,'gplusrss.com': Extraction(keep=FULL_URL, feedfn=None)
	,'googleplusfeed.net': Extraction(keep=FULL_URL, feedfn=None)
	,'twitter-rss.com': Extraction(keep=FULL_URL, feedfn=None)
	,'dreamwidth.org': Extraction(keep=DOMAIN, feedfn=None)
	,'blog.com': Extraction(keep=DOMAIN, feedfn=None)
	,'pipes.yahoo.com': Extraction(keep=FULL_URL, feedfn=None)
	,'page2rss.com': Extraction(keep=FULL_URL, feedfn=None)
	,'boards.4chan.org': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'dis.4chan.org/atom/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'vox.com': Extraction(keep=DOMAIN, feedfn=None)
	,'jux.com': Extraction(keep=DOMAIN, feedfn=None)
	,'at.webry.info': Extraction(keep=DOMAIN, feedfn=None)
	,'rsspect.com': Extraction(keep=FULL_URL, feedfn=None)
	,'buzz.googleapis.com': Extraction(keep=FULL_URL, feedfn=None)
	,'craigslist.org': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'www.reddit.com/user/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'pay.reddit.com/user/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'www.reddit.com/r/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'pay.reddit.com/r/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'blog.myspace.com/blog/rss.cfm': Extraction(keep=FULL_URL, feedfn=None)
	,'spaces.live.com': Extraction(keep=DOMAIN, feedfn=None)
	,'rss.searchyc.com': Extraction(keep=FULL_URL, feedfn=None)
	,'lesswrong.com/user/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'www.quora.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'www.google.com/reader/public/': Extraction(keep=FULL_URL, feedfn=None)
	# skipped kickstarter
	,'del.icio.us/rss/': Extraction(keep=FULL_URL, feedfn=None)
	,'del.icio.us/tag/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'youtube.com/user/': Extraction(keep=SECOND_SLASH, feedfn=None)
	,'youtube.com/rss/': Extraction(keep=FULL_URL, feedfn=None)
	,'gdata.youtube.com/feeds/': Extraction(keep=FULL_URL, feedfn=None)
	,'multiply.com': Extraction(keep=DOMAIN, feedfn=None)
	,'bandcamp.com/feed/': Extraction(keep=FULL_URL, feedfn=None)
	,'bandcamp.com': Extraction(keep=DOMAIN, feedfn=None)
	,'hatena.ne.jp': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'vimeo.com': FIRST_SLASH # needs to be filtered afterwards to get usernames and exclude video Extraction(keep=IDs, feedfn=None)
	,'flickr.com/services/feeds/': Extraction(keep=FULL_URL, feedfn=None)
	,'flickr.com/recent_comments_feed.gne': Extraction(keep=FULL_URL, feedfn=None)
	,'api.twitter.com/1/statuses/': Extraction(keep=FULL_URL, feedfn=None)
	,'twitter.com/statuses/user_timeline/': Extraction(keep=FULL_URL, feedfn=None)
	,'rss.egloos.com': Extraction(keep=FULL_URL, feedfn=None)
	,'egloos.com': Extraction(keep=DOMAIN, feedfn=None)
	,'podomatic.com': Extraction(keep=DOMAIN, feedfn=None)
	,'secuobs.com/revue/xml/': Extraction(keep=FULL_URL, feedfn=None)
	,'blogs.com': Extraction(keep=DOMAIN, feedfn=None)
	,'mysyndicaat.com/myfeed/feed/': Extraction(keep=FULL_URL, feedfn=None)
	,'blog.sina.com.cn/rss/': Extraction(keep=FULL_URL, feedfn=None)
	,'blog.sina.com.cn': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'loadaveragezero.com/drx/rss/': Extraction(keep=FULL_URL, feedfn=None)
	,'feedsky.com': Extraction(keep=FULL_URL, feedfn=None)
	,'rss.pics.livedoor.com': Extraction(keep=FULL_URL, feedfn=None)
	,'news.livedoor.com/rss/': Extraction(keep=FULL_URL, feedfn=None)
	,'podbean.com': Extraction(keep=DOMAIN, feedfn=None)
	,'blogs.msdn.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	,'libsyn.com': Extraction(keep=DOMAIN, feedfn=None)
	,'prlog.org/rss/': Extraction(keep=FULL_URL, feedfn=None)
	,'npr.org/rss/': Extraction(keep=FULL_URL, feedfn=None)
	# TODO: spaces.msn.com; has annoying pattern
	,'blog.yam.com/rss.php': Extraction(keep=FULL_URL, feedfn=None)
	,'blog.yam.com': Extraction(keep=FIRST_SLASH, feedfn=None)
	# TODO: news.google.com, needs filter on output=(rss|atom)
	,'webcast.berkeley.edu/media/common/rss/': Extraction(keep=FULL_URL, feedfn=None)
}

_domain_to_extraction = defaultdict(list)
for k, extraction in path_to_extraction.iteritems():
	try:
		domain, path = k.split('/', 1)
	except ValueError:
		domain = k
		path = ''
	_domain_to_extraction[domain].append((path, extraction))

for k, extraction in _domain_to_extraction.iteritems():
	_domain_to_extraction[k] = sorted(_domain_to_extraction[k], key=lambda x: len(x), reverse=True)

##pprint.pprint(dict(_domain_to_extraction))


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
		actions = _domain_to_extraction.get(domain_variant)
		if actions:
			break

	if not actions:
		return None

	action = None
	for action_path, maybe_action in actions:
		##print rest, action_path
		if rest.startswith(action_path):
			action = maybe_action
			break

	if action:
		return action.keep

	return None


assert get_action("blah.com", "") == None
assert get_action("youtube.com", "user/blah") == SECOND_SLASH
assert get_action("youtube.com", "usx") == None
assert get_action("bandcamp.com", "feed/blah") == FULL_URL, get_action("bandcamp.com", "feed/blah")
assert get_action("bandcamp.com", "fee") == DOMAIN
assert get_action("x.bandcamp.com", "") == DOMAIN


def without_query(rest):
	rest = rest.split("?", 1)[0]
	rest = rest.split("&", 1)[0]
	return rest


def main():
	if sys.argv[1:] == ["print_paths"]:
		print "\n".join(sorted(path_to_extraction.keys()))
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
