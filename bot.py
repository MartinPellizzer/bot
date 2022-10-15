import twitter_bot
import twitter_comment
import time

while True:
    ########################################################
    # TWITTER
    ########################################################
    err = twitter_comment.comment()
    if err: log('FAILED: twitter_comment.comment')

    time.sleep(7200)

