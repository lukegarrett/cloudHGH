import tweepy

my_consumer_key="3WrbGEmJo2M4Dz4OBZFKIdv6N"
my_consumer_secret="soCXeKGa5PrC6G6h91fkZMp8JvxxpG4Hot0YSE20xqts4a7E6Y"
my_access_token="1379746468731490305-FlumCi8zzCi2rbmAGdWcSt63fv9wP2"
my_access_token_secret="RuBPoGxUmtBJ5PCjfliIiGcCMxcMwQloyA04hClykWRpu"
client = tweepy.Client(consumer_key=my_consumer_key,
                       consumer_secret=my_consumer_secret,
                       access_token=my_access_token,
                       access_token_secret=my_access_token_secret)



stream = tweepy.Stream(
  my_consumer_key, my_consumer_secret,
  my_access_token, my_access_token_secret
)

stream.filter(track=["covid"])

class IDPrinter(tweepy.Stream):

    def on_status(self, status):
        print(status.id)


printer = IDPrinter(
  my_consumer_key, my_consumer_secret,
  my_access_token, my_access_token_secret
)
printer.sample()