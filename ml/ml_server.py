import requests
import base64
import json
import random
import urllib
import nltk

from collections import Counter
from nltk.stem.lancaster import LancasterStemmer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import urlparse, parse_qs

def gen_text_from_image(url):
    GOOGLE_API_KEY = ""
    GOOGLE_CLOUD_VISION_URL = "https://vision.googleapis.com/v1/images:annotate"

    try:
        img = urllib.urlopen(url).read()
    except Exception:
        return ""

    b64_string = base64.b64encode(img)

    req_data = {
      "requests":[
        {
          "image":{
            "content": b64_string
          },
          "features":[
            {
              "type":"LABEL_DETECTION",
              "maxResults": 5
            }
          ]
        }
      ]
    }

    r = requests.post("%s?key=%s" % (GOOGLE_CLOUD_VISION_URL, GOOGLE_API_KEY), json.dumps(req_data), headers={'content-type': 'application/json'})

    js = json.loads(r.text)

    words = []
    for match in js["responses"][0]["labelAnnotations"]:
        words.append(match["description"])

    nice_adjectives = [
        "excellent",
        "high-class",
        "terrific",
        "exceptional",
        "remarkable",
        "top quality",
        "exquisite",
        "amazing",
        "extraordinary",
        "humble",
        "fabulous",
        "resplendent",
        "impressive",
        "attractive",
        "fantastic",
        "outstanding",
        "awesome",
        "incredible",
        "beautiful",
        "dazzling",
        "sensational",
        "unequaled",
        "perfect",
        "delightful",
        "inspiring",
        "breathtaking",
        "gallant",
        "bright",
        "shining",
        "brilliant",
        "sparkling",
        "elegant",
        "gleaming",
        "spectacular",
        "splendid",
        "enchanting",
        "good",
        "charming",
        "gorgeous",
        "lovely",
        "stunning",
        "endearing",
        "graceful",
        "super",
        "wonderful",
        "gracious",
        "luminous",
        "superb",
        "worthy",
        "great",
        "magnificent",
        "marvelous",
    ]

    beginning = [
        "What ",
        "Wow, what ",
        "It's such ",
        "Wow, it's such ",
    ]

    generated = []

    for word in words:
        addition = "a"
        pick = random.choice(nice_adjectives)
        if pick[0] in ('a', 'e', 'i', 'o', 'u'):
            addition += "n"

        generated.append(random.choice(beginning) + addition + " " + pick + " " + word + random.choice([".", "!"]))

    return generated

st = LancasterStemmer()

def gen_text_from_tweets(tweets):
    API_KEY = ""
    URL_SENTIMENT_API = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'
    URL_KEYPHRASES_API = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'

    new_tweets = []
    new_tweet = ""
    cnt = 0
    for tweet in tweets:
        cnt += 1
        new_tweet += tweet + ". "

        if cnt > 20:
            new_tweets.append(new_tweet)
            new_tweet = ""
            cnt = 0

    documents = []

    for i, tweet in enumerate(new_tweets):
        documents.append({
            "language": "en",
            "id": str(i + 1),
            "text": tweet
        })

    text = json.dumps({"documents": documents})


    headers = {
        'Ocp-Apim-Subscription-Key': API_KEY,
        'Content-type': 'application/json',
        'Accept': 'application/json'
    }

    api_response_sentiment = requests.post(URL_SENTIMENT_API, headers=headers, data=text)
    api_response_keyphrases = requests.post(URL_KEYPHRASES_API, headers=headers, data=text)

    res_sentiment = json.loads(json.dumps(json.loads(api_response_sentiment.content), indent=2, sort_keys=True))
    res_keyphrases = json.loads(json.dumps(json.loads(api_response_keyphrases.content), indent=2, sort_keys=True))

    result = []
    for (sent, keyp) in zip(res_sentiment["documents"], res_keyphrases["documents"]):
        result.extend(keyp["keyPhrases"])

    return result

def gen_attributes(keywords):
    
    flattened = []
    for keyword in keywords:
        flattened.extend(keyword.split(" "))

    top_words = Counter()
    for keyword in flattened:
        top_words[keyword] += 1

    result = []
    count = 0
    for word, i in top_words.most_common():
        if len(word) > 2 and nltk.pos_tag(st.stem(word))[0][1] == 'NN' or len(word) > 2 and word[0].isupper():
            count += 1
            result.append(word)

            if count == 56:
                break

    return result

PORT_NUMBER = 8080

class myHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        try:
            query_components = parse_qs(urlparse(self.path).query)
            url = query_components["url"][0]
        except Exception:
            return

        text = gen_text_from_image(url)

        result = "<br>"
        for paragraph in text:
            result += '<p style="color: white;">' + paragraph + "</p>"
        self.wfile.write(result)

        return

    def do_POST(self):
        self.send_response(200)

        try:
            tweets = json.loads(self.rfile.read(int(self.headers['Content-length'])))
        except Exception:
            return

        self.send_header('Content-type', 'text/html')
        self.end_headers()

        result = ""
        cur_line = "<p>"
        text = gen_text_from_tweets(tweets["tweets"])
        attributes = gen_attributes(text)
        for i, word in enumerate(attributes):
            if i % 8 == 0:
                result += cur_line + "</p>"
                cur_line = "<p>" + word
                continue
            cur_line += "\t\t\t" + word
        result += cur_line + "</p>"
        self.wfile.write(result)
        return


try:
    server = HTTPServer(('', PORT_NUMBER), myHandler)

    print 'Started httpserver on port ', PORT_NUMBER

    server.serve_forever()

except KeyboardInterrupt:
    server.socket.close()