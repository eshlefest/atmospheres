from pymongo import MongoClient



class MongoReader:
    DEFAULT_DATABASE = "tweetdata"
    DEFAULT_COLLECTION = "tweets"

    def __init__(self, database=DEFAULT_DATABASE,collection=DEFAULT_COLLECTION):
        self.client = MongoClient()
        self.db = self.client[database]
        self.collection = self.db[collection]

    def text_regex_query(self, regex):
        """ returns one document from db whose text field matches regex """
        query = {}
        query["text"] = {"$regex":regex}
        return self.collection.find_one(query)

    def get_N_results(self, regex, n):
        """ returns N results from the db whose text field matches regex """
        query = {}
        query["text"] = {"$regex":regex}
        cursor = self.collection.find(query)

        res = [cursor.next() for i in range(n)]
        return res

    def close(self):
        self.client.close()

    def write(self, data):
        """ writes data to db """
        self.collection.insert(data)



if __name__ == "__main__":
    
    mongo = MongoReader()
    t = mongo.get_N_results("\\:\\)",10)
    for r in t:
        print r["text"]


    mongo.close()