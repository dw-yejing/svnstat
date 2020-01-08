# encoding: utf-8

import logging
import configparser
import os

def checkout(cmd):
    os.system(cmd)

def generate_log(cmd):
    os.system(cmd)

def statistics(cmd):
    os.system(cmd)

def invoke_browser(cmd):
    os.system(cmd)

if __name__=="__main__":
    cwd = os.getcwd()
    logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(asctime)s - %(message)s")
    handler = logging.FileHandler(filename="logger.log", encoding="utf-8")
    logger = logging.getLogger(name="init")
    logger.addHandler(handler)
    cf = configparser.RawConfigParser()
    cf.read("config.ini", encoding="utf-8")
    cf.options("config")
    url = cf.get("config", "url")
    username = cf.get("config", "username")
    password = cf.get("config", "password")
    local_path = cf.get("config", "local_path")
    svn_log_fpath = cf.get("config", "svn_log_fpath")
    svn_dist_path = cf.get("config", "svn_dist_path")
    period_switch = cf.get("config", "period_switch")
    period = cf.get("config", "period")
    browser = cf.get("config", "browser")
    start_date = None
    end_date = None
    if period and len(period)>16:
        start_date = "{}-{}-{}".format(period[0:4], period[4:6], period[6:8])
        end_date = "{}-{}-{}".format(period[9:13], period[13:15], period[15:17])
    checkout_cmd = "svn checkout {} {} --username {} --password {}".format(url, local_path, username, password)
    log_cmd = None
    if period_switch.lower()=="true":
        if (not start_date) or (not end_date):
            logger.info("未配置统计的开始结束区段")
        log_cmd = "svn log -v --xml  -r {{{}}}:{{{}}} > {} > {}".format(start_date, end_date, local_path, svn_log_fpath)
    else:
        log_cmd = "svn log -v --xml > {} > {}".format(local_path, svn_log_fpath)
    statistics_cmd = "java -jar statsvn.jar {} {} -charset gbk -output-dir {}".format(svn_log_fpath, local_path, svn_dist_path)
    html = os.path.join(svn_dist_path, "index.html")
    browser_cmd = "{} {}".format(browser, html)
    checkout(checkout_cmd)
    os.chdir(local_path)
    generate_log(log_cmd)
    os.chdir(cwd)
    statistics(statistics_cmd)
    invoke_browser(browser_cmd)
    
