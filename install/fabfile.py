# -*- coding:utf-8 -*-
from fabric.api import *

env.passwords = {
    'root@10.66.94.239:22': '32985200Xsh',
}

env.roledefs = {
    'front': ['root@10.66.94.239:22',],
    'backend': ['root@10.66.94.239:22',],
    'mysql': ['root@10.66.94.239:22',],
    'mongodb': ['root@10.66.94.239:22',]
}

installDicts = {
    'common': {
        'localPackagePath': '/home/download/initenv',
        'remotePackagePath': '/home/download',
        'gitUserName': 'jiangwei',
        'gitUserEmail': 'jiangwei07061625@163.com'
    },
    'front': {
        'envProfile': [
            '',
            'export LUAJIT_LIB=/usr/local/luajit/lib',
            'export LUAJIT_INC=/usr/local/luajit/include/luajit-2.0',
            "export CPPFLAGS='-I/usr/local/libjpeg/include -I/usr/local/freetype/include'",
            "export LDFLAGS='-L/usr/local/libjpeg/lib -L/usr/local/freetype/lib'",
            'export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/lib',
            'export JAVA_HOME=/usr/java/jdk1.8.0',
            'export CLASSPATH=.:\$JAVA_HOME/jre/lib/rt.jar:\$JAVA_HOME/lib/dt.jar:\$JAVA_HOME/lib/tools.jar',
            'export PATH=\$PATH:/usr/local/git/bin:/usr/local/bin:\$JAVA_HOME/bin:\$JAVA_HOME/jre/bin',
        ]
    },
    'backend': {
        'envProfile': [
            '',
            'export LUAJIT_LIB=/usr/local/luajit/lib',
            'export LUAJIT_INC=/usr/local/luajit/include/luajit-2.0',
            "export CPPFLAGS='-I/usr/local/libjpeg/include -I/usr/local/freetype/include'",
            "export LDFLAGS='-L/usr/local/libjpeg/lib -L/usr/local/freetype/lib'",
            'export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/lib',
            'export ETCDCTL_API=3',
            'export PATH=\$PATH:/usr/local/git/bin:/usr/local/bin',
        ]
    },
    'mysql': {
        'envProfile': [
            '',
            'export PATH=\$PATH:/usr/local/git/bin',
        ]
    },
    'mongodb': {
        'envProfile': [
            '',
            'ulimit -f unlimited',
            'ulimit -t unlimited',
            'ulimit -v unlimited',
            'ulimit -n 64000',
            'ulimit -m unlimited',
            'ulimit -u 64000',
            'export PATH=\$PATH:/usr/local/git/bin',
        ]
    }
}

# 初始化系统环境配置
def __initSystemEnv(envList):
    for eEnv in iter(envList):
        run('echo "%s" >> /etc/profile' % eEnv, False)
    run('source /etc/profile')

