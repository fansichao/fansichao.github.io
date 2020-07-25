---
title: Linux-功能模块-证书配置
date: 2018-11-12 15:38:13
updated: 2018-11-12 19:17:11
tags:
  - 系统部署
  - Linux
  - Centos7
  - Centos8
  - HTTPS
categories:
  - Linux-功能模块
description: 证书配置
---

环境说明

- CentOS 8.1.1
- httpd 2.4.37
- 机器 IP: 192.168.172.73
- 主机名: fdm
- 说明事项
  - 文件修改前备份
  - 证书等位置 储存在 `/etc/httpd/extra/https_cert`

## 配置说明

### 证书配置

生成服务器证书, `root` 用户

```bash
# 创建目录
mkdir -p /etc/httpd/extra/https_cert/
cd /etc/httpd/extra/https_cert/

# 建立服务器密钥 必须2048以上，否则会提示 ee key too small，从而无法启动Apache
[root@fdm https_cert]# openssl genrsa -des3 2048  > /etc/httpd/extra/https_cert/server.key
Generating RSA private key, 2048 bit long modulus (2 primes)
.....................+++++
.+++++
e is 65537 (0x010001)
Enter pass phrase:
Verifying - Enter pass phrase:
# 从密钥中删除密码（以避免系统启动后被询问口令）
[root@fdm https_cert]# openssl rsa -in /etc/httpd/extra/https_cert/server.key > /etc/httpd/extra/https_cert/server2.key
Enter pass phrase for /usr/local/apache/conf/server.key:
writing RSA key
[root@fdm https_cert]# mv /etc/httpd/extra/https_cert/server2.key  /etc/httpd/extra/https_cert/server.key
mv: overwrite '/etc/httpd/extra/https_cert/server.key'? y
# 建立服务器密钥请求文件
[root@fdm https_cert]# openssl req -new -key /etc/httpd/extra/https_cert/server.key -out /etc/httpd/extra/https_cert/server.csr
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [XX]:
State or Province Name (full name) []:
Locality Name (eg, city) [Default City]:
Organization Name (eg, company) [Default Company Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (eg, your name or your server s hostname) []:fdm
Email Address []:

Please enter the following extra attributes
to be sent with your certificate request
A challenge password []:
An optional company name []:
# 建立服务器证书
[root@fdm conf]# openssl x509 -in /etc/httpd/extra/https_cert/server.csr -out  /etc/httpd/extra/https_cert/server.crt -req -signkey /etc/httpd/extra/https_cert/server.key -days 365
Signature ok
subject=C = XX, L = Default City, O = Default Company Ltd, CN = fdm
Getting Private key
[root@fdm https_cert]# pwd
/etc/httpd/extra/https_cert
[root@fdm https_cert]# ll
total 12
-rw-r--r-- 1 root root 1155 Jun 19 18:21 server.crt
-rw-r--r-- 1 root root  972 Jun 19 18:20 server.csr
-rw-r--r-- 1 root root 1679 Jun 19 18:20 server.key
# 项目用户 fdm 需要有证书的读写权限
chmod 777 -R /etc/httpd/extra/https_cert/server*
```

### Apache 配置

#### 安装依赖包

```bash
yum install httpd -y
yum install openssl openssl-devel httpd-devel -y
yum install mod_ssl -y
```

#### fdm.conf 配置

文件路径 `/etc/httpd/conf.d/fdm.conf`

```bash
# 配置原有 HTTP服务
User fdm
Group fdm
# HTTP
<VirtualHost *:80>
    DocumentRoot "/home/fdm/quick/web/fdm"
    <Directory "/home/fdm/quick/web/fdm">
        options Indexes MultiViews
        AllowOverride all
        Allow from all
    </Directory>
</VirtualHost>
```

#### ssl.conf 配置

文件路径 `/etc/httpd/conf.d/ssl.conf`

修改内容如下:

