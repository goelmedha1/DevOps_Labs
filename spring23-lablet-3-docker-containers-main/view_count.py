import os
import atexit

from flask import Flask
import redis
import emoji

# If the REDIS_HOST environment variable is set, use it.
# Otherwise, use the hostname "redis" as the default.
redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379)
# Set view count to 0 if the key doesn't exist
r.setnx("view_count", 0)
# Persist the value of the view count to Redis when the application exits.
atexit.register(r.save)

app = Flask(__name__)

@app.route("/")
def hello():
    # Increment the view count
    count = r.incr("view_count")
    e = emoji.emojize(":eye:")
    return f"{e} This page has been viewed {count} times.\n"

app.run(host="0.0.0.0" , port=80)
