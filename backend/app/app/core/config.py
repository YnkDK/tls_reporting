from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    SERVER_NAME: str

    APPLICATION_NAME: str = "TLS Reporting"
    APPLICATION_DESCRIPTION: str = """A number of protocols exist for establishing encrypted channels between SMTP
Mail Transfer Agents (MTAs), including STARTTLS, DNS-Based Authentication of Named Entities (DANE) TLSA, and MTA
Strict Transport Security (MTA-STS).  These protocols can fail due to misconfiguration or active attack, leading to
undelivered messages or delivery over unencrypted or unauthenticated channels.

The STARTTLS extension to SMTP [RFC3207] allows SMTP clients and hosts to establish secure SMTP sessions over TLS.
The protocol design uses an approach that has come to be known as "Opportunistic Security" (OS) [RFC7435]. This
method maintains interoperability with clients that do not support STARTTLS, but it means that any attacker could
potentially eavesdrop on a session.  An attacker could perform a downgrade or interception attack by deleting parts
of the SMTP session (such as the "250 STARTTLS" response) or redirect the entire SMTP session (perhaps by
overwriting the resolved MX record of the delivery domain).

Because such "downgrade attacks" are not necessarily apparent to the receiving MTA, this document defines a
mechanism for sending domains to report on failures at multiple stages of the MTA-to-MTA conversation.

Recipient domains may also use the mechanisms defined by MTA-STS [RFC8461] or DANE [RFC6698] to publish additional
encryption and authentication requirements; this document defines a mechanism for sending domains that are
compatible with MTA-STS or DANE to share success and failure statistics with recipient domains.

Specifically, this document defines a reporting schema that covers failures in routing, DNS resolution, and STARTTLS
negotiation; policy validation errors for both DANE [RFC6698] and MTA-STS [RFC8461]; and a standard TXT record that
recipient domains can use to indicate where reports in this format should be sent.  The report can also serve as a
heartbeat to indicate that systems are successfully negotiating TLS during sessions as expected.

Text from https://datatracker.ietf.org/doc/html/rfc8460
"""

    # POSTGRES_SERVER: str
    # POSTGRES_USER: str
    # POSTGRES_PASSWORD: str
    # POSTGRES_DB: str
    # SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
    #
    # @classmethod
    # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    # def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
    #     if isinstance(v, str):
    #         return v
    #     return PostgresDsn.build(
    #         scheme="postgresql",
    #         user=values.get("POSTGRES_USER"),
    #         password=values.get("POSTGRES_PASSWORD"),
    #         host=values.get("POSTGRES_SERVER"),
    #         path=f"/{values.get('POSTGRES_DB') or ''}",
    #     )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