```conf
# 如果 ssl.conf 文件不存在，yum install mod_ssl -y

# 增加 LoadModule
LoadModule ssl_module modules/mod_ssl.so
# 修改 Listen 443
Listen 443 https
# 增加 指定证书路径
SSLCertificateFile /etc/httpd/extra/https_cert/server.crt
# 增加 指定Key路径
SSLCertificateKeyFile  /etc/httpd/extra/https_cert/server.key
# 增加 VirtualHost
<VirtualHost *:443>
    DocumentRoot "/home/fdm/quick/web/fdm"
    ServerName 192.168.172.73:443
    <Proxy *>
    Order deny,allow
    Allow from all
    </Proxy>
    SSLEngine On
    SSLProxyEngine On
    SSLProxyVerify none
    SSLProxyCheckPeerCN off
    SSLProxyCheckPeerName off
    SSLCertificateFile "/etc/httpd/extra/https_cert/server.crt"
    SSLCertificateKeyFile "/etc/httpd/extra/https_cert/server.key"

    ProxyRequests Off
    ProxyPreserveHost On
</VirtualHost>
```

文件内容如下:

```conf
#
# This is the Apache server configuration file providing SSL support.
# It contains the configuration directives to instruct the server how to
# serve pages over an https connection. For detailing information about these
# directives see <URL:http://httpd.apache.org/docs/2.2/mod/mod_ssl.html>
#
# Do NOT simply read the instructions in here without understanding
# what they do.  They're here only as hints or reminders.  If you are unsure
# consult the online docs. You have been warned.
#

LoadModule ssl_module modules/mod_ssl.so

# When we also provide SSL we have to listen to the
# the HTTPS port in addition.
#

Listen 443 https

# HTTP -> HTTPS
# <IfModule mod_rewrite.c>
#  RewriteEngine On
#  RewriteBase /
#  RewriteCond %{SERVER_PORT} 80
#  RewriteRule ^(.*)$ https://blog.mimvp.com/$1 [R=301,L]
# </IfModule>

# HTTPS -> HTTP
# <IfModule mod_rewrite.c>
#  RewriteEngine On
#  RewriteBase /
#  RewriteCond %{SERVER_PORT} 443
#  RewriteRule ^(.*)$ https://blog.mimvp.com/$1 [R=301,L]
# </IfModule>


##
##  SSL Global Context
##
##  All SSL configuration in this context applies both to
##  the main server and all SSL-enabled virtual hosts.
##

#   Pass Phrase Dialog:
#   Configure the pass phrase gathering process.
#   The filtering dialog program (`builtin' is a internal
#   terminal dialog) has to provide the pass phrase on stdout.
SSLPassPhraseDialog  builtin

#   Inter-Process Session Cache:
#   Configure the SSL Session Cache: First the mechanism
#   to use and second the expiring timeout (in seconds).
SSLSessionCache         shmcb:/var/cache/mod_ssl/scache(512000)
SSLSessionCacheTimeout  300

#   Semaphore:
#   Configure the path to the mutual exclusion semaphore the
#   SSL engine uses internally for inter-process synchronization.
# SSLMutex default
Mutex default

#   Pseudo Random Number Generator (PRNG):
#   Configure one or more sources to seed the PRNG of the
#   SSL library. The seed data should be of good random quality.
#   WARNING! On some platforms /dev/random blocks if not enough entropy
#   is available. This means you then cannot use the /dev/random device
#   because it would lead to very long connection times (as long as
#   it requires to make more entropy available). But usually those
#   platforms additionally provide a /dev/urandom device which doesn't
#   block. So, if available, use this one instead. Read the mod_ssl User
#   Manual for more details.
SSLRandomSeed startup file:/dev/urandom  256
SSLRandomSeed connect builtin
#SSLRandomSeed startup file:/dev/random  512
#SSLRandomSeed connect file:/dev/random  512
#SSLRandomSeed connect file:/dev/urandom 512

#
# Use "SSLCryptoDevice" to enable any supported hardware
# accelerators. Use "openssl engine -v" to list supported
# engine names.  NOTE: If you enable an accelerator and the
# server does not start, consult the error logs and ensure
# your accelerator is functioning properly.
#
SSLCryptoDevice builtin
#SSLCryptoDevice ubsec

##
## SSL Virtual Host Context
##

<VirtualHost _default_:443>

# General setup for the virtual host, inherited from global configuration
#DocumentRoot "/var/www/html"
#ServerName www.example.com:443

# Use separate log files for the SSL virtual host; note that LogLevel
# is not inherited from httpd.conf.
ErrorLog logs/ssl_error_log
TransferLog logs/ssl_access_log
LogLevel warn

#   SSL Engine Switch:
#   Enable/Disable SSL for this virtual host.
SSLEngine on

#   SSL Protocol support:
# List the enable protocol levels with which clients will be able to
# connect.  Disable SSLv2 access by default:
SSLProtocol all -SSLv2

