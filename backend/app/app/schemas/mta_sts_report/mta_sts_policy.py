from enum import Enum
from typing import List

from pydantic import AnyUrl, BaseModel, Field, IPvAnyAddress


class PolicyTypes(Enum):
    TLSA = "tlsa"
    STS = "sts"
    NO_POLICY_FOUND = "no-policy-found"


class Policy(BaseModel):
    policy_type: PolicyTypes = Field(
        ...,
        description="The type of policy that was applied by the sending domain. Presently, the only three valid "
        'choices are "tlsa", "sts", and the literal string "no-policy-found".',
        alias="policy-type",
        example=PolicyTypes.STS,
    )
    policy_string: List[str] = Field(
        ...,
        description="An encoding of the applied policy as a JSON array of strings, whether it's a TLSA record "
        "([RFC6698], Section 2.3) or an MTA-STS Policy.",
        alias="policy-string",
        example=[
            "version: STSv1",
            "mode: testing",
            "mx: *.mail.company-y.example",
            "max_age: 86400",
        ],
    )
    policy_domain: str = Field(
        ...,
        description="The Policy Domain against which the MTA-STS or DANE policy is defined. In the case of "
        "Internationalized Domain Names [RFC5891], the domain MUST consist of the Punycode-encoded A-labels"
        " [RFC3492] and not the U-labels.",
        alias="policy-domain",
        example="company-y.example",
        max_length=255,
    )
    mx_host: str = Field(
        None,
        description='In the case where "policy-type" is "sts", it\'s the pattern of MX hostnames from the applied'
        " policy.",
        alias="mx-host",
        example="*.mail.company-y.example",
        max_length=450,
    )


class Summary(BaseModel):
    total_successful_session_count: int = Field(
        ...,
        description="The aggregate count of successfully negotiated TLS-enabled connections to the receiving site.",
        alias="total-successful-session-count",
        ge=0,
        example=5326,
    )
    total_failure_session_count: int = Field(
        ...,
        description="The aggregate count of failures to negotiate a TLS-enabled connection to the receiving site.",
        alias="total-failure-session-count",
        ge=0,
        example=303,
    )


class FailureDetail(BaseModel):
    result_type: str = Field(..., description="The result type.", alias="result-type")
    sending_mta_ip: IPvAnyAddress = Field(
        ...,
        description="The IP address of the Sending MTA that attempted the STARTTLS connection. It is provided as a "
        "string representation of an IPv4 (see below) or IPv6 [RFC5952] address in dot-decimal or "
        "colon-hexadecimal notation.",
        alias="sending-mta-ip",
    )
    receiving_mx_hostname: str = Field(
        None,
        description="The hostname of the receiving MTA MX record with which the Sending MTA attempted to negotiate a "
        "STARTTLS connection",
        alias="receiving-mx-hostname",
    )
    receiving_mx_helo: str = Field(
        None,
        description="The HELLO (HELO) or Extended HELLO (EHLO) string from the banner announced during the reported "
        "session.",
        alias="receiving-mx-helo",
    )
    receiving_ip: IPvAnyAddress = Field(
        None,
        description="The destination IP address that was used when creating the outbound session.  It is provided as a "
        "string representation of an IPv4 (see below) or IPv6 [RFC5952] address in dot-decimal or "
        "colon-hexadecimal notation.",
        alias="receiving-ip",
    )
    failed_session_count: int = Field(
        ...,
        description='The number of (attempted) sessions that match the relevant "result-type" for this section.',
        alias="failed-session-count",
        ge=1,
    )
    additional_information: AnyUrl = Field(
        None,
        description='A URI [RFC3986] that points to additional information around the relevant "result-type". For '
        "example, this URI might host the complete certificate chain presented during an attempted "
        "STARTTLS session",
        alias="additional-information",
    )
    failure_reason_code: str = Field(
        None,
        description="A text field to include a TLS-related error code or error message.",
        alias="failure-reason-code",
    )


class PolicyContainer(BaseModel):
    policy: Policy = Field(..., description="The policy.")
    summary: Summary = Field(
        ..., description="Aggregate counts of successful and failure sessions."
    )
    failure_details: List[FailureDetail] = Field(
        [],
        alias="failure-details",
        example=[
            {
                "result-type": "certificate-expired",
                "sending-mta-ip": "2001:db8:abcd:0012::1",
                "receiving-mx-hostname": "mx1.mail.company-y.example",
                "failed-session-count": 100,
            },
            {
                "result-type": "starttls-not-supported",
                "sending-mta-ip": "2001:db8:abcd:0013::1",
                "receiving-mx-hostname": "mx2.mail.company-y.example",
                "receiving-ip": "203.0.113.56",
                "failed-session-count": 200,
                "additional-information": "https://reports.company-x.example/report_info?id=5065427c-23d3#StarttlsNotSupported",
            },
            {
                "result-type": "validation-failure",
                "sending-mta-ip": "198.51.100.62",
                "receiving-ip": "203.0.113.58",
                "receiving-mx-hostname": "mx-backup.mail.company-y.example",
                "failed-session-count": 3,
                "failure-error-code": "X509_V_ERR_PROXY_PATH_LENGTH_EXCEEDED",
            },
        ],
    )
