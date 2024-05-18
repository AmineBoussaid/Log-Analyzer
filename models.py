from dataclasses import dataclass
import datetime

@dataclass
class AccessLog:
    ip: str
    timestamp: str
    http_method: str
    uri: str
    http_protocol: str
    response_code: int
    response_size: int
    referer: str
    user_agent: str

@dataclass
class ErrorLog:
    timestamp: str
    module: str
    severity: str
    pid: int
    message: str


@dataclass
class SecureLog:
    date: datetime
    hote: str
    sshd: str
    msg: str
    user: str
    ip: str
    port: int
    ssh: str
@dataclass
class SecureAuth:
    date: datetime
    hote: str
    sshd: str
    msg: str
    logname: str
    uid: int
    euid: int
    tty: str
    ruser: str
    rhost: str
    user: str