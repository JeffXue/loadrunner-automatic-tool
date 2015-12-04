import os
import sys
import util
import report


def main():
    parameter_lists = util.get_parameter_lists(sys.argv)
	
    if len(parameter_lists) == 3:
        result_dit = parameter_lists[0]
        prefix = parameter_lists[1]
        build_id = parameter_lists[2]
        vuser_type = 0
    elif len(parameter_lists) == 4:
        result_dit = parameter_lists[0]
        prefix = parameter_lists[1]
        build_id = parameter_lists[2]
        vuser_type = parameter_lists[3]
    else:
        print "[ERROR]parameter number error"
        print "[ERROR]start.py result_dir prefix build_id [vuser_type]"
        return

    if int(vuser_type) == 0:
        lr_sum_report = report.LRReport(result_dit, prefix, build_id)
    else:
        lr_sum_report = report.LRJavaVuserReport(result_dit, prefix, build_id)

    lr_sum_report.work()


if __name__ == "__main__":
    main()
