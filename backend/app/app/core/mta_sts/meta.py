import datetime


class Meta:
    def __init__(self, report_name: str):
        self.report_name = report_name
        self.organization_name = ''
        self.start = datetime.datetime.min
        self.end = datetime.datetime.min
        self.contact_info = ''
        self.report_id = ''

    def build(self, raw_report):
        date_ranges = raw_report['date-range']

        self.organization_name = raw_report['organization-name']
        self.start = datetime.datetime.strptime(date_ranges['start-datetime'], "%Y-%m-%dT%H:%M:%SZ")
        self.end = datetime.datetime.strptime(date_ranges['end-datetime'], "%Y-%m-%dT%H:%M:%SZ")
        self.contact_info = raw_report['contact-info']
        self.report_id = raw_report['report-id']
