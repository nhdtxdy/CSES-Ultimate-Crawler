import requests
from urllib3 import encode_multipart_formdata
from bs4 import BeautifulSoup
from time import sleep
import json
import os
import pdfkit

base = 'https://cses.fi'

def make_pdf(d : dict):
    counter = 0
    for item in d.items():
        counter += 1
        problem = item[0]
        print('Making pdf for problem', problem, counter/299*100, '%')
        test_number = 0
        folder_name = 'CSES_' + problem
        path = './DATA/' + folder_name
        if not os.path.exists(path):
            os.makedirs(path)
        url = base + '/problemset/task/' + problem
        pdfkit.from_url(url, path + '/statement.pdf')

def main(csrf_token : str, session_id : str):
    problem_list = []
    problem_html = {}
    submission_result = {}
    with open('problem_html.json', 'r') as f:
        problem_html = json.load(f)
    with open('submission_result.json', 'r') as f:
        submission_result = json.load(f)
    problem_list = [int(x) for x in problem_html.keys()]
    make_pdf(problem_html)


#2f9e68b2ef201db79f7eef87d76b6c6c *csrf_token
#d0b963d0e63ac97ab193805e944dc28e682aa655 *session_id
main('274b88a66aadd9133a98e3c0cf86b6bd', '01a51609e2610e0b4cb2fd0b85301f0cd1d23c0f')




