#!/usr/bin/env python
import urllib2, json, sys, re

if len(sys.argv) != 2:
    print 'usage: %s <video-url>' % sys.argv[0]
    sys.exit(1)
watch_url = sys.argv[1]

# Fetch the video page HTML
watch_html = urllib2.urlopen(watch_url).read()

# Search the HTML for the URL of the video file
match = re.search(r"img.src = '([^']*)';", watch_html)
if match is None:
    print 'unable to find flv url'
    sys.exit(1)

# The video file URL is extracted from some Javascript that needs decoding
flv_url = json.loads('"%s"' % match.group(1)).replace('generate_204', 'videoplayback')
print 'flv url:', flv_url

# Download the video file
open('video.flv', 'wb').write(urllib2.urlopen(flv_url).read())

# That's it!
#
# Some ideas on going further:
#
# Send a fake HTTP User-Agent string using urllib2.build_opener() and
# opener.addheaders = [('User-Agent', '...')].  This way the video downloader
# won't stand out and looks like a "real" web browser.
#
# Use the urllib2.urlopen(url[, data][, timeout]) arguments to specify a
# timeout should the request take too long.  This will make the downloader more
# robust in case the connection goes bad or the server takes too long to
# respond.
#
# The video file is downloaded in one go by a single read() call.  This forces
# the entire video to be downloaded and kept in memory *before* writing it to a
# file.  This consumes a lot of memory.  Try using fixed-size calls like
# read(256 * 1024) in a loop to stream the video and avoid keeping it all in
# memory.  This also lets you add a progress indicator during the download!