#   SSL Cipher Suite:
# List the ciphers that the client is permitted to negotiate.
# See the mod_ssl documentation for a complete list.
SSLCipherSuite DEFAULT:!EXP:!SSLv2:!DES:!IDEA:!SEED:+3DES

#   Server Certificate:
# Point SSLCertificateFile at a PEM encoded certificate.  If
# the certificate is encrypted, then you will be prompted for a
# pass phrase.  Note that a kill -HUP will prompt again.  A new
# certificate can be generated using the genkey(1) command.
# SSLCertificateFile /etc/pki/tls/certs/localhost.crt
SSLCertificateFile /etc/httpd/extra/https_cert/server.crt

#   Server Private Key:
#   If the key is not combined with the certificate, use this
#   directive to point at the key file.  Keep in mind that if
#   you've both a RSA and a DSA private key you can configure
#   both in parallel (to also allow the use of DSA ciphers, etc.)
# SSLCertificateKeyFile /etc/pki/tls/private/localhost.key
SSLCertificateKeyFile  /etc/httpd/extra/https_cert/server.key

#   Server Certificate Chain:
#   Point SSLCertificateChainFile at a file containing the
#   concatenation of PEM encoded CA certificates which form the
#   certificate chain for the server certificate. Alternatively
#   the referenced file can be the same as SSLCertificateFile
#   when the CA certificates are directly appended to the server
#   certificate for convinience.
#SSLCertificateChainFile /etc/pki/tls/certs/server-chain.crt

#   Certificate Authority (CA):
#   Set the CA certificate verification path where to find CA
#   certificates for client authentication or alternatively one
#   huge file containing all of them (file must be PEM encoded)
#SSLCACertificateFile /etc/pki/tls/certs/ca-bundle.crt

#   Client Authentication (Type):
#   Client certificate verification type and depth.  Types are
#   none, optional, require and optional_no_ca.  Depth is a
#   number which specifies how deeply to verify the certificate
#   issuer chain before deciding the certificate is not valid.
#SSLVerifyClient require
#SSLVerifyDepth  10

#   Access Control:
#   With SSLRequire you can do per-directory access control based
#   on arbitrary complex boolean expressions containing server
#   variable checks and other lookup directives.  The syntax is a
#   mixture between C and Perl.  See the mod_ssl documentation
#   for more details.
#<Location />
#SSLRequire (    %{SSL_CIPHER} !~ m/^(EXP|NULL)/ \
#            and %{SSL_CLIENT_S_DN_O} eq "Snake Oil, Ltd." \
#            and %{SSL_CLIENT_S_DN_OU} in {"Staff", "CA", "Dev"} \
#            and %{TIME_WDAY} >= 1 and %{TIME_WDAY} <= 5 \
#            and %{TIME_HOUR} >= 8 and %{TIME_HOUR} <= 20       ) \
#           or %{REMOTE_ADDR} =~ m/^192\.76\.162\.[0-9]+$/
#</Location>

#   SSL Engine Options:
#   Set various options for the SSL engine.
#   o FakeBasicAuth:
#     Translate the client X.509 into a Basic Authorisation.  This means that
#     the standard Auth/DBMAuth methods can be used for access control.  The
#     user name is the `one line' version of the client's X.509 certificate.
#     Note that no password is obtained from the user. Every entry in the user
#     file needs this password: `xxj31ZMTZzkVA'.
#   o ExportCertData:
#     This exports two additional environment variables: SSL_CLIENT_CERT and
#     SSL_SERVER_CERT. These contain the PEM-encoded certificates of the
#     server (always existing) and the client (only existing when client
#     authentication is used). This can be used to import the certificates
#     into CGI scripts.
#   o StdEnvVars:
#     This exports the standard SSL/TLS related `SSL_*' environment variables.
#     Per default this exportation is switched off for performance reasons,
#     because the extraction step is an expensive operation and is usually
#     useless for serving static content. So one usually enables the
#     exportation for CGI and SSI requests only.
#   o StrictRequire:
#     This denies access when "SSLRequireSSL" or "SSLRequire" applied even
#     under a "Satisfy any" situation, i.e. when it applies access is denied
#     and no other module can change it.
#   o OptRenegotiate:
#     This enables optimized SSL connection renegotiation handling when SSL
#     directives are used in per-directory context.
#SSLOptions +FakeBasicAuth +ExportCertData +StrictRequire
<Files ~ "\.(cgi|shtml|phtml|php3?)$">
    SSLOptions +StdEnvVars
