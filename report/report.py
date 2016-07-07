# -*- coding:utf-8 -*-
import os
import copy
import zipfile
import ConfigParser
from ftplib import FTP
import util
import Parser
import requests
import json

from pyexcel_xls import get_data
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('./templates'))
template = env.get_template('report.html')


class LRReport:

    build_id = ""
    datafile_prefix = ""
    result_dir = ""
    session_dir = ""
    report_file = ""
    pdf_file = ""
    package_file = ""
    config_file = ""
    ftp_conf = {}
    api_url = ""
    api_flag = 0
    api_monitor_type = ""

    # 用于上传数据
    summary_data = {}

    def __init__(self, result_dir, prefix, build_id,
                 config_file="../conf/report.ini"):
        self.result_dir = copy.copy(result_dir)
        self.config_file = copy.copy(config_file)
        self.datafile_prefix = copy.copy(prefix)
        temp_build_id = "".join(build_id.split('-'))
        self.build_id = "".join(temp_build_id.split('_'))
        self.build_id = self.build_id[:12]

    def get_conf(self):
        """
        get configuration from ini file
        """
        config = ConfigParser.ConfigParser()
        with open(self.config_file, "r") as cfg_file:
            config.readfp(cfg_file)
        self.ftp_conf.setdefault("flag", int(config.get("ftp", "flag")))
        self.ftp_conf.setdefault("ip", config.get("ftp", "ip"))
        self.ftp_conf.setdefault("user", config.get("ftp", "user"))
        self.ftp_conf.setdefault("password", config.get("ftp", "password"))
        self.api_url = config.get("api", "url")
        self.api_flag = int(config.get("api", "flag"))
        self.api_monitor_type = config.get('api', 'type')

    def set_file_name(self):
        time_stamp = self.build_id
        self.report_file = (self.result_dir + "\\" + self.datafile_prefix + "_lr_" + time_stamp + ".html")
        self.package_file = self.report_file.split(".html")[0] + ".zip"
        self.session_dir = self.result_dir + "\\" + "An_Session1"

    def get_html_msg(self):
        runner_user_hyper_link = r"An_Report1/Report0.png"
        hits_per_second_hyper_link = r"An_Report1/Report1.png"
        throughput_hyper_link = r"An_Report1/Report2.png"
        response_time_hyper_link = r"An_Report1/Report4.png"
        tps_hyper_link = r"An_Report1/Report5.png"

        summary_data = {}
        summary_file = self.result_dir + "\\An_Report1\\summary.html"
        if os.path.exists(summary_file):
            summary_parser = Parser.LRParser()
            f = open(summary_file, "r")
            try:
                for line in f.readlines():
                    summary_parser.feed(line)
                summary_data = summary_parser.work()
            finally:
                f.close()
        else:
            print "[ERROR]can not find summary.html in lr report directory"

        tps_data = {}
        tps_file = self.result_dir + "\\An_Report1\\Report5.html"
        if os.path.exists(tps_file):
            report5_parser = Parser.LRParser()
            f = open(tps_file, "r")
            try:
                for line in f.readlines():
                    report5_parser.feed(line)
                tps_data = report5_parser.work()
            finally:
                f.close()
        else:
            print "[ERROR]can not find Report5.html in lr report directory"

        passed = float(summary_data.get("total_passed"))
        failed = float(summary_data.get("total_failed"))
        total = passed + failed
        success_rate = "%0.2f" % (passed * 100 / total)

        msg = template.render(summary_data=summary_data, tps_data=tps_data,
                              runner_user_hyper_link=runner_user_hyper_link,
                              hits_per_second_hyper_link=hits_per_second_hyper_link,
                              response_time_hyper_link=response_time_hyper_link,
                              tps_hyper_link=tps_hyper_link,
                              success_rate=str(success_rate),
                              not_java_script=True)

        # 保存数据用于后续上传

        self.summary_data.update(summary_data)
        tps_data['tps'].pop(0)
        self.summary_data.update(tps_data)
        self.summary_data['success_rate'] = str(success_rate)
        self.summary_data['script_type'] = 0
        self.summary_data['monitor_type'] = self.api_monitor_type

        return msg

    def generate_html_report(self):
        html_report = self.get_html_msg()
        f = open(self.report_file, "a+")
        try:
            f.write(html_report.encode('utf-8'))
        finally:
            f.close()

    def get_trs_graph_data(self):
        trs_xls = self.result_dir + "\\An_Report1\\Report4.xls"
        origin_data = get_data(trs_xls)
        origin_columns = origin_data
        self.summary_data['trs_graph_data'] = origin_columns['Sheet1']

    def get_tps_graph_data(self):
        tps_xls = self.result_dir + "\\An_Report1\\Report5.xls"
        origin_data = get_data(tps_xls)
        origin_columns = origin_data
        self.summary_data['tps_graph_data'] = origin_columns['Sheet1']

    def package_files(self):
        if not os.path.isdir(self.session_dir):
            print "[ERROR]" + self.session_dir + "No such a directory"
        zipfp = zipfile.ZipFile(self.package_file, 'w', zipfile.ZIP_DEFLATED)
        for dir_path, dir_names, file_names in os.walk(self.session_dir, True):
            for filename in file_names:
                directory = os.path.join(dir_path, filename)
                zipfp.write(directory)
        zipfp.close()
        pass

    def ftp_upload(self):
        ftp = FTP()
        ftp.set_debuglevel(0)
        ftp.connect(self.ftp_conf.get("ip"), '21')
        ftp.login(self.ftp_conf.get("user"), self.ftp_conf.get("password"))
        try:
            ftp.mkd(self.datafile_prefix.split("-")[0])
        except Exception, e:
            print ("[INFO]ftp directory: %s existed" %
                   self.datafile_prefix.split("-")[0])
            print e
        ftp.cwd(self.datafile_prefix.split("-")[0])
        try:
            ftp.mkd(self.datafile_prefix.split("-")[2])
        except Exception, e:
            print ("[INFO]ftp directory: %s existed" %
                   self.datafile_prefix.split("-")[2])
            print e
        ftp.cwd(self.datafile_prefix.split("-")[2])
        try:
            ftp.mkd(self.datafile_prefix.split("-")[1])
        except Exception, e:
            print ("[INFO]ftp directory: %s existed" %
                   self.datafile_prefix.split("-")[1])
            print e
        ftp.cwd(self.datafile_prefix.split("-")[1])
        try:
            ftp.mkd("lr_report")
        except Exception, e:
            print "[INFO]ftp directory: lr_report existed"
            print e
        ftp.cwd("lr_report")
        ftp.mkd(os.path.basename(self.report_file).split(".html")[0])
        ftp.cwd(os.path.basename(self.report_file).split(".html")[0])
        buffer_size = 1024

        file_handler = open(self.package_file, "rb")
        ftp.storbinary("STOR %s" % os.path.basename(self.package_file),
                       file_handler, buffer_size)
        file_handler = open(self.report_file, "rb")
        ftp.storbinary("STOR %s" % os.path.basename(self.report_file),
                       file_handler, buffer_size)
        file_handler = open(self.result_dir + "/" + "An_Report1.html", "rb")
        ftp.storbinary("STOR %s" % "An_Report1.html", file_handler, buffer_size)

        ftp.mkd("An_Report1")
        ftp.cwd("An_Report1")
        for report_file in util.get_dir_files(self.result_dir + "/" + "An_Report1"):
            file_handler = open(self.result_dir + "/" +
                                "An_Report1" + "/" + report_file, "rb")
            ftp.storbinary("STOR %s" % report_file, file_handler, buffer_size)
        ftp.set_debuglevel(0)
        file_handler.close()
        ftp.quit()

    def api_upload(self):
        r = requests.post(self.api_url, json=json.dumps(self.summary_data))
        if r.text == "200":
            print "[INFO]api upload success"
        else:
            print "[ERROR]api upload failed: " + r.text

    def work(self):
        self.get_conf()
        self.set_file_name()
        self.generate_html_report()
        if self.api_flag:
            self.get_tps_graph_data()
            self.get_trs_graph_data()
            self.api_upload()
        self.package_files()
        if self.ftp_conf.get('flag'):
            self.ftp_upload()


