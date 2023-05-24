#!/usr/bin/python
#
# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import random
import uuid
import time
import requests
# from locust import HttpUser, task, between

# from opentelemetry import context, baggage, trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
# from opentelemetry.instrumentation.requests import RequestsInstrumentor
# from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor

# tracer_provider = TracerProvider()
# trace.set_tracer_provider(tracer_provider)
# tracer_provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter()))

# # Instrumenting manually to avoid error with locust gevent monkey
# RequestsInstrumentor().instrument()
# URLLib3Instrumentor().instrument()

categories = [
    "binoculars",
    "telescopes",
    "accessories",
    "assembly",
    "travel",
    "books",
    None,
]

products = [
    "0PUK6V6EV0",
    "1YMWWN1N4O",
    "2ZYFJ3GM2N",
    "66VCHSJNUP",
    "6E92ZMYYFZ",
    "9SIQT8TOJO",
    "L9ECAV7KIM",
    "LS4PSXUNUM",
    "OLJCESPC7Z",
    "HQTGWGPNH4",
]

people_file = open('people.json')
people = json.load(people_file)
frontend_addr = "http://frontend:8080"

def add_to_cart(user=""):
        if user == "":
            user = str(uuid.uuid1())
        product = random.choice(products)
        requests.get(frontend_addr + "/api/products/" + product)
        cart_item = {
            "item": {
                "productId": product,
                "quantity": random.choice([1, 2, 3, 4, 5, 10]),
            },
            "userId": user,
        }
        requests.post(frontend_addr + "/api/cart", json=cart_item)

def perform(task):
    try:
        if (task == 1):
            requests.get(frontend_addr)
        elif (task == 2):
            requests.get(frontend_addr + "/api/products/" + random.choice(products))
        elif (task == 3):
            params = {
                "productIds": [random.choice(products)],
            }
            requests.get(frontend_addr + "/api/recommendations/", params=params)
        elif (task == 4):
            params = {
                "contextKeys": [random.choice(categories)],
            }
            requests.get(frontend_addr + "/api/data/", params=params)
        elif (task == 5):
            requests.get(frontend_addr + "/api/cart")
        elif (task == 6):
            user = str(uuid.uuid1())
            add_to_cart(user=user)
            checkout_person = random.choice(people)
            checkout_person["userId"] = user
            requests.post(frontend_addr + "/api/checkout", json=checkout_person)
        elif (task == 7):
            user = str(uuid.uuid1())
            for i in range(random.choice([2, 3, 4])):
                add_to_cart(user=user)
            checkout_person = random.choice(people)
            checkout_person["userId"] = user
            requests.post(frontend_addr + "/api/checkout", json=checkout_person)
    except Exception as e:
        print("load-generator2: FAILED TO CONNECT TO FRONTEND")
        print(e)

time.sleep(10)
while (1==1):
    task_num = random.randint(1, 7)
    perform(task_num)
    time.sleep(random.randint(0, 2))

# class WebsiteUser(HttpUser):
#     wait_time = between(1, 10)

#     @task(1)
#     def index(self):
#         self.client.get("/")

#     @task(10)
#     def browse_product(self):
#         self.client.get("/api/products/" + random.choice(products))

#     @task(3)
#     def get_recommendations(self):
#         params = {
#             "productIds": [random.choice(products)],
#         }
#         self.client.get("/api/recommendations/", params=params)

#     @task(3)
#     def get_ads(self):
#         params = {
#             "contextKeys": [random.choice(categories)],
#         }
#         self.client.get("/api/data/", params=params)

#     @task(3)
#     def view_cart(self):
#         self.client.get("/api/cart")

#     @task(2)
#     def add_to_cart(self, user=""):
#         if user == "":
#             user = str(uuid.uuid1())
#         product = random.choice(products)
#         self.client.get("/api/products/" + product)
#         cart_item = {
#             "item": {
#                 "productId": product,
#                 "quantity": random.choice([1, 2, 3, 4, 5, 10]),
#             },
#             "userId": user,
#         }
#         self.client.post("/api/cart", json=cart_item)

#     @task(1)
#     def checkout(self):
#         # checkout call with an item added to cart
#         user = str(uuid.uuid1())
#         self.add_to_cart(user=user)
#         checkout_person = random.choice(people)
#         checkout_person["userId"] = user
#         self.client.post("/api/checkout", json=checkout_person)

#     @task(1)
#     def checkout_multi(self):
#         # checkout call which adds 2-4 different items to cart before checkout
#         user = str(uuid.uuid1())
#         for i in range(random.choice([2, 3, 4])):
#             self.add_to_cart(user=user)
#         checkout_person = random.choice(people)
#         checkout_person["userId"] = user
#         self.client.post("/api/checkout", json=checkout_person)

    # def on_start(self):
    #     ctx = baggage.set_baggage("synthetic_request", "true")
    #     context.attach(ctx)
    #     self.index()