</Files>
<Directory "/var/www/cgi-bin">
    SSLOptions +StdEnvVars
</Directory>

#   SSL Protocol Adjustments:
#   The safe and default but still SSL/TLS standard compliant shutdown
#   approach is that mod_ssl sends the close notify alert but doesn't wait for
#   the close notify alert from client. When you need a different shutdown
#   approach you can use one of the following variables:
#   o ssl-unclean-shutdown:
#     This forces an unclean shutdown when the connection is closed, i.e. no
#     SSL close notify alert is send or allowed to received.  This violates
#     the SSL/TLS standard but is needed for some brain-dead browsers. Use
#     this when you receive I/O errors because of the standard approach where
#     mod_ssl sends the close notify alert.
#   o ssl-accurate-shutdown:
#     This forces an accurate shutdown when the connection is closed, i.e. a
#     SSL close notify alert is send and mod_ssl waits for the close notify
#     alert of the client. This is 100% SSL/TLS standard compliant, but in
#     practice often causes hanging connections with brain-dead browsers. Use
#     this only for browsers where you know that their SSL implementation
#     works correctly.
#   Notice: Most problems of broken clients are also related to the HTTP
#   keep-alive facility, so you usually additionally want to disable
#   keep-alive for those clients, too. Use variable "nokeepalive" for this.
#   Similarly, one has to force some clients to use HTTP/1.0 to workaround
#   their broken HTTP/1.1 implementation. Use variables "downgrade-1.0" and
#   "force-response-1.0" for this.
SetEnvIf User-Agent ".*MSIE.*" \
         nokeepalive ssl-unclean-shutdown \
         downgrade-1.0 force-response-1.0

#   Per-Server Logging:
#   The home of a custom SSL log file. Use this when you want a
#   compact non-error SSL logfile on a virtual host basis.
CustomLog logs/ssl_request_log \
          "%t %h %{SSL_PROTOCOL}x %{SSL_CIPHER}x \"%r\" %b"

</VirtualHost>

<VirtualHost *:443>
    DocumentRoot "/home/fdm/quick/web/fdm"
    ServerName 192.168.172.73:443
    <Proxy *>
    Order deny,allow
    Allow from all
    </Proxy>
    SSLEngine On
    SSLProxyEngine On
    SSLProxyVerify none
    SSLProxyCheckPeerCN off
    SSLProxyCheckPeerName off
    SSLCertificateFile "/etc/httpd/extra/https_cert/server.crt"
    SSLCertificateKeyFile "/etc/httpd/extra/https_cert/server.key"

    ProxyRequests Off
    ProxyPreserveHost On
</VirtualHost>
```

#### httpd.conf 配置

文件路径: `/etc/httpd/conf/httpd.conf`

文件无需修改

文件内容如下:

```conf
#
# This is the main Apache HTTP server configuration file.  It contains the
# configuration directives that give the server its instructions.
# See <URL:http://httpd.apache.org/docs/2.4/> for detailed information.
# In particular, see
# <URL:http://httpd.apache.org/docs/2.4/mod/directives.html>
# for a discussion of each configuration directive.
#
# See the httpd.conf(5) man page for more information on this configuration,
# and httpd.service(8) on using and configuring the httpd service.
#
# Do NOT simply read the instructions in here without understanding
# what they do.  They're here only as hints or reminders.  If you are unsure
# consult the online docs. You have been warned.
#
# Configuration and logfile names: If the filenames you specify for many
# of the server's control files begin with "/" (or "drive:/" for Win32), the
# server will use that explicit path.  If the filenames do *not* begin
# with "/", the value of ServerRoot is prepended -- so 'log/access_log'
# with ServerRoot set to '/www' will be interpreted by the
# server as '/www/log/access_log', where as '/log/access_log' will be
# interpreted as '/log/access_log'.

#
# ServerRoot: The top of the directory tree under which the server's
# configuration, error, and log files are kept.
#
# Do not add a slash at the end of the directory path.  If you point
# ServerRoot at a non-local disk, be sure to specify a local disk on the
# Mutex directive, if file-based mutexes are used.  If you wish to share the
# same ServerRoot for multiple httpd daemons, you will need to change at
# least PidFile.
#
ServerRoot "/etc/httpd"

