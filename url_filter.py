#!/usr/bin/python

import sys

SUBDOMAIN, \
FIRST_SLASH, \
SECOND_SLASH, \
THIRD_SLASH, \
FOURTH_SLASH, \
SUBDOMAIN_AND_FIRST_SLASH, \
FULL_URL = range(7)

domain_to_action = {
	 'tumblr.com': SUBDOMAIN
	,'community.livejournal.com': FIRST_SLASH
	,'www.livejournal.com': SECOND_SLASH
	,'livejournal.com': SUBDOMAIN
	,'wordpress.com': SUBDOMAIN
	,'blogspot.com': SUBDOMAIN
	,'blogger.com': SECOND_SLASH
	,'feeds.feedburner.com': SECOND_SLASH
	,'feeds2.feedburner.com': SECOND_SLASH
	,'feeds.rapidfeeds.com': FIRST_SLASH
	,'posterous.com': SUBDOMAIN
	,'groups.google.com': SECOND_SLASH
	,'groups.yahoo.com': SECOND_SLASH
	,'typepad.com': SUBDOMAIN_AND_FIRST_SLASH
	,'typepad.jp': SUBDOMAIN_AND_FIRST_SLASH
	,'blog.roodoo.com': FIRST_SLASH
	,'diarynote.jp': SUBDOMAIN
	,'ameblo.jp': FIRST_SLASH
	,'rssblog.ameba.jp': FIRST_SLASH
	,'wretch.cc': SECOND_SLASH
	,'formspring.me': FIRST_SLASH
	,'blog.shinobi.jp': SUBDOMAIN
	,'rss.exblog.jp': THIRD_SLASH
	,'exblog.jp': SUBDOMAIN
	,'blog.hexun.com': SUBDOMAIN
	,'blog.hexun.com.tw': SUBDOMAIN
	,'blog.livedoor.jp': FIRST_SLASH
	,'altervista.org': SUBDOMAIN
	,'feeds.qzone.qq.com': SECOND_SLASH
	,'qzone.qq.com': SUBDOMAIN
	,'blog.163.com': SUBDOMAIN
	,'inube.com': SUBDOMAIN
	,'feed43.com': FIRST_SLASH
	,'static.blog4ever.com': FULL_URL
	,'www.xanga.com': FULL_URL
	,'xanga.com': SUBDOMAIN
	,'feed.pixnet.net': FOURTH_SLASH
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
	,'dis.4chan.org': SECOND_SLASH
	,'vox.com': SUBDOMAIN
	,'jux.com': SUBDOMAIN
	,'at.webry.info': SUBDOMAIN
	,'rsspect.com': FULL_URL
	,'buzz.googleapis.com': FULL_URL
	,'craigslist.org': SUBDOMAIN_AND_FIRST_SLASH
}

# TODO: subdomain should not get "www" - get next segment instead (needed for blogspot.com)

# TODO: should *_SLASH get rid of ? and & params like href="/blog/kuni&rss20=1"

def main():
	if sys.argv[1:] == ["gimme_domains"]:
		print "\n".join(domain_to_action.keys())
		sys.exit(0)




if __name__ == '__main__':
	main()