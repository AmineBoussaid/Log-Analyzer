CReate DataBase LogsBD

CREATE TABLE access_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(255),
    timestamp DATETIME,
    http_method VARCHAR(10),
    uri VARCHAR(255),
    http_protocol VARCHAR(10),
    response_code INT,
    response_size INT,
    referer TEXT,
    user_agent TEXT
);


CREATE TABLE error_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    severity VARCHAR(50),
    module VARCHAR(100),
    pid INT,
    message TEXT
);

CREATE TABLE secure_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  date datetime  NULL,
  hote VARCHAR(255)  NULL,
  sshd VARCHAR(255)  NULL,
  meg TEXT  NULL,
  user VARCHAR(255)  NULL,
  ip VARCHAR(255)  NULL,
  port int  NULL,
  ssh VARCHAR(255)  NULL
);

CREATE TABLE secure_auth (
  id INT AUTO_INCREMENT PRIMARY KEY,
  date datetime  NULL,
  hote VARCHAR(255)  NULL,
  sshd VARCHAR(255)  NULL,
  meg TEXT  NULL,
  logname VARCHAR(255)  NULL,
  uid int  NULL,
  euid int  NULL,
  tty VARCHAR(255)  NULL,
  ruser VARCHAR(255)  NULL,
  rhost VARCHAR(255)  NULL,
  user VARCHAR(255)  NULL
);
