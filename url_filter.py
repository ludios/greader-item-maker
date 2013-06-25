#!/usr/bin/python

import sys

SUBDOMAIN, \
FIRST_SLASH, \
SECOND_SLASH, \
THIRD_SLASH, \
FOURTH_SLASH, \
SUBDOMAIN_AND_FIRST_SLASH, \
FULL_URL = range(7)

path_to_action = {
	 'tumblr.com': SUBDOMAIN
	,'community.livejournal.com': FIRST_SLASH
	,'www.livejournal.com/users': SECOND_SLASH
	,'www.livejournal.com/community': SECOND_SLASH
	,'livejournal.com': SUBDOMAIN
	,'wordpress.com': SUBDOMAIN
	,'blogspot.com': SUBDOMAIN
	,'blogger.com/feeds': SECOND_SLASH
	,'feeds.feedburner.com': FIRST_SLASH
	,'feeds2.feedburner.com': FIRST_SLASH
	,'feeds.rapidfeeds.com': FIRST_SLASH
	,'posterous.com': SUBDOMAIN
	,'groups.google.com/group': SECOND_SLASH
	,'groups.yahoo.com/group': SECOND_SLASH
	,'typepad.com': SUBDOMAIN_AND_FIRST_SLASH
	,'typepad.jp': SUBDOMAIN_AND_FIRST_SLASH
	,'blog.roodoo.com': FIRST_SLASH
	,'diarynote.jp': SUBDOMAIN
	,'ameblo.jp': FIRST_SLASH
	,'rssblog.ameba.jp': FIRST_SLASH
	,'wretch.cc/blog': SECOND_SLASH
	,'formspring.me': FIRST_SLASH
	,'blog.shinobi.jp': SUBDOMAIN
	,'rss.exblog.jp/rss/exblog': THIRD_SLASH
	,'exblog.jp': SUBDOMAIN
	,'blog.hexun.com': SUBDOMAIN
	,'blog.hexun.com.tw': SUBDOMAIN
	,'blog.livedoor.jp': FIRST_SLASH
	,'altervista.org': SUBDOMAIN
	,'feeds.qzone.qq.com/cgi-bin': FULL_URL
	,'qzone.qq.com': SUBDOMAIN
	,'blog.163.com': SUBDOMAIN
	,'inube.com': SUBDOMAIN
	,'feed43.com': FIRST_SLASH
	,'static.blog4ever.com': FULL_URL
	,'www.xanga.com': FULL_URL
	,'xanga.com': SUBDOMAIN
	,'feed.pixnet.net/blog/posts/rss': FOURTH_SLASH
	,'feed.pixnet.net/blog/posts/atom': FOURTH_SLASH
	,'pixnet.net': SUBDOMAIN
	,'twitter.com': FIRST_SLASH
	,'rss2lj.net': FULL_URL
	,'gplusrss.com': FULL_URL
	,'googleplusfeed.net': FULL_URL
	,'twitter-rss.com': FULL_URL
	,'dreamwidth.org': SUBDOMAIN
	,'blog.com': SUBDOMAIN
	,'pipes.yahoo.com': FULL_URL
	,'page2rss.com': FULL_URL
	,'boards.4chan.org': FIRST_SLASH
	,'dis.4chan.org/atom': SECOND_SLASH
	,'vox.com': SUBDOMAIN
	,'jux.com': SUBDOMAIN
	,'at.webry.info': SUBDOMAIN
	,'rsspect.com': FULL_URL
	,'buzz.googleapis.com': FULL_URL
	,'craigslist.org': SUBDOMAIN_AND_FIRST_SLASH
	,'www.reddit.com/user': SECOND_SLASH
	,'pay.reddit.com/user': SECOND_SLASH
	,'www.reddit.com/r': SECOND_SLASH
	,'pay.reddit.com/r': SECOND_SLASH
	,'blog.myspace.com/blog/rss.cfm': FULL_URL
	,'spaces.live.com': SUBDOMAIN
	,'rss.searchyc.com': FULL_URL
	,'lesswrong.com/user': SECOND_SLASH
	,'www.quora.com': FIRST_SLASH
	,'www.google.com/reader/public': FULL_URL
	# skipped kickstarter
	,'del.icio.us/rss': FULL_URL
	,'del.icio.us/tag': SECOND_SLASH
	,'youtube.com/user': SECOND_SLASH
	,'youtube.com/rss': FULL_URL
	,'gdata.youtube.com/feeds/': FULL_URL
	,'multiply.com': SUBDOMAIN
	,'bandcamp.com/feed': FULL_URL
	,'bandcamp.com': SUBDOMAIN
}

# TODO: subdomain should not get "www" - get next segment instead (needed for blogspot.com)

# TODO: should *_SLASH get rid of ? and & params like href="/blog/kuni&rss20=1"

def main():
	for key in path_to_action.keys():
		assert not key.endswith('/')

	if sys.argv[1:] == ["print_paths"]:
		print "\n".join(path_to_action.keys())
		sys.exit(0)



if __name__ == '__main__':
	main()
