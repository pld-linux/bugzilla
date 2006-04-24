#
# With the introduction of a configurable index page using the
# template toolkit, Bugzilla's main index page is now index.cgi.
# Most web servers will allow you to use index.cgi as a directory
# index, and many come preconfigured that way, but if yours doesn't
# then you'll need an index.html file that provides redirection
# to index.cgi. Setting $index_html to 1 below will allow
# checksetup.pl to create one for you if it doesn't exist.
# NOTE: checksetup.pl will not replace an existing file, so if you
#       wish to have checksetup.pl create one for you, you must
#       make sure that index.html doesn't already exist
$index_html = 0;


#
# For some optional functions of Bugzilla (such as the pretty-print patch
# viewer), we need the cvs binary to access files and revisions.
# Because it's possible that this program is not in your path, you can specify
# its location here.  Please specify the full path to the executable.
$cvsbin = "/usr/bin/cvs";



#
# For some optional functions of Bugzilla (such as the pretty-print patch
# viewer), we need the interdiff binary to make diffs between two patches.
# Because it's possible that this program is not in your path, you can specify
# its location here.  Please specify the full path to the executable.
$interdiffbin = "";



#
# The interdiff feature needs diff, so we have to have that path.
# Please specify the directory name only; do not use trailing slash.
$diffpath = "/usr/bin";


#
# If you are using Apache as your web server, Bugzilla can create .htaccess
# files for you that will instruct Apache not to serve files that shouldn't
# be accessed from the web (like your local configuration data and non-cgi
# executable files).  For this to work, the directory your Bugzilla
# installation is in must be within the jurisdiction of a <Directory> block
# in the httpd.conf file that has 'AllowOverride Limit' in it.  If it has
# 'AllowOverride All' or other options with Limit, that's fine.
# (Older Apache installations may use an access.conf file to store these
# <Directory> blocks.)
# If this is set to 1, Bugzilla will create these files if they don't exist.
# If this is set to 0, Bugzilla will not create these files.
$create_htaccess = 0;


#
# This is the group your web server runs as.
# If you have a windows box, ignore this setting.
# If you do not have access to the group your web server runs under,
# set this to "". If you do set this to "", then your Bugzilla installation
# will be _VERY_ insecure, because some files will be world readable/writable,
# and so anyone who can get local access to your machine can do whatever they
# want. You should only have this set to "" if this is a testing installation
# and you cannot set this up any other way. YOU HAVE BEEN WARNED!
# If you set this to anything other than "", you will need to run checksetup.pl
# as root, or as a user who is a member of the specified group.
$webservergroup = "http";



#
# What SQL database to use. Default is mysql. List of supported databases
# can be obtained by listing Bugzilla/DB directory - every module corresponds
# to one supported database and the name corresponds to a driver name.
#
$db_driver = "mysql";



#
# How to access the SQL database:
#
$db_host = 'localhost';         # where is the database?
$db_name = 'bugzilla';              # name of the SQL database
$db_user = 'mysql';              # user to attach to the SQL database

# Sometimes the database server is running on a non-standard
# port. If that's the case for your database server, set this
# to the port number that your database server is running on.
# Setting this to 0 means "use the default port for my database
# server."
$db_port = 0;



#
# Enter your database password here. It's normally advisable to specify
# a password for your bugzilla database user.
# If you use apostrophe (') or a backslash (\) in your password, you'll
# need to escape it by preceding it with a '\' character. (\') or (\)
# (Far simpler just not to use those characters.)
#
$db_pass = '';



# MySQL Only: Enter a path to the unix socket for mysql. If this is 
# blank, then mysql\'s compiled-in default will be used. You probably 
# want that.
$db_sock = '';



#
# Should checksetup.pl try to verify that your database setup is correct?
# (with some combinations of database servers/Perl modules/moonphase this 
# doesn't work)
#
$db_check = 1;