class LRJavaVuserReport(LRReport):

    def get_html_msg(self):
        runner_user_hyper_link = r"An_Report1/Report0.png"
        response_time_hyper_link = r"An_Report1/Report2.png"
        tps_hyper_link = r"An_Report1/Report3.png"

        summary_data = {}
        summary_file = self.result_dir + "\\An_Report1\\summary.html"
        if os.path.exists(summary_file):
            summary_parser = Parser.LRParser()
            f = open(summary_file, "r")
            try:
                for line in f.readlines():
                    summary_parser.feed(line)
                summary_data = summary_parser.work()
            finally:
                f.close()
        else:
            print "[ERROR]can not find summary.html in lr report directory"

        tps_data = {}
        tps_file = self.result_dir + "\\An_Report1\\Report3.html"
        if os.path.exists(tps_file):
            report5_parser = Parser.LRParser()
            f = open(tps_file, "r")
            try:
                for line in f.readlines():
                    report5_parser.feed(line)
                tps_data = report5_parser.work()
            finally:
                f.close()
        else:
            print "[ERROR]can not find Report3.html in lr report directory"

        passed = float(summary_data.get("total_passed"))
        failed = float(summary_data.get("total_failed"))
        total = passed + failed
        success_rate = "%0.2f" % (passed * 100 / total)

        msg = template.render(summary_data=summary_data, tps_data=tps_data,
                              runner_user_hyper_link=runner_user_hyper_link,
                              response_time_hyper_link=response_time_hyper_link,
                              tps_hyper_link=tps_hyper_link,
                              success_rate=str(success_rate),
                              not_java_script=False)

        # 保存数据用于后续上传

        self.summary_data.update(summary_data)
        tps_data['tps'].pop(0)
        self.summary_data.update(tps_data)
        self.summary_data['success_rate'] = str(success_rate)
        self.summary_data['script_type'] = 1
        self.summary_data['monitor_type'] = self.api_monitor_type

        return msg

    def get_trs_graph_data(self):
        trs_xls = self.result_dir + "\\An_Report1\\Report2.xls"
        origin_data = get_data(trs_xls)
        origin_columns = origin_data
        self.summary_data['trs_graph_data'] = origin_columns['Sheet1']

    def get_tps_graph_data(self):
        tps_xls = self.result_dir + "\\An_Report1\\Report3.xls"
        origin_data = get_data(tps_xls)
        origin_columns = origin_data
        self.summary_data['tps_graph_data'] = origin_columns['Sheet1']

