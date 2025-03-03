# Web App - team Web Crawlers

# import modules that are necessary for this program
import pymongo
import datetime
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, abort, url_for, make_response
import pymongo.mongo_client

# make connection to the database
connection = pymongo.MongoClient("mongodb+srv://lgl1876523678:1017@cluster0.k8xwe.mongodb.net/?retryWrites=true&w=majority")