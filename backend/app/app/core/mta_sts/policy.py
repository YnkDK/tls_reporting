from typing import Optional, List

from app.core.mta_sts.failure_detail import FailureDetail


class Policy:
    def __init__(self):
        self.policy_type = ''
        self.policy_string = None  # type: Optional[str]
        self.policy_domain = ''
        self.mx_host = None  # type: Optional[str]
        self.total_successful_session_count = 0
        self.total_failure_session_count = 0
        self.failure_details = []  # type: List[FailureDetail]

    def build(self, raw_policy: dict):
        meta = raw_policy['policy']
        summary = raw_policy['summary']

        self.policy_type = meta['policy-type']
        self.policy_string = meta.get('policy-string', None)
        self.policy_domain = meta['policy-domain']
        self.mx_host = meta.get('mx-host', None)
        self.total_successful_session_count = summary['total-successful-session-count']
        self.total_failure_session_count = summary['total-failure-session-count']
        for detail in raw_policy.get('failure-details', []):
            failure_detail = FailureDetail()
            failure_detail.build(detail)
            self.failure_details.append(failure_detail)
