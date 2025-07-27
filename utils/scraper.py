import praw

reddit = praw.Reddit(
    client_id="YOUR_ID",
    client_secret="YOUR_SECRET",
    user_agent="toxicity-detector"
)

def fetch_reddit_comments(username):
    user = reddit.redditor(username)
    comments = [c.body for c in user.comments.new(limit=100)]
    return comments
