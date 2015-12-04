# -*- coding:utf-8 -*-

report_html_header = """
<html>
<style type="text/css">
th{
    background: #a6caf0;
    align:center;
    vertical-align:middle;
}
td{
    background:#bfbfbf;
    font-weight:bold;
    color:green;
}
</style>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
</head>
<body>
<div align="center">
"""

report_summary_table = """
    <p><strong>LR统计数据汇总</strong></p>
    <table border="0" cellpadding="5" cellspacing="2"  width="60%%">
        <tr>
            <th>测试时间段</th>
            <td>%s</td>
        </tr>
        <tr>
            <th><a href="%s" target="_png">并发虚拟用户数</a></th>
            <td>%s</td>
        </tr>
        <tr>
            <th>总的吞吐量(字节)</th>
            <td>%s</td>
        </tr>
        <tr>
            <th>平均吞吐量(字节/秒)</th>
            <td>%s</td>
        </tr>
        <tr>
            <th>总的点击率</th>
            <td>%s</td>
        </tr>
        <tr>
            <th><a href="%s" target="_png">点击率/秒</a></th>
            <td>%s</td>
        </tr>
    </table>
"""

report_summary_java_table = """
    <p><strong>LR统计数据汇总</strong></p>
    <table border="0" cellpadding="5" cellspacing="2"  width="50%%">
        <tr>
            <th>测试时间段</th>
            <td>%s</td>
        </tr>
        <tr>
            <th><a href="%s">并发虚拟用户数</a></th>
            <td>%s</td>
        </tr>
    </table>
"""


report_trs_table_header = """
    <p style="text-align:center"><strong>Total Passed: %s     Total Failed: %s   Total Stopped: %s   成功率: %s%%</strong></p>
    <p><strong>事务响应时间汇总(Response Time)</strong></p>
    <table border="0" cellpadding="5" cellspacing="2"  width="60%%">
    <tr>
        <th>事务名称</th>
        <th>最小响应时间</th>
        <th>平均响应时间</th>
        <th>最大响应时间</th>
        <th>90%%响应时间</th>
        <th>通过事务数</th>
        <th>失败事务数</th>
        <th>停止事务数</th>
    </tr>
"""

report_trs_table_body = """
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>
"""

report_trs_image = """
    <tr>
        <td colspan="8"><div align="center"><img src="%s"></div></td>
    </tr>
    </table>
"""

report_tps_table_header = """
    <p><strong>每秒处理事务汇总(TPS)</strong></p>
    <table border="0" cellpadding="5" cellspacing="2"  width="60%%">
    <tr>
        <th>事务名称</th>
        <th>每秒处理事务平均数</th>
    </tr>
"""

report_tps_table_body = """
    <tr>
        <td>%s</td>
        <td>%s</td>
    </tr>
"""

report_tps_image = """
    <tr>
        <td colspan="2"><div align="center"><img src="%s" align="center"></div></td>
    </tr>
    </table>
"""

report_http_table_header = """
    <p><strong>HTTP响应汇总</strong></p>
    <table border="0" cellpadding="5" cellspacing="2"  width="60%%">
    <tr>
        <th>HTTP状态码</th>
        <th>总数量</th>
        <th>每秒响应数量</th>
    </tr>
"""

report_http_table_body = """
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>
"""

report_html_end = """
    </table>
    </div>
</body>
</html>
"""
