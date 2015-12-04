# -*- coding:utf-8 -*-
import os
import copy
import zipfile
import ConfigParser
from ftplib import FTP
import util
import Parser

from template import report_html_header
from template import report_summary_table
from template import report_trs_table_header
from template import report_trs_table_body
from template import report_trs_image
from template import report_tps_table_header
from template import report_tps_table_body
from template import report_tps_image
from template import report_http_table_header
from template import report_http_table_body
from template import report_html_end

class LRReport():

    build_id = ""
    datafile_prefix = ""
    result_dir = ""
    session_dir = ""
    report_file = ""
    pdf_file = ""
    package_file = ""
    config_file = ""
    ftp_conf = {}

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
        get the email configuration from ini file
        """
        config = ConfigParser.ConfigParser()
        with open(self.config_file, "r") as cfg_file:
            config.readfp(cfg_file)
        self.ftp_conf.setdefault("ip", config.get("ftp", "ip"))
        self.ftp_conf.setdefault("user", config.get("ftp", "user"))
        self.ftp_conf.setdefault("password", config.get("ftp", "password"))

    def set_file_name(self):
        time_stamp = self.build_id
        self.report_file = (self.result_dir + "\\"
                            + self.datafile_prefix +
                            "_lr_statistical_data_" + time_stamp + ".html")
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

        statistics_msg = report_summary_table % (
                summary_data.get("header_timerange").split("Period:")[1],
                runner_user_hyper_link, 
                summary_data.get("maximum_runner_vuser"),
                summary_data.get("total_throughput"),
                summary_data.get("average_throughput"),
                summary_data.get("total_hits"),
                hits_per_second_hyper_link,
                summary_data.get("average_hits"))

        success_rate = "%0.2f" % \
                       (float(summary_data.get("total_passed").replace(",", "").split(":")[1]) *
                        100 /
                        (float(summary_data.get("total_passed").replace(",", "").split(":")[1])
                         + float(summary_data.get("total_failed").replace(",", "").split(":")[1])))

        transaction_trs_msg = report_trs_table_header % (
                summary_data.get("total_passed").split(":")[1],
                summary_data.get("total_failed").split(":")[1],
                summary_data.get("total_stopped").split(":")[1],
                str(success_rate))

        for i in xrange(len(summary_data.get("trs"))):
            transaction_trs_sub_msg = report_trs_table_body % (summary_data.get("trs")[i][0],
                   summary_data.get("trs")[i][1],
                   summary_data.get("trs")[i][2],
                   summary_data.get("trs")[i][3],
                   summary_data.get("trs")[i][4],
                   summary_data.get("trs")[i][5],
                   summary_data.get("trs")[i][6],
                   summary_data.get("trs")[i][7])
            transaction_trs_msg += transaction_trs_sub_msg
        transaction_trs_msg += report_trs_image  % response_time_hyper_link

        transaction_tps_msg = report_tps_table_header
        for i in xrange(len(tps_data.get("tps"))-1):
            transaction_tps_sub_msg = report_tps_table_body  % (
                    tps_data.get("tps")[i+1][1], tps_data.get("tps")[i+1][3])
            transaction_tps_msg += transaction_tps_sub_msg
        transaction_tps_msg += report_tps_image % tps_hyper_link
        http_reponse_msg = report_http_table_header
        for i in xrange(len(summary_data.get("http"))):
            http_reponse_sub_msg = report_http_table_body % (
                    summary_data.get("http")[i][0],
                    summary_data.get("http")[i][1],
                    summary_data.get("http")[i][2])
            http_reponse_msg += http_reponse_sub_msg
        msg = (report_html_header + statistics_msg + transaction_trs_msg + transaction_tps_msg +
               http_reponse_msg + report_html_end)
        return msg

    def generate_html_report(self):
        html_report = self.get_html_msg()
        f = open(self.report_file, "a+")
        try:
            f.write(html_report)
        finally:
            f.close()

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

    def work(self):
        self.get_conf()
        self.set_file_name()
        self.generate_html_report()
        self.package_files()
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

        statistics_msg = report_summary_java_table % (
                summary_data.get("header_timerange").split("Period:")[1],
                runner_user_hyper_link,
                summary_data.get("maximum_runner_vuser"))

        success_rate = "%0.2f" % \
                       (float(summary_data.get("total_passed").replace(",", "").split(":")[1]) *
                        100 /
                        (float(summary_data.get("total_passed").replace(",", "").split(":")[1])
                         + float(summary_data.get("total_failed").replace(",", "").split(":")[1])))
        transaction_trs_msg = report_trs_table_header % (
                summary_data.get("total_passed").split(":")[1],
                summary_data.get("total_failed").split(":")[1],
                summary_data.get("total_stopped").split(":")[1],
                str(success_rate))

        for i in xrange(len(summary_data.get("trs"))):
            transaction_trs_sub_msg = report_trs_table_body % (
                    summary_data.get("trs")[i][0],
                    summary_data.get("trs")[i][1],
                    summary_data.get("trs")[i][2],
                    summary_data.get("trs")[i][3],
                    summary_data.get("trs")[i][4],
                    summary_data.get("trs")[i][5],
                    summary_data.get("trs")[i][6],
                    summary_data.get("trs")[i][7])
            transaction_trs_msg += transaction_trs_sub_msg
        transaction_trs_msg += report_trs_image % response_time_hyper_link

        transaction_tps_msg = report_tps_table_header

        for i in xrange(len(tps_data.get("tps"))-1):
            transaction_tps_sub_msg = report_tps_table_body % (
                    tps_data.get("tps")[i+1][1],
                    tps_data.get("tps")[i+1][3])
            transaction_tps_msg += transaction_tps_sub_msg
        transaction_tps_msg += report_tps_image  % tps_hyper_link

        msg = (report_html_header + statistics_msg + transaction_trs_msg + transaction_tps_msg + report_html_end)
        return msg

