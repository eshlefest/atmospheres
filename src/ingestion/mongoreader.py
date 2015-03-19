from pymongo import MongoClient

DEFAULT_DATABASE = "tweetdata"
DEFAULT_COLLECTION = "tweets"

class MongoBridge:

    def __init__(this):
        this.client = MongoClient()
        this.db = this.client[database]
        this.collection = this.db[collection]

    def __init__(this, database=DEFAULT_DATABASE,collection=DEFAULT_COLLECTION):
        this.client = MongoClient()
        this.db = this.client[database]
        this.collection = this.db[collection]

    def text_regex_query(this,regex):
        query = {}
        query["text"] = {"$regex":regex}
        return this.collection.find_one(query)

    def get_N_results(this,regex,n):
        query = {}
        query["text"] = {"$regex":regex}
        cursor = this.collection.find(query)

        res = [cursor.next() for i in range(n)]
        return res

    def close(this):
        this.client.close()

    def write(this,data):
        this.collection.insert(data)



if __name__ == "__main__":
    
    mongo = MongoReader()
    t = mongo.get_N_results("\\:\\)",10)
    for r in t:
        print r["text"]


    mongo.close()