# 配置基础环境
def __installBase():
    run('yum -y install vim zip nss gcc gcc-c++ net-tools wget htop lsof unzip bzip2 curl-devel zlib-devel epel-release perl-ExtUtils-MakeMaker expat-devel gettext-devel openssl-devel iproute.x86_64 autoconf')
    run('wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo')
    run('mkdir %s' % installDicts['common']['remotePackagePath'])
    run('mkdir /home/configs')
    run('mkdir /home/logs')
    run('systemctl enable firewalld')
    run('systemctl start firewalld')
    run('systemctl enable crond')
    run('systemctl start crond')
    run('mkdir /usr/local/git')
    run('yum -y remove git')

    gitLocal = ''.join([installDicts['common']['localPackagePath'], '/linux/git-2.10.2.tar.gz'])
    gitRemote = ''.join([installDicts['common']['remotePackagePath'], '/git-2.10.2.tar.gz'])
    put(gitLocal, gitRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -xzf git-2.10.2.tar.gz')
        run('cd git-2.10.2 && make prefix=/usr/local/git all && make prefix=/usr/local/git install && cd ../ && rm -rf git-2.10.2 && rm -rf git-2.10.2.tar.gz')
        run('git config --global user.name "%s"' % installDicts['common']['gitUserName'])
        run('git config --global user.email "%s"' % installDicts['common']['gitUserEmail'])
    run('yum -y update')

# 配置nginx环境
def __installNginx():
    run('mkdir /home/logs/nginx')
    run('mkdir /home/configs/nginx')
    run('mkdir /home/configs/nginx/certs')
    run('mkdir /home/configs/nginx/modules')
    run('mkdir /home/configs/nginx/servers')
    pcreLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/pcre-8.39.tar.gz'])
    pcreRemote = ''.join([installDicts['common']['remotePackagePath'], '/pcre-8.39.tar.gz'])
    put(pcreLocal, pcreRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/pcre')
        run('tar -zxvf pcre-8.39.tar.gz')
        run('cd pcre-8.39/ && ./configure --prefix=/usr/local/pcre && make && make install')
        run('rm -rf pcre-8.39/')

    zlibLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/zlib-1.2.11.tar.gz'])
    zlibRemote = ''.join([installDicts['common']['remotePackagePath'], '/zlib-1.2.11.tar.gz'])
    put(zlibLocal, zlibRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/zlib')
        run('tar -zxvf zlib-1.2.11.tar.gz')
        run('cd zlib-1.2.11/ && ./configure --prefix=/usr/local/zlib && make && make install')
        run('rm -rf zlib-1.2.11/')

    opensslLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/openssl-1.0.2m.tar.gz'])
    opensslRemote = ''.join([installDicts['common']['remotePackagePath'], '/openssl-1.0.2m.tar.gz'])
    put(opensslLocal, opensslRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/openssl')
        run('tar -zxvf openssl-1.0.2m.tar.gz')
        run('cd openssl-1.0.2m/ && ./config --prefix=/usr/local/openssl shared zlib && make && make install')
        run('rm -rf openssl-1.0.2m/')
        run('mv /usr/bin/openssl /usr/bin/openssl.old')
        run('mv /usr/include/openssl /usr/include/openssl.old')
        run('ln -s /usr/local/openssl/bin/openssl /usr/bin/openssl')
        run('ln -s /usr/local/openssl/include/openssl /usr/include/openssl')
        run('echo "/usr/local/openssl/lib" >> /etc/ld.so.conf')

    libunwindLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/libunwind-1.1.tar.gz'])
    libunwindRemote = ''.join([installDicts['common']['remotePackagePath'], '/libunwind-1.1.tar.gz'])
    put(libunwindLocal, libunwindRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf libunwind-1.1.tar.gz')
        run('cd libunwind-1.1/ && CFLAGS=-fPIC ./configure --prefix=/usr && make CFLAGS=-fPIC && make CFLAGS=-fPIC install')
        run('rm -rf libunwind-1.1/')
        run('rm -rf libunwind-1.1.tar.gz')

    gperftoolsLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/gperftools-2.1.tar.gz'])
    gperftoolsRemote = ''.join([installDicts['common']['remotePackagePath'], '/gperftools-2.1.tar.gz'])
    put(gperftoolsLocal, gperftoolsRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf gperftools-2.1.tar.gz')
        run('cd gperftools-2.1/ && ./configure --prefix=/usr --enable-frame-pointers && make && make install')
        run('rm -rf gperftools-2.1/')
        run('rm -rf gperftools-2.1.tar.gz')
        run('echo "/usr/local/lib" > /etc/ld.so.conf.d/usr_local_lib.conf')
        run('/sbin/ldconfig')
        run('mkdir /tmp/tcmalloc')
        run('chmod 0777 /tmp/tcmalloc')

    luajitLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/LuaJIT-2.0.5.tar.gz'])
    luajitRemote = ''.join([installDicts['common']['remotePackagePath'], '/LuaJIT-2.0.5.tar.gz'])
    put(luajitLocal, luajitRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/luajit')
        run('tar -zxvf LuaJIT-2.0.5.tar.gz')
        run('cd LuaJIT-2.0.5/ && make && make install PREFIX=/usr/local/luajit')
        run('rm -rf LuaJIT-2.0.5/')
        run('rm -rf LuaJIT-2.0.5.tar.gz')

    ngxdevelLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/ngx_devel_kit-0.2.19.tar.gz'])
    ngxdevelRemote = ''.join([installDicts['common']['remotePackagePath'], '/ngx_devel_kit-0.2.19.tar.gz'])
    put(ngxdevelLocal, ngxdevelRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf ngx_devel_kit-0.2.19.tar.gz')
        run('mv ngx_devel_kit-0.2.19/ /home/configs/nginx/modules/ngx_devel_kit')
        run('rm -rf ngx_devel_kit-0.2.19.tar.gz')

    ngxluaLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/lua-nginx-module-0.10.11.tar.gz'])
    ngxluaRemote = ''.join([installDicts['common']['remotePackagePath'], '/lua-nginx-module-0.10.11.tar.gz'])
    put(ngxluaLocal, ngxluaRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf lua-nginx-module-0.10.11.tar.gz')
        run('mv lua-nginx-module-0.10.11/ /home/configs/nginx/modules/lua-nginx-module')
        run('rm -rf lua-nginx-module-0.10.11.tar.gz')

    ngxwafLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/ngx_lua_waf.tar.gz'])
    ngxwafRemote = ''.join([installDicts['common']['remotePackagePath'], '/ngx_lua_waf.tar.gz'])
    put(ngxwafLocal, ngxwafRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf ngx_lua_waf.tar.gz')
        run('mv ngx_lua_waf/ /home/configs/nginx/waf')
        run('rm -rf ngx_lua_waf.tar.gz')

    nginxLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/nginx-1.12.1.tar.gz'])
    nginxRemote = ''.join([installDicts['common']['remotePackagePath'], '/nginx-1.12.1.tar.gz'])
    put(nginxLocal, nginxRemote)
    with cd(installDicts['common']['remotePackagePath']):
        pcreDirRemote = ''.join([installDicts['common']['remotePackagePath'], '/pcre-8.39'])
        zlibDirRemote = ''.join([installDicts['common']['remotePackagePath'], '/zlib-1.2.11'])
        opensslDirRemote = ''.join([installDicts['common']['remotePackagePath'], '/openssl-1.0.2m'])
        run('mkdir /usr/local/nginx')
        run('tar -zxvf nginx-1.12.1.tar.gz')
        run('tar -zxvf pcre-8.39.tar.gz')
        run('tar -zxvf zlib-1.2.11.tar.gz')
        run('tar -zxvf openssl-1.0.2m.tar.gz')
        run('cd nginx-1.12.1/ && ./configure --prefix=/usr/local/nginx --with-pcre=%s --with-zlib=%s --with-openssl=%s --without-http_autoindex_module --without-http_ssi_module --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_gzip_static_module --with-http_v2_module --with-stream --with-stream_ssl_module --with-google_perftools_module --add-module=/home/configs/nginx/modules/ngx_devel_kit --add-module=/home/configs/nginx/modules/lua-nginx-module --with-ld-opt="-Wl,-rpath,$LUAJIT_LIB" && make -j 4 && make install' % (pcreDirRemote, zlibDirRemote, opensslDirRemote))
        run('rm -rf nginx-1.12.1/')
        run('rm -rf nginx-1.12.1.tar.gz')
        run('rm -rf pcre-8.39/')
        run('rm -rf pcre-8.39.tar.gz')
        run('rm -rf zlib-1.2.11/')
        run('rm -rf zlib-1.2.11.tar.gz')
        run('rm -rf openssl-1.0.2m/')
        run('rm -rf openssl-1.0.2m.tar.gz')

    nginxConfLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/nginx.conf'])
    nginxConfRemote = '/usr/local/nginx/conf/nginx.conf'
    run('rm -rf %s' % nginxConfRemote)
    put(nginxConfLocal, nginxConfRemote)

    nginxServiceLocal = ''.join([installDicts['common']['localPackagePath'], '/nginx/nginx.service'])
    nginxServiceRemote = '/lib/systemd/system/nginx.service'
    put(nginxServiceLocal, nginxServiceRemote)
    run('chmod 754 %s' % nginxServiceRemote)
    run('systemctl enable nginx')

# 配置PHP7环境
def __installPhp7():
    run('yum -y install gdb php-mcrypt libmcrypt libmcrypt-devel libxslt libxml2 libxml2-devel openssl openssl-devel curl-devel libcurl-devel libpng.x86_64 freetype.x86_64 libjpeg-turbo.x86_64 libjpeg-turbo-devel.x86_64 libjpeg-turbo-utils.x86_64 libpng-devel.x86_64 freetype-devel.x86_64 libjpeg-turbo-devel libmcrypt-devel mysql-devel openldap openldap-devel libtool-ltdl-devel.x86_64 gmp-devel')

    jpegLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/jpegsrc.v9.tar.gz'])
    jpegRemote = ''.join([installDicts['common']['remotePackagePath'], '/jpegsrc.v9.tar.gz'])
    put(jpegLocal, jpegRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/libjpeg')
        run('tar -zxvf jpegsrc.v9.tar.gz')
        run('cd jpeg-9/ && ./configure --prefix=/usr/local/libjpeg --enable-shared --enable-static && make && make install')
        run('ldconfig /usr/local/libjpeg/lib')
        run('rm -rf jpeg-9/')
        run('rm -rf jpegsrc.v9.tar.gz')

    freetypeLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/freetype-2.6.5.tar.bz2'])
    freetypeRemote = ''.join([installDicts['common']['remotePackagePath'], '/freetype-2.6.5.tar.bz2'])
    put(freetypeLocal, freetypeRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/freetype')
        run('tar -xjf freetype-2.6.5.tar.bz2')
        run('cd freetype-2.6.5/ && ./configure --prefix=/usr/local/freetype --enable-shared --enable-static && make && make install')
        run('ldconfig /usr/local/freetype/lib')
        run('rm -rf freetype-2.6.5/')
        run('rm -rf freetype-2.6.5.tar.bz2')

    php7Local = ''.join([installDicts['common']['localPackagePath'], '/php7/php-7.1.14.tar.gz'])
    php7Remote = ''.join([installDicts['common']['remotePackagePath'], '/php-7.1.14.tar.gz'])
    put(php7Local, php7Remote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /tmp/swoolyaf')
        run('mkdir /home/configs/yaconf-cli')
        run('mkdir /home/configs/yaconf-fpm')
        run('mkdir /home/logs/seaslog-cli')
        run('mkdir /home/logs/seaslog-fpm')
        run('mkdir /usr/local/mysql')
        run('mkdir /usr/local/php7')
        run('tar -zxvf php-7.1.14.tar.gz')
        run('cd php-7.1.14/ && ./configure --prefix=/usr/local/php7 --exec-prefix=/usr/local/php7 --bindir=/usr/local/php7/bin --sbindir=/usr/local/php7/sbin --includedir=/usr/local/php7/include --libdir=/usr/local/php7/lib/php --mandir=/usr/local/php7/php/man --with-config-file-path=/usr/local/php7/etc --with-mysql-sock=/usr/local/mysql/mysql.sock --with-zlib=/usr/local/zlib --with-mhash --with-openssl --with-mysqli=shared,mysqlnd --with-pdo-mysql=shared,mysqlnd --with-iconv --enable-zip --enable-inline-optimization --disable-debug --disable-rpath --enable-shared --enable-xml --enable-pcntl --enable-bcmath --enable-mysqlnd --enable-sysvsem --with-mysqli --enable-embedded-mysqli  --with-pdo-mysql --enable-shmop --enable-mbregex --enable-mbstring --enable-ftp --enable-sockets --with-xmlrpc --enable-soap --without-pear --with-gettext --enable-session --with-curl --enable-opcache --enable-fpm --without-gdbm --enable-fileinfo --with-gmp && make && make install')

    php7CliIniLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/php-cli.ini'])
    php7CliIniRemote = '/usr/local/php7/etc/php-cli.ini'
    put(php7CliIniLocal, php7CliIniRemote)
    php7FpmIniLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/php-fpm-fcgi.ini'])
    php7FpmIniRemote = '/usr/local/php7/etc/php-fpm-fcgi.ini'
    put(php7FpmIniLocal, php7FpmIniRemote)
    php7FpmConfLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/www.conf'])
    php7FpmConfRemote = '/usr/local/php7/etc/php-fpm.d/www.conf'
    put(php7FpmConfLocal, php7FpmConfRemote)
    php7FpmServiceLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/php7-fpm.service'])
    php7FpmServiceRemote = '/lib/systemd/system/php7-fpm.service'
    put(php7FpmServiceLocal, php7FpmServiceRemote)
    run('chmod 754 /lib/systemd/system/php7-fpm.service')
    run('systemctl enable php7-fpm.service')

    php7DirRemote = ''.join([installDicts['common']['remotePackagePath'], '/php-7.1.14'])
    with cd(php7DirRemote):
        run('groupadd www')
        run('useradd -g www www -s /sbin/nologin')
        run('cp sapi/fpm/init.d.php-fpm /etc/init.d/php7-fpm')
        run('chmod +x /etc/init.d/php7-fpm')
        run('cp /usr/local/php7/etc/php-fpm.conf.default /usr/local/php7/etc/php-fpm.conf')
        run('cp -frp /usr/lib64/libldap* /usr/lib/')
        run('cd ext/ldap/ && /usr/local/php7/bin/phpize && ./configure --with-php-config=/usr/local/php7/bin/php-config && make && make install')
        run('cd ext/gd/ && /usr/local/php7/bin/phpize && ./configure --with-php-config=/usr/local/php7/bin/php-config --with-freetype-dir=/usr/local/freetype --with-jpeg-dir=/usr/local/libjpeg --with-zlib-dir=/usr/local/zlib --enable-gd-jis-conv --enable-gd-native-ttf && make && make install')

    # 扩展redis
    extRedisLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/redis-3.1.6.tgz'])
    extRedisRemote = ''.join([installDicts['common']['remotePackagePath'], '/redis-3.1.6.tgz'])
    put(extRedisLocal, extRedisRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/phpredis')
        run('tar -zxvf redis-3.1.6.tgz')
        run('cd redis-3.1.6/ && /usr/local/php7/bin/phpize && ./configure --prefix=/usr/local/phpredis --with-php-config=/usr/local/php7/bin/php-config && make && make install')
        run('rm -rf redis-3.1.6/')
        run('rm -rf redis-3.1.6.tgz')

    # 扩展imgick
    extImageMagickLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/ImageMagick-7.0.6-7.tar.gz'])
    extImageMagickRemote = ''.join([installDicts['common']['remotePackagePath'], '/ImageMagick-7.0.6-7.tar.gz'])
    put(extImageMagickLocal, extImageMagickRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/imagemagick')
        run('tar -zxvf ImageMagick-7.0.6-7.tar.gz')
        run('cd ImageMagick-7.0.6-7/ && ./configure --prefix=/usr/local/imagemagick --enable-shared --enable-lzw --without-perl --with-modules && make && make install')
        run('rm -rf ImageMagick-7.0.6-7/')
        run('rm -rf ImageMagick-7.0.6-7.tar.gz')
    extImagickLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/imagick-3.4.3.tgz'])
    extImagickRemote = ''.join([installDicts['common']['remotePackagePath'], '/imagick-3.4.3.tgz'])
    put(extImagickLocal, extImagickRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/imagick')
        run('tar -zxvf imagick-3.4.3.tgz')
        run('cd imagick-3.4.3/ && /usr/local/php7/bin/phpize && ./configure --prefix=/usr/local/imagick --with-php-config=/usr/local/php7/bin/php-config --with-imagick=/usr/local/imagemagick && make && make install')
        run('rm -rf imagick-3.4.3/')
        run('rm -rf imagick-3.4.3.tgz')

    # 扩展SeasLog
    extSeasLogLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/SeasLog-1.7.6.tgz'])
    extSeasLogRemote = ''.join([installDicts['common']['remotePackagePath'], '/SeasLog-1.7.6.tgz'])
    put(extSeasLogLocal, extSeasLogRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf SeasLog-1.7.6.tgz')
        run('cd SeasLog-1.7.6/ && /usr/local/php7/bin/phpize && ./configure --with-php-config=/usr/local/php7/bin/php-config && make && make install')
        run('rm -rf SeasLog-1.7.6/')
        run('rm -rf SeasLog-1.7.6.tgz')

    # 扩展mongodb
    extMongodbLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/mongodb-1.3.4.tgz'])
    extMongodbRemote = ''.join([installDicts['common']['remotePackagePath'], '/mongodb-1.3.4.tgz'])
    put(extMongodbLocal, extMongodbRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf mongodb-1.3.4.tgz')
        run('cd mongodb-1.3.4/ && /usr/local/php7/bin/phpize && ./configure --with-php-config=/usr/local/php7/bin/php-config && make && make install')
        run('rm -rf mongodb-1.3.4/')
        run('rm -rf mongodb-1.3.4.tgz')

    # 扩展msgpack
    extMsgpackLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/msgpack-2.0.2.tgz'])
    extMsgpackRemote = ''.join([installDicts['common']['remotePackagePath'], '/msgpack-2.0.2.tgz'])
    put(extMsgpackLocal, extMsgpackRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf msgpack-2.0.2.tgz')
        run('cd msgpack-2.0.2/ && /usr/local/php7/bin/phpize && ./configure --with-php-config=/usr/local/php7/bin/php-config && make && make install')
        run('rm -rf msgpack-2.0.2/')
        run('rm -rf msgpack-2.0.2.tgz')

    # 扩展yac
    extYacLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/yac-2.0.2.tgz'])
    extYacRemote = ''.join([installDicts['common']['remotePackagePath'], '/yac-2.0.2.tgz'])
    put(extYacLocal, extYacRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf yac-2.0.2.tgz')
        run('cd yac-2.0.2/ && /usr/local/php7/bin/phpize && ./configure --with-php-config=/usr/local/php7/bin/php-config && make && make install')
        run('rm -rf yac-2.0.2/')
        run('rm -rf yac-2.0.2.tgz')

    # 扩展yaconf
    extYaconfLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/yaconf-1.0.7.tgz'])
    extYaconfRemote = ''.join([installDicts['common']['remotePackagePath'], '/yaconf-1.0.7.tgz'])
    put(extYaconfLocal, extYaconfRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf yaconf-1.0.7.tgz')
        run('cd yaconf-1.0.7/ && /usr/local/php7/bin/phpize && ./configure --with-php-config=/usr/local/php7/bin/php-config && make && make install')
        run('rm -rf yaconf-1.0.7/')
        run('rm -rf yaconf-1.0.7.tgz')

    # 扩展yaf
    extYafLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/yaf-3.0.6.tgz'])
    extYafRemote = ''.join([installDicts['common']['remotePackagePath'], '/yaf-3.0.6.tgz'])
    put(extYafLocal, extYafRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf yaf-3.0.6.tgz')
        run('cd yaf-3.0.6/ && /usr/local/php7/bin/phpize && ./configure --with-php-config=/usr/local/php7/bin/php-config && make && make install')
        run('rm -rf yaf-3.0.6/')
        run('rm -rf yaf-3.0.6.tgz')

    # 扩展swoole-1.10.1.tgz
    extSwooleJemallocLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/jemalloc-4.5.0.tar.bz2'])
    extSwooleJemallocRemote = ''.join([installDicts['common']['remotePackagePath'], '/jemalloc-4.5.0.tar.bz2'])
    put(extSwooleJemallocLocal, extSwooleJemallocRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/jemalloc')
        run('tar -xjvf jemalloc-4.5.0.tar.bz2')
        run('cd jemalloc-4.5.0/ && ./configure --prefix=/usr/local/jemalloc --with-jemalloc-prefix=je_ && make -j 4 && make install')
        run('rm -rf jemalloc-4.5.0/')
        run('rm -rf jemalloc-4.5.0.tar.bz2')
    extSwooleHttp2Local = ''.join([installDicts['common']['localPackagePath'], '/php7/nghttp2-1.26.0.tar.bz2'])
    extSwooleHttp2Remote = ''.join([installDicts['common']['remotePackagePath'], '/nghttp2-1.26.0.tar.bz2'])
    put(extSwooleHttp2Local, extSwooleHttp2Remote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -xf nghttp2-1.26.0.tar.bz2')
        run('mv nghttp2-1.26.0/ /usr/local/nghttp2')
        run('cd /usr/local/nghttp2 && ./configure && make libdir=/usr/lib64 && make libdir=/usr/lib64 install')
        run('rm -rf nghttp2-1.26.0.tar.bz2')
    extSwooleLocal = ''.join([installDicts['common']['localPackagePath'], '/php7/swoole-1.10.1.tgz'])
    extSwooleRemote = ''.join([installDicts['common']['remotePackagePath'], '/swoole-1.10.1.tgz'])
    put(extSwooleLocal, extSwooleRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf swoole-1.10.1.tgz')
        run('cd swoole-1.10.1/ && /usr/local/php7/bin/phpize && ./configure --with-php-config=/usr/local/php7/bin/php-config --with-jemalloc-dir=/usr/local/jemalloc --enable-openssl --enable-http2 && make && make install')
        run('rm -rf swoole-1.10.1/')
        run('rm -rf swoole-1.10.1.tgz')

# 配置java环境
def __installJava():
    jdkLocal = ''.join([installDicts['common']['localPackagePath'], '/java/jdk-8u131-linux-x64.tar.gz'])
    jdkRemote = ''.join([installDicts['common']['remotePackagePath'], '/jdk-8u131-linux-x64.tar.gz'])
    put(jdkLocal, jdkRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/java')
        run('tar -zxvf jdk-8u131-linux-x64.tar.gz')
        run('mv jdk1.8.0_131/ /usr/java/jdk1.8.0')
        run('rm -rf jdk-8u131-linux-x64.tar.gz')

# 配置inotify环境
def __installInotify():
    inotifyLocal = ''.join([installDicts['common']['localPackagePath'], '/linux/inotify-tools-3.14.tar.gz'])
    inotifyRemote = ''.join([installDicts['common']['remotePackagePath'], '/inotify-tools-3.14.tar.gz'])
    put(inotifyLocal, inotifyRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/inotify')
        run('tar -zxvf inotify-tools-3.14.tar.gz')
        run('cd inotify-tools-3.14/ && ./configure --prefix=/usr/local/inotify && make && make install')
        run('rm -rf inotify-tools-3.14.tar.gz')
        run('mkdir /usr/local/inotify/symodules')
        run('touch /usr/local/inotify/symodules/change_service.txt')

# 配置etcd环境
def __installEtcd():
    etcdLocal = ''.join([installDicts['common']['localPackagePath'], '/linux/etcd-v3.2.7-linux-amd64.tar.gz'])
    etcdRemote = ''.join([installDicts['common']['remotePackagePath'], '/etcd-v3.2.7-linux-amd64.tar.gz'])
    put(etcdLocal, etcdRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf etcd-v3.2.7-linux-amd64.tar.gz')
        run('mv etcd-v3.2.7-linux-amd64/ /usr/local/etcd')
        run('cp /usr/local/etcd/etcd* /usr/local/bin')
        run('rm -rf etcd-v3.2.7-linux-amd64.tar.gz')

# 配置redis环境
def __installRedis():
    redisLocal = ''.join([installDicts['common']['localPackagePath'], '/redis/redis-3.2.11.tar.gz'])
    redisRemote = ''.join([installDicts['common']['remotePackagePath'], '/redis-3.2.11.tar.gz'])
    put(redisLocal, redisRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('mkdir /usr/local/redis')
        run('mkdir /etc/redis')
        run('tar -zxvf redis-3.2.11.tar.gz')
        run('mv redis-3.2.11/ /usr/local/redis/')
        run('cd /usr/local/redis/redis-3.2.11 && make && cd src/ && make install')
        redisServiceLocal = ''.join([installDicts['common']['localPackagePath'], '/redis/redis'])
        redisServiceRemote = '/etc/init.d/redis'
        put(redisServiceLocal, redisServiceRemote)
        run('chmod +x %s' % redisServiceRemote)
        redisConfLocal = ''.join([installDicts['common']['localPackagePath'], '/redis/6379.conf'])
        redisConfRemote = '/etc/redis/6379.conf'
        put(redisConfLocal, redisConfRemote)
        run('rm -rf redis-3.2.11.tar.gz')
        run('systemctl daemon-reload')
        run('chkconfig redis on')

@roles('front')
def installFront():
    __initSystemEnv(installDicts['front']['envProfile'])
    __installBase()
    run('firewall-cmd --zone=public --add-port=21/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=22/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=80/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=8983/tcp --permanent')
    run('firewall-cmd --reload')
    __installNginx()
    __installPhp7()
    __installJava()

@roles('backend')
def installBackend():
    __initSystemEnv(installDicts['backend']['envProfile'])
    __installBase()
    run('firewall-cmd --zone=public --add-port=21/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=22/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=80/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=2379/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=6379/tcp --permanent')
    run('firewall-cmd --reload')
    __installNginx()
    __installPhp7()
    __installRedis()
    __installInotify()
    __installEtcd()

# 配置mysql环境
# 配置之前先用命令rpm -qa | grep mariadb找出已经安装的数据库,然后用命令rpm -e --nodeps xxx删除已经安装的软件(xxx为前一步命令找到的软件名)
@roles('mysql')
def installMysql():
    __initSystemEnv(installDicts['mysql']['envProfile'])
    __installBase()
    run('firewall-cmd --zone=public --add-port=21/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=22/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=80/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=3306/tcp --permanent')
    run('firewall-cmd --reload')
    run('rm -rf /etc/my.cnf')
    run('yum -y install make cmake libaio libaio-devel bison-devel ncurses-devel perl-Data-Dumpe')
    run('groupadd mysql && useradd -g mysql mysql -s /sbin/nologin')
    run('mkdir /usr/local/mysql && mkdir /usr/local/mysql/data && mkdir /home/logs/mysql && touch /home/logs/mysql/error.log && chown -R mysql /home/logs/mysql && chgrp -R mysql /home/logs/mysql')

    mysqlLocal = ''.join([installDicts['common']['localPackagePath'], '/mysql/mysql-5.6.37.tar.gz'])
    mysqlRemote = ''.join([installDicts['common']['remotePackagePath'], '/mysql-5.6.37.tar.gz'])
    put(mysqlLocal, mysqlRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf mysql-5.6.37.tar.gz')
        run('cd mysql-5.6.37/ && cmake -DCMAKE_INSTALL_PREFIX=/usr/local/mysql -DMYSQL_DATADIR=/usr/local/mysql/data -DSYSCONFDIR=/etc/my.cnf -DWITH_MYISAM_STORAGE_ENGINE=1 -DWITH_INNOBASE_STORAGE_ENGINE=1 -DMYSQL_UNIX_ADDR=/usr/local/mysql/mysql.sock -DMYSQL_TCP_PORT=3306 -DENABLED_LOCAL_INFILE=1 -DWITH_PARTITION_STORAGE_ENGINE=1 -DEXTRA_CHARSETS=all && make && make install')
        run('chown -R mysql:mysql /usr/local/mysql')

    mysqlConfigLocal = ''.join([installDicts['common']['localPackagePath'], '/mysql/my.cnf'])
    mysqlConfigRemote = '/etc/my.cnf'
    put(mysqlConfigLocal, mysqlConfigRemote)
    with cd('/usr/local/mysql'):
        run('./scripts/mysql_install_db --user=mysql --basedir=/usr/local/mysql --datadir=/usr/local/mysql/data')

    mysqlServiceLocal = ''.join([installDicts['common']['localPackagePath'], '/mysql/mysql.service'])
    mysqlServiceRemote = '/lib/systemd/system/mysql.service'
    put(mysqlServiceLocal, mysqlServiceRemote)
    run('chmod 754 %s' % mysqlServiceRemote)
    run('systemctl enable mysql')

    with cd(installDicts['common']['remotePackagePath']):
        run('rm -rf mysql-5.6.37/ && rm -rf mysql-5.6.37.tar.gz')
    # 后续设置mysql登录帐号和密码以及授权需要登录服务器设置

# 配置mongodb环境
@roles('mongodb')
def installMongodb():
    __initSystemEnv(installDicts['mongodb']['envProfile'])
    __installBase()
    run('firewall-cmd --zone=public --add-port=21/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=22/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=80/tcp --permanent')
    run('firewall-cmd --zone=public --add-port=27017/tcp --permanent')
    run('firewall-cmd --reload')
    run('echo "never" > /sys/kernel/mm/transparent_hugepage/enabled && echo "never" > /sys/kernel/mm/transparent_hugepage/defrag')

    mongoLocal = ''.join([installDicts['common']['localPackagePath'], '/mongodb/mongodb-linux-x86_64-rhel70-3.2.17.tgz'])
    mongoRemote = ''.join([installDicts['common']['remotePackagePath'], '/mongodb-linux-x86_64-rhel70-3.2.17.tgz'])
    put(mongoLocal, mongoRemote)
    with cd(installDicts['common']['remotePackagePath']):
        run('tar -zxvf mongodb-linux-x86_64-rhel70-3.2.17.tgz')
        run('mv mongodb-linux-x86_64-rhel70-3.2.17/ /usr/local/mongodb')
        run('mkdir /usr/local/mongodb/data && mkdir /usr/local/mongodb/data/db && mkdir /usr/local/mongodb/data/logs')
        run('rm -rf mongodb-linux-x86_64-rhel70-3.2.17.tgz')

    mongoConfigLocal = ''.join([installDicts['common']['localPackagePath'], '/mongodb/mongodb.conf'])
    mongoConfigRemote = '/usr/local/mongodb/mongodb.conf'
    put(mongoConfigLocal, mongoConfigRemote)

    # crontab任务对应的txt文件结束必须按回车键另起一行
    mongoCronLocal = ''.join([installDicts['common']['localPackagePath'], '/mongodb/crontab.txt'])
    mongoCronRemote = ''.join([installDicts['common']['remotePackagePath'], '/crontab.txt'])
    put(mongoCronLocal, mongoCronRemote)
    run('crontab %s' % mongoCronRemote)
    run('rm -rf %s' % mongoCronRemote)