#
# Listen: Allows you to bind Apache to specific IP addresses and/or
# ports, instead of the default. See also the <VirtualHost>
# directive.
#
# Change this to Listen on specific IP addresses as shown below to
# prevent Apache from glomming onto all bound IP addresses.
#
#Listen 12.34.56.78:80
Listen 80
Listen 8000
Listen 8001
Listen 8888

#
# Dynamic Shared Object (DSO) Support
#
# To be able to use the functionality of a module which was built as a DSO you
# have to place corresponding `LoadModule' lines at this location so the
# directives contained in it are actually available _before_ they are used.
# Statically compiled modules (those listed by `httpd -l') do not need
# to be loaded here.
#
# Example:
# LoadModule foo_module modules/mod_foo.so
#
Include conf.modules.d/*.conf



#
# If you wish httpd to run as a different user or group, you must run
# httpd as root initially and it will switch.
#
# User/Group: The name (or #number) of the user/group to run httpd as.
# It is usually good practice to create a dedicated user and group for
# running httpd, as with most system services.
#
User apache
Group apache

# 'Main' server configuration
#
# The directives in this section set up the values used by the 'main'
# server, which responds to any requests that aren't handled by a
# <VirtualHost> definition.  These values also provide defaults for
# any <VirtualHost> containers you may define later in the file.
#
# All of these directives may appear inside <VirtualHost> containers,
# in which case these default settings will be overridden for the
# virtual host being defined.
#

#
# ServerAdmin: Your address, where problems with the server should be
# e-mailed.  This address appears on some server-generated pages, such
# as error documents.  e.g. admin@your-domain.com
#
ServerAdmin root@localhost

#
# ServerName gives the name and port that the server uses to identify itself.
# This can often be determined automatically, but we recommend you specify
# it explicitly to prevent problems during startup.
#
# If your host doesn't have a registered DNS name, enter its IP address here.
#
#ServerName www.example.com:80
ServerName  localhost:80

#
# Deny access to the entirety of your server's filesystem. You must
# explicitly permit access to web content directories in other
# <Directory> blocks below.
#

# <Directory />
#     AllowOverride none
#     Require all denied
# </Directory>

#
# Note that from this point forward you must specifically allow
# particular features to be enabled - so if something's not working as
# you might expect, make sure that you have specifically enabled it
# below.
#

#
# DocumentRoot: The directory out of which you will serve your
# documents. By default, all requests are taken from this directory, but
# symbolic links and aliases may be used to point to other locations.
#
DocumentRoot "/var/www/html"

#
# Relax access to content within /var/www.
#
<Directory "/var/www">
    AllowOverride None
    # Allow open access:
    Require all granted
</Directory>

# Further relax access to the default document root:
<Directory "/var/www/html">
    #
    # Possible values for the Options directive are "None", "All",
    # or any combination of:
    #   Indexes Includes FollowSymLinks SymLinksifOwnerMatch ExecCGI MultiViews
    #
    # Note that "MultiViews" must be named *explicitly* --- "Options All"
    # doesn't give it to you.
    #
    # The Options directive is both complicated and important.  Please see
    # http://httpd.apache.org/docs/2.4/mod/core.html#options
    # for more information.
    #
    Options Indexes FollowSymLinks

    #
    # AllowOverride controls what directives may be placed in .htaccess files.
    # It can be "All", "None", or any combination of the keywords:
    #   Options FileInfo AuthConfig Limit
    #
    AllowOverride None

    #
    # Controls who can get stuff from this server.
    #
    Require all granted
</Directory>

#
# DirectoryIndex: sets the file that Apache will serve if a directory
# is requested.
#
<IfModule dir_module>
    DirectoryIndex index.html
</IfModule>

#
# The following lines prevent .htaccess and .htpasswd files from being
# viewed by Web clients.
#
<Files ".ht*">
    Require all denied
</Files>

#
# ErrorLog: The location of the error log file.
# If you do not specify an ErrorLog directive within a <VirtualHost>
# container, error messages relating to that virtual host will be
# logged here.  If you *do* define an error logfile for a <VirtualHost>
# container, that host's errors will be logged there and not here.
#
ErrorLog "logs/error_log"

#
# LogLevel: Control the number of messages logged to the error_log.
# Possible values include: debug, info, notice, warn, error, crit,
# alert, emerg.
#
LogLevel warn

<IfModule log_config_module>
    #
    # The following directives define some format nicknames for use with
    # a CustomLog directive (see below).
    #
    LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined
    LogFormat "%h %l %u %t \"%r\" %>s %b" common

    <IfModule logio_module>
      # You need to enable mod_logio.c to use %I and %O
      LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\" %I %O" combinedio
    </IfModule>

    #
    # The location and format of the access logfile (Common Logfile Format).
    # If you do not define any access logfiles within a <VirtualHost>
    # container, they will be logged here.  Contrariwise, if you *do*
    # define per-<VirtualHost> access logfiles, transactions will be
    # logged therein and *not* in this file.
    #
    #CustomLog "logs/access_log" common

    #
    # If you prefer a logfile with access, agent, and referer information
    # (Combined Logfile Format) you can use the following directive.
    #
    CustomLog "logs/access_log" combined
</IfModule>

<IfModule alias_module>
    #
    # Redirect: Allows you to tell clients about documents that used to
    # exist in your server's namespace, but do not anymore. The client
    # will make a new request for the document at its new location.
    # Example:
    # Redirect permanent /foo http://www.example.com/bar

    #
    # Alias: Maps web paths into filesystem paths and is used to
    # access content that does not live under the DocumentRoot.
    # Example:
    # Alias /webpath /full/filesystem/path
    #
    # If you include a trailing / on /webpath then the server will
    # require it to be present in the URL.  You will also likely
    # need to provide a <Directory> section to allow access to
    # the filesystem path.

    #
    # ScriptAlias: This controls which directories contain server scripts.
    # ScriptAliases are essentially the same as Aliases, except that
    # documents in the target directory are treated as applications and
    # run by the server when requested rather than as documents sent to the
    # client.  The same rules about trailing "/" apply to ScriptAlias
    # directives as to Alias.
    #
    ScriptAlias /cgi-bin/ "/var/www/cgi-bin/"

</IfModule>

#
# "/var/www/cgi-bin" should be changed to whatever your ScriptAliased
# CGI directory exists, if you have that configured.
#
<Directory "/var/www/cgi-bin">
    AllowOverride None
    Options None
    Require all granted
</Directory>

<IfModule mime_module>
    #
    # TypesConfig points to the file containing the list of mappings from
    # filename extension to MIME-type.
    #
    TypesConfig /etc/mime.types

    #
    # AddType allows you to add to or override the MIME configuration
    # file specified in TypesConfig for specific file types.
    #
    #AddType application/x-gzip .tgz
    #
    # AddEncoding allows you to have certain browsers uncompress
    # information on the fly. Note: Not all browsers support this.
    #
    #AddEncoding x-compress .Z
    #AddEncoding x-gzip .gz .tgz
    #
    # If the AddEncoding directives above are commented-out, then you
    # probably should define those extensions to indicate media types:
    #
    AddType application/x-compress .Z
    AddType application/x-gzip .gz .tgz

    #
    # AddHandler allows you to map certain file extensions to "handlers":
    # actions unrelated to filetype. These can be either built into the server
    # or added with the Action directive (see below)
    #
    # To use CGI scripts outside of ScriptAliased directories:
    # (You will also need to add "ExecCGI" to the "Options" directive.)
    #
    #AddHandler cgi-script .cgi

    # For type maps (negotiated resources):
    #AddHandler type-map var

    #
    # Filters allow you to process content before it is sent to the client.
    #
    # To parse .shtml files for server-side includes (SSI):
    # (You will also need to add "Includes" to the "Options" directive.)
    #
    AddType text/html .shtml
    AddOutputFilter INCLUDES .shtml
</IfModule>

#
# Specify a default charset for all content served; this enables
# interpretation of all content as UTF-8 by default.  To use the
# default browser choice (ISO-8859-1), or to allow the META tags
# in HTML content to override this choice, comment out this
# directive:
#
AddDefaultCharset UTF-8

<IfModule mime_magic_module>
    #
    # The mod_mime_magic module allows the server to use various hints from the
    # contents of the file itself to determine its type.  The MIMEMagicFile
    # directive tells the module where the hint definitions are located.
    #
    MIMEMagicFile conf/magic
</IfModule>

#
# Customizable error responses come in three flavors:
# 1) plain text 2) local redirects 3) external redirects
#
# Some examples:
#ErrorDocument 500 "The server made a boo boo."
#ErrorDocument 404 /missing.html
#ErrorDocument 404 "/cgi-bin/missing_handler.pl"
#ErrorDocument 402 http://www.example.com/subscription_info.html
#

#
# EnableMMAP and EnableSendfile: On systems that support it,
# memory-mapping or the sendfile syscall may be used to deliver
# files.  This usually improves server performance, but must
# be turned off when serving from networked-mounted
# filesystems or if support for these functions is otherwise
# broken on your system.
# Defaults if commented: EnableMMAP On, EnableSendfile Off
#
#EnableMMAP off
EnableSendfile on

# Supplemental configuration
#
# Load config files in the "/etc/httpd/conf.d" directory, if any.
IncludeOptional conf.d/*.conf
```

#### 服务配置

```bash
# 重启服务
/bin/systemctl restart httpd.service
# 查看服务状态
/bin/systemctl status  httpd.service
# 查看服务日志, exp: error.log
ll -srt /var/log/httpd/
```

### 项目配置

TODO gunicorn 模式存在 [SSLV3_ALERT_CERTIFICATE_UNKNOWN] sslv3 alert certificate unknown 问题

TODO JS-ip_config.js 存在修改处，如何通过 env 控制？ 或者统一控制。

```bash
# tools.py
def start_web():
    """开始Web后台服务, 试用Gunicorn作为服务器
    其参数配置请至setting/gun.conf进行配置
    """
    print("Start Web Server, Saving Log To Web.log..")
    if Config.REQUESTS_METHOD == 'HTTP':
        os.system("nohup gunicorn -c fdm/base/gun.conf fdm.views:app >> web.log &")
    elif Config.REQUESTS_METHOD == 'HTTPS':
        # 正常
        # gunicorn --certfile=/etc/httpd/extra/https_cert/server.crt  --keyfile=/etc/httpd/extra/https_cert/server.key --bind 0.0.0.0:3000 fdm.views:app
        # TODO 有问题
        os.system("nohup gunicorn -c fdm/base/gun.conf --certfile=%s --keyfile=%s fdm.views:app >> web.log &" % (Config.HTTPS_SERVER_CERT_PATH, Config.HTTPS_SERVER_KEY_PATH))
    print("Web Server Started.")
# tools.py
def run_app(ip):
    """单例后台服务器, 将输出日志信息
    主要用于开发与校验运行情况

    :param str ip: 服务启动IP地址
    """
    stop_web()
    if Config.REQUESTS_METHOD == 'HTTP':
        web_app.run(host=ip, port=web_app.config["PORT"], debug=True,
                    use_debugger=True, use_reloader=True)
    elif Config.REQUESTS_METHOD == 'HTTPS':
        ctx = (Config.HTTPS_SERVER_CERT_PATH, Config.HTTPS_SERVER_KEY_PATH)
        web_app.run(host=ip, port=web_app.config["PORT"], debug=True,
                    use_debugger=True, use_reloader=True, ssl_context=ctx)


# /home/fdm/.fdm_profile
export REQUESTS_METHOD=HTTPS
export HTTPS_SERVER_CERT_PATH=/etc/httpd/extra/https_cert/server.crt
export HTTPS_SERVER_KEY_PATH=/etc/httpd/extra/https_cert/server.key


# fdm/base/settings.py
"""
    是否启用 HTTPS
"""
REQUESTS_METHOD = os.environ.get("REQUESTS_METHOD", "HTTP").upper()
REQUESTS_METHODS = ['HTTPS', 'HTTP']
REQUESTS_METHOD = REQUESTS_METHOD if REQUESTS_METHOD in REQUESTS_METHODS else 'HTTP'

# 证书路径 需授权至此用户可以访问
HTTPS_SERVER_CERT_PATH = os.environ.get("HTTPS_SERVER_CERT_PATH", "/etc/httpd/extra/https_cert/server.crt")
HTTPS_SERVER_KEY_PATH = os.environ.get("HTTPS_SERVER_KEY_PATH", "/etc/httpd/extra/https_cert/server.key")
if not os.path.exists(HTTPS_SERVER_CERT_PATH) or not os.path.exists(HTTPS_SERVER_KEY_PATH):
    logging.warning('> 存在HTTPS相关文件[%s]-[%s]缺失, 自动切换到 HTTP模式', HTTPS_SERVER_CERT_PATH, HTTPS_SERVER_KEY_PATH)
    HTTPS_SERVER_CERT_PATH = 'HTTP'


# fdm/js/ip_config.js
var idv_url = ["http://", ip, ":", port].join("");
var idv_url = ["https://", ip, ":", port].join("");
```

项目登录界面:

- [http://192.168.172.73](http://192.168.172.73)
- [https://192.168.172.73](https://192.168.172.73)

## 附件

### 其他配置

```bash
# Flask-HTTPS 加载ssl证书
app.run('0.0.0.0', debug=True, port=11000, ssl_context=('path/xxxx.pem', 'path/xxxx.key'))
# Flask-HTTPS 在后台服务中加入
response.headers.add("Content-Security-Policy", "upgrade-insecure-requests")
# HTML-HTTPS 在需要的页面中加入
<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests">

```

### 参考资源

- [Apache 使用 ssl 模块配置 HTTPS](https://blog.csdn.net/ithomer/article/details/50433363)
- [配置 HTTPS 证书后，浏览器出现不安全提示的解决方法](https://blog.csdn.net/AllisWell_Wotrus/article/details/93058704)
- [服务器已部署 SSL 开启 https 协议为什么浏览器仍然提示不安全？](https://blog.csdn.net/weixin_43731793/article/details/93197332)
- [使用 openssl 生成 https 证书](https://baijiahao.baidu.com/s?id=1649462735958571118&wfr=spider&for=pc)

[https 网页加载 http 资源导致的页面报错及解决方案](https://blog.csdn.net/xiasohuai/article/details/83349385)
[HTTPS 常见部署问题及解决方案](https://imququ.com/post/troubleshooting-https.html)

[记一次从 HTTP 升级 HTTPS 完全指南](https://juejin.im/post/5d57cc0de51d453b1d6482d1)

[什么是混合内容](https://developers.google.com/web/fundamentals/security/prevent-mixed-content/what-is-mixed-content?hl=zh-cn#_11)
[在服务器上启用 HTTPS](https://developers.google.com/web/fundamentals/security/encrypt-in-transit/enable-https?hl=zh-cn)

无法从 HTTPS 访问 http api，由于浏览器同源策略，这是不可实现的。必须要将 api 修改为支持 https 方式
[Calling http api from https website [duplicate]](https://stackoverflow.com/questions/46735446/calling-http-api-from-https-website)

### 问题记录

#### [SSLV3_ALERT_CERTIFICATE_UNKNOWN] sslv3 alert certificate unknown

```bash
# reboot_server 命令报错
gunicorn -c fdm/base/gun.conf --certfile=%s --keyfile=%s fdm.views:app

# 此命令不报错
gunicorn --certfile=/etc/httpd/extra/https_cert/server.crt  --keyfile=/etc/httpd/extra/https_cert/server.key --bind 0.0.0.0:3000 fdm.views:app

# 日志详情
[2020-06-19 21:12:28 +0800] [4780] [DEBUG] Invalid request from ip=192.168.172.2: [SSL: SSLV3_ALERT_CERTIFICATE_UNKNOWN] sslv3 alert certificate unknown (_ssl.c:2607)
[2020-06-19 21:12:28 +0800] [4780] [DEBUG] Failed to send error message.
```

#### code 400, message Bad request syntax

- 问题原因
  - 由于 Flask 没有 ssl 证书，所以无法访问 https 站点
- 解决方案
  - 购买 ssl 证书，参考链接: [在 Flask 中配置 ssl 证书，将 http 升级为 https](https://blog.csdn.net/qq_41427568/article/details/101025193)

日志详情

```bash
# 场景
登录时报错

# 前台服务 试图访问HTTPS后台报错
GET https://192.168.172.73:3000/LoginToken/Login?code=%E5%88%86%E6%9E%90%E5%91%98&password=e10adc3949ba59abbe56e057f20f883e net::ERR_SSL_PROTOCOL_ERROR

# 后台服务报错
[2020-06-19 12:01:26,652] PID:22944-werkzeug: [_internal.py-_log-122] ERROR  : 192.168.172.2 - - [19/Jun/2020 12:01:26] code 400, message Bad request syntax ('\x16\x03\x01\x02\x00\x01\x00\x01ü\x03\x03Æ¼ãßV\x9eN.')
[2020-06-19 12:01:26,654] PID:22944-werkzeug: [_internal.py-_log-122] INFO   : 192.168.172.2 - - [19/Jun/2020 12:01:26] "üÆ¼ãßVN." HTTPStatus.BAD_REQUEST -
```
