# -*- coding: utf-8 -*-
#######################################################
# This script saves result data                       #
# It expects the format of unladen swallow's perf.py  #
#######################################################
import urllib, urllib2
from datetime import datetime

#SPEEDURL = 'http://127.0.0.1:8000/'
SPEEDURL = 'http://speed.pypy.org/'

def save(project, revision, results, options, executable, environment, testing=False):
    testparams = []
    #Parse data
    data = {}
    current_date = datetime.now()
    for b in results:
        bench_name = b[0]
        res_type = b[1]
        results = b[2]
        value = 0
        if res_type == "ComparisonResult":
            value = results['avg_changed']
        elif res_type == "SimpleComparisonResult":
            value = results['changed_time']
        else:
            print(f"ERROR: result type unknown {b[1]}")
            return 1
        data = {
            'commitid': revision,
            'project': project,
            'executable': executable,
            'benchmark': bench_name,
            'environment': environment,
            'result_value': value,
        }
        if res_type == "ComparisonResult":
            data['std_dev'] = results['std_changed']
        if testing: testparams.append(data)
        else: send(data)
    return testparams if testing else 0

def send(data):
    #save results
    params = urllib.urlencode(data)
    f = None
    response = "None"
    info = f"{str(datetime.now())}: Saving result for " + data['executable']
    info += " revision " + " " + str(data['commitid']) + ", benchmark "
    info += data['benchmark']
    print(info)
    try:
        f = urllib2.urlopen(f'{SPEEDURL}result/add/', params)
        response = f.read()
        f.close()
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            response = '\n  We failed to reach a server\n'
            response += f'  Reason: {str(e.reason)}'
        elif hasattr(e, 'code'):
            response = '\n  The server couldn\'t fulfill the request\n'
            response += f'  Error code: {str(e)}'
        print("Server (%s) response: %s\n" % (SPEEDURL, response))
        return 1
    return 0
