from sgmllib import SGMLParser


class LRParser(SGMLParser):

    def reset(self):
        self.data_dictionary = {}
        self.header_timerange_flag = False
        self.duration_flag = False
        self.maximum_running_vuser_flag = False
        self.total_throughput_flag = False
        self.average_throughput_flag = False
        self.total_hits_flag = False
        self.average_hits_flag = False

        self.transaction_summary_flag = False
        self.transaction_summary_count = 0
        self.transaction_total_passed_flag = False
        self.transaction_total_failed_flag = False
        self.transaction_total_stopped_flag = False

        self.trs_name_flag = False
        self.trs_name_count = 0
        self.trs_minumum_flag = False
        self.trs_average_flag = False
        self.trs_maximum_flag = False
        self.trs_90percent_flag = False
        self.trs_pass_flag = False
        self.trs_fail_flag = False
        self.trs_stop_flag = False

        self.http_responses_flag = False
        self.http_responses_count = 0
        self.http_total_flag = False
        self.http_persecond_flag = False

        self.tps_flag = False
        self.tps_count = 0

        SGMLParser.reset(self)
        pass

    def start_td(self, attrs):
        for key, value in attrs:
            if key == "class" and value == "header_timerange":
                self.header_timerange_flag = True
                return
            if key == "headers" and value == "LraDuration":
                self.duration_flag = True
                return
            if key == "headers" and value == "LraMaximumRunningVusers":
                self.maximum_running_vuser_flag = True
                return
            if key == "headers" and value == "LraTotalThroughput":
                self.total_throughput_flag = True
                return
            if key == "headers" and value == "LraAverageThroughput":
                self.average_throughput_flag = True
                return
            if key == "headers" and value == "LraTotalHits":
                self.total_hits_flag = True
                return
            if key == "headers" and value == "LraAverageHitsPerSecond":
                self.average_hits_flag = True
                return
            if self.transaction_summary_flag:
                if (key == "class" and value == "VerBl8" and
                            self.transaction_summary_count == 0):
                    self.transaction_total_passed_flag = True
                    self.transaction_summary_count += 1
                    return
                if (key == "class" and value == "VerBl8" and
                            self.transaction_summary_count == 1):
                    self.transaction_total_failed_flag = True
                    self.transaction_summary_count += 1
                    return
                if (key == "class" and value == "VerBl8" and
                            self.transaction_summary_count == 2):
                    self.transaction_total_stopped_flag = True
                    self.transaction_summary_count += 1
                    return
            if key == "headers" and value == "LraTransaction Name":
                self.data_dictionary.setdefault("trs", [])
                self.trs_name_count += 1
                self.trs_name_flag = True
                self.data_dictionary.get("trs").append([])
                return
            if key == "headers" and value == "LraMinimum":
                self.trs_minumum_flag = True
                return
            if key == "headers" and value == "LraAverage":
                self.trs_average_flag = True
                return
            if key == "headers" and value == "LraMaximum":
                self.trs_maximum_flag = True
                return
            if key == "headers" and value == "Lra90 Percent":
                self.trs_90percent_flag = True
                return
            if key == "headers" and value == "LraPass":
                self.trs_pass_flag = True
                return
            if key == "headers" and value == "LraFail":
                self.trs_fail_flag = True
                return
            if key == "headers" and value == "LraStop":
                self.trs_stop_flag = True
                return
            if key == "headers" and value =="LraHTTP Responses":
                self.data_dictionary.setdefault("http", [])
                self.http_responses_count += 1
                self.http_responses_flag = True
                self.data_dictionary.get("http").append([])
                return
            if key == "headers" and value =="LraTotal":
                self.http_total_flag = True
                return
            if key == "headers" and value =="LraPer second":
                self.http_persecond_flag = True
                return

    def end_td(self):
        if self.header_timerange_flag:
            self.header_timerange_flag = False
        if self.duration_flag:
            self.duration_flag = False
        if self.maximum_running_vuser_flag:
            self.maximum_running_vuser_flag = False
        if self.total_throughput_flag:
            self.total_throughput_flag = False
        if self.average_throughput_flag:
            self.average_throughput_flag = False
        if self.total_hits_flag:
            self.total_hits_flag = False
        if self.average_hits_flag:
            self.average_throughput_flag = False
        if self.transaction_total_passed_flag:
            self.transaction_total_passed_flag = False
        if self.transaction_total_failed_flag:
            self.transaction_total_failed_flag = False
        if self.transaction_total_stopped_flag:
            self.transaction_total_stopped_flag = False
        if self.trs_name_flag:
            self.trs_name_flag = False
        if self.trs_minumum_flag:
            self.trs_minumum_flag = False
        if self.trs_average_flag:
            self.trs_average_flag = False
        if self.trs_maximum_flag:
            self.trs_maximum_flag = False
        if self.trs_90percent_flag:
            self.trs_90percent_flag = False
        if self.trs_pass_flag:
            self.trs_pass_flag = False
        if self.trs_fail_flag:
            self.trs_fail_flag = False
        if self.trs_stop_flag:
            self.trs_stop_flag = False
        if self.http_responses_flag:
            self.http_responses_flag = False
        if self.http_total_flag:
            self.http_total_flag = False
        if self.http_persecond_flag:
            self.http_persecond_flag = False

    def start_table(self, attrs):
        for key, value in attrs:
            if key == "summary" and value == "Transaction end state table":
                self.transaction_summary_flag = True
                self.transaction_summary_count = 0
                return
            if key == "border" and value == "1":
                self.data_dictionary.setdefault("tps", [])
                self.tps_flag = True

    def end_table(self):
        if self.transaction_summary_flag:
            self.transaction_summary_flag = False
            self.transaction_summary_count = 0
        if self.tps_flag:
            self.tps_flag = False

    def start_tr(self, attrs):
        if self.tps_flag:
            self.tps_count += 1
            self.data_dictionary.get("tps").append([])

    def end_tr(self):
        pass

    def handle_data(self, data):
        if data.strip() != "":
            if self.header_timerange_flag:
                self.data_dictionary.setdefault("header_timerange", data)
            if self.duration_flag:
                self.data_dictionary.setdefault("duration", data)
            if self.maximum_running_vuser_flag:
                self.data_dictionary.setdefault("maximum_runner_vuser", data)
            if self.total_throughput_flag:
                self.data_dictionary.setdefault("total_throughput", data)
            if self.average_throughput_flag:
                self.data_dictionary.setdefault("average_throughput", data)
            if self.total_hits_flag:
                self.data_dictionary.setdefault("total_hits", data)
            if self.average_hits_flag:
                self.data_dictionary.setdefault("average_hits", data)
            if self.transaction_total_passed_flag:
                self.data_dictionary.setdefault("total_passed", data)
            if self.transaction_total_failed_flag:
                self.data_dictionary.setdefault("total_failed", data)
            if self.transaction_total_stopped_flag:
                self.data_dictionary.setdefault("total_stopped", data)
            if self.trs_name_flag:
                self.data_dictionary.get("trs")[self.trs_name_count-1].append(data)
            if self.trs_minumum_flag:
                self.data_dictionary.get("trs")[self.trs_name_count-1].append(data)
            if self.trs_average_flag:
                self.data_dictionary.get("trs")[self.trs_name_count-1].append(data)
            if self.trs_maximum_flag:
                self.data_dictionary.get("trs")[self.trs_name_count-1].append(data)
            if self.trs_90percent_flag:
                self.data_dictionary.get("trs")[self.trs_name_count-1].append(data)
            if self.trs_pass_flag:
                self.data_dictionary.get("trs")[self.trs_name_count-1].append(data)
            if self.trs_fail_flag:
                self.data_dictionary.get("trs")[self.trs_name_count-1].append(data)
            if self.trs_stop_flag:
                self.data_dictionary.get("trs")[self.trs_name_count-1].append(data)
            if self.http_responses_flag:
                self.data_dictionary.get("http")[self.http_responses_count-1].append(data)
            if self.http_total_flag:
                self.data_dictionary.get("http")[self.http_responses_count-1].append(data)
            if self.http_persecond_flag:
                self.data_dictionary.get("http")[self.http_responses_count-1].append(data)
            if self.tps_flag:
                self.data_dictionary.get("tps")[self.tps_count-1].append(data.split("\r\n")[0])

    def work(self):
        return self.data_dictionary