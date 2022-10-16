import requests
from urllib3 import encode_multipart_formdata
from bs4 import BeautifulSoup
from time import sleep
import json
import os
import shutil
import sys

base = 'https://cses.fi'

def get_problem_list(problem_list, problem_html):
    url = base + '/problemset'
    r = requests.get(url)
    bs = BeautifulSoup(r.text, 'html.parser')
    ls = bs.find_all('a', href=True)
    # from ls 9
    for i in range(9, len(ls)):
        problem_url = ls[i]['href']
        task_num = int(problem_url.split('/')[3])
        problem_list.append(task_num)
        url = base + problem_url
        r = requests.get(url)
        if r.status_code != 200:
            print('WHAT THE phuc BR0')
            raise RuntimeError
        problem_html[task_num] = r.text
        print('Successfully cloned task', task_num)

def get_status(entry, cookies):
    url = base + '/ajax/get_status.php?entry=' + entry
    r = requests.get(url, cookies=cookies)
    if r.text == '':
        print('ERROR GETTING STATUS')
        raise RuntimeError
    while r.text != 'READY':
        sleep(0.5)
        r = requests.get(url, cookies=cookies)
    
def submit(problem : int, csrf_token : str, session_id : str, save_dict) -> bool:
    print('Submitting task', problem)
    global base
    fields = {
        "csrf_token": csrf_token,
        "task": problem,
        "file": ("code.cpp", open("code.cpp").read(), "text/plain"),
        "lang":"C++",
        "option":"C++17",
        "type":"course",
        "target":"problemset",
    }
    cookies = {'PHPSESSID':session_id}
    body, header = encode_multipart_formdata(fields)
    headers = {'Content-Type':header}
    url = base + '/course/send.php'
    r = requests.post(url, data=body, headers=headers, cookies=cookies, allow_redirects=False)
    if r.status_code != 302:
        return False
    save_dict[problem] = r.headers['Location']
    entry = r.headers['Location'].split('/')[3]
    print(entry)
    get_status(entry, cookies)
    print('Task', problem, 'ready!')
    return True

def process(d : dict, session_id : str):
    cookies = {'PHPSESSID':session_id}
    counter = 0
    for item in d.items():
        counter += 1
        problem = item[0]
        print('Processing problem', problem, counter/299*100, '%')
        test_number = 0
        folder_name = 'CSES_' + problem
        path = './DATA/' + folder_name
        inp01 = path + '/1.inp'
        if not os.path.exists(path):
            os.makedirs(path)
        if os.path.exists(inp01):
            continue
        print('Problem not processed')
        url = base + item[1]
        r = requests.get(url, cookies = cookies)
        bs = BeautifulSoup(r.text, 'html.parser')
        # print(bs)
        tables = bs.find_all('table', class_='narrow')[2:]
        if len(tables) % 3 != 0:
            print('WHAT THE FUc')
            raise RuntimeError
        for i in range(0, len(tables), 3):
            test_number += 1
            #i : input
            #i+1 : correct output
            input_url = base + tables[i].find_all('a')[1]['href']
            r = requests.get(input_url, cookies=cookies)
            input_content = r.text
            input_file = path + '/' + str(test_number) + '.inp'
            with open(input_file, 'w') as f:
                f.write(input_content)
            
            try:
                output_url = base + tables[i+1].find_all('a')[1]['href']
                r = requests.get(output_url, cookies=cookies)
                output_content = r.text
                output_file = path + '/' + str(test_number) + '.out'
                with open(output_file, 'w') as f:
                    f.write(output_content)
            except:
                output_content = ''
                output_file = path + '/' + str(test_number) + '.out'
                with open(output_file, 'w') as f:
                    f.write(output_content)

def zip_dir(problem_list):
    for problem in problem_list:
        folder_name = 'CSES_' + problem
        path = './DATA/' + folder_name
        shutil.make_archive(path, 'zip', path)


def main(csrf_token : str, session_id : str):
    problem_list = []
    problem_html = {}
    submission_result = {}
    with open('problem_html.json', 'r') as f:
        problem_html = json.load(f)
    with open('submission_result.json', 'r') as f:
        submission_result = json.load(f)
    problem_list = [str(x) for x in problem_html.keys()]
    process(submission_result, session_id)
    # zip_dir(problem_list)


#2f9e68b2ef201db79f7eef87d76b6c6c *csrf_token
#d0b963d0e63ac97ab193805e944dc28e682aa655 *session_id
# main('274b88a66aadd9133a98e3c0cf86b6bd', '01a51609e2610e0b4cb2fd0b85301f0cd1d23c0f')

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])




