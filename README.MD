**\"web-logbook\"** is an open-source and free [Python](https://www.python.org/downloads/) application that
allows you to present your digital Diving Logbook in the web such that
you can host your own logbook by yourself.

![main-window](divelogs-main.png)

\"web-logbook\" currently supports only digital logbooks that are
created with the [Windows Diving Log 6.0
application.](https://www.divinglog.com) **(DL6)**. Support for other logbooks
might be in the future.

\"web-logbook\" python application reads the [Diving Log](https://www.divinglog.com) 6.0 sqlite
database file and produces static HTML, CSS, JS that can be hosted
easily on any web serving platform that can serve static HTML. The
python app renders static HTML pages from a logbook database of +1000
dives in a few seconds. Because the web-logbook produces static HTML, it does not require server-side capability to execute PHP or any other
scripts on server side. Serving the plain HTML is extremely fast.

If you have entered GPS coordinates of your dive sites to your database, then you can view maps of your dive sites.

![map](divelogs-map.png)

Dive profiles from your dive computer are shown as interactive SVG (Scalable Vector Graphics) images.
![profile](divelogs-profile.png)

There is also media gallery integration that can show photos and videos
from a web media gallery linked to the dive logs.
![photos](divelogs-photos.png)

\"web-logbook\" uses SPA SSG technology. That means that it is a
[**Static Site Generator (SSG),**](https://en.wikipedia.org/wiki/Static_site_generator) that produces a [Single Page Application
(SPA)](https://en.wikipedia.org/wiki/Single-page_application).

# Examples
Hosted on a personal Linux server:

<https://divelogs.ianleiman.com/logbook.html>

Hosted on Github pages:

https://eianlei.github.io/my-web-logbook/

# Operating

To operate \"web-logbook\" you simply run **\"python main.py\"**, and in a
few seconds it produces for you the latest web view of your logbook that
is immediately available in your web site. You typically run the
application every time you have added new dives or have modified
existing data in your logbook and you want to update the web view to
match your logbook\'s latest content.

For this to happen you of course need to install and configure the app
first and you must have prepared a platform that can host your logbook
web site.

# Hosting web-logbook

There are many ways to host the web-logbook web site for free, as it is only static HTML, CSS and JS files. One example is using GitHub Pages. Read a later section how to do this. You can also use services like Netlify, Vercel, Cloudflare.

You can host the web-logbook web site by yourself if you have a computer
that runs 24/7, can run a web server such as Apache and has http/https
ports open to the public internet with a static IP-address and a DNS
domain name assigned to that IP-address.

You can also buy such a web-hosting service.  

# Exporting DL6 ([Diving Log](https://www.divinglog.com)) database to sqlite format
The logbook database to be used by web-logbook must be in the SQLite file format. [Diving Log](https://www.divinglog.com) application uses internally the [Microsoft Access](https://en.wikipedia.org/wiki/Microsoft_Access) MDB database format.

From [Diving Log](https://www.divinglog.com) application you can export or synchronize your own log data to SQLite database file format. The created file has the extension *.sql. From the File menu select "Export", then "SQLite" and finally the output file name.

![im](DL6-export-sqlite.jpg)

Another possibility is to use the Web Cloud sync, which exports an sqlite database to a cloud service and location of your choice. From main menu select "Web", then the cloud service of your choice. For example "Dropbox", or you can also use "OneDrive" or others. For this method you need to pre-configure where the database is synced. 

It is possible to configure your web server to access directly the sqlite database file synced by this method.

![dropbox-export](DL6-web-dropbox.jpg)

# Installation and configuration

## Python Dependencies

- [Python](https://www.python.org/downloads/) 3.6 is minimum, verified to run on 3.14
- ["PyYAML"](https://pyyaml.org/) for reading the [YAML](https://en.wikipedia.org/wiki/YAML) configuration file
- ["svg.py"](https://github.com/orsinium-labs/svg.py) for producing dive profiles as [SVG images](https://en.wikipedia.org/wiki/SVG)
- [charset_normalizer](https://charset-normalizer.readthedocs.io/) for handling UTF-16/UTF-8 character set interoperability

Note that your web server does not need to run python, you can generate
the web site files with any host that can run python and then copy/sync
the output files to the web server.

## General overview

- You need [Python](https://www.python.org/downloads/) to use this
- clone the sources from this git repository to a host that can run
  python
- it is recommended to use venv for a Python virtual environment
- use pip to install the dependencies
- export your [Diving Log](https://www.divinglog.com) database to a logbook.sql file in [sqlite](https://en.wikipedia.org/wiki/SQLite) format
- provide access to your logbook.sql file or copy it to the host where
  you run the application
- provide access to the root directory of your web server
- configure config.yaml, see next section how
- the app work by running \"python main.py\"
- in config.yaml you specifiy the destination where the web site files
  are written, ideally this your web server root
- you can use \"python -m http.server 8888\" immediately to test the web site on localhost

### logbook.sql from Diving Log

The Windows [Diving Log](https://www.divinglog.com) 6.0 (DL6) application keeps the logbook data in a
Microsoft Access database, a file that has type .MDB. MDB-file can
easily be converted to sqlite3 database format by DL6 itself.
web-logbook uses sqlite3 database format as Python can natively read
such files on any platform.

From [Diving Log](https://www.divinglog.com) application you can export or synchronize your own log data to
SQLite database file format. The created file has by default the
extension \*.sql. If your logbook is named logbook.mdb, then exported
sqlite file would usually be logbook.sql. But you can name the file
however you like.

The most convenient arrangement makes the DL6 exported logbook.sql file
available for the web-logbook application \"python main.py\"

### config.yaml
See example in repo: config.example

main.py reads the configuration file config.yaml, where you configure:

- **logbook_file:** full or relative path to your logbook.sql
- **out_directory:** full or relative path to your web server root, or a  destination of your choosing
- **gallery_use**:
   - **false** to disable media gallery integration
   - **true** to enable media gallery
   - read the section \"Media gallery" for more info
- **gallery_type:** "logbook" or "database"
-    - read the section \"Media gallery" for more info
- **gallery_db:** full or relative path to a sidecar gallery database
    - read the section \"Media gallery" for more info

#### simple example **config.yaml**:
<!-- -->

    ---
    logbook_file: "/path-to-your-db/logbook.sql"
    out_directory: "/var/www/divelogs"
    gallery_use: false

### out_directory

After each run of \"python main.py\", the following files and
subdirectories are created. Ideally these would go directly to your web
server root. But you can of course also transfer or sync them to the
correct location, which can be on another host.

    ├── logbook.html 
    ├── favicon.ico
    ├── MapPinPlace.png
    ├── viewdive.css
    ├── leaflet.css
    ├── divinglog.js
    ├── gen_html_table.js
    ├── leaflet.js
    ├── sitemap.js
    ├── html
    │   ├── brevets_{num}.html
    │   ├── buddy_{num}.html
    │   ├── dive_{num}.html
    │   ├── equipment_{num}.html
    │   ├── place_{num}.html
    │   └── trip_{num}.html
    ├── json
    │   ├── Brevets_summary.json
    │   ├── Buddy_summary.json
    │   ├── Equipment_summary.json
    │   ├── gallery.json
    │   ├── Logbook_summary.json
    │   ├── Place_summary.json
    │   └── Trip_summary.json

- **logbook.html** is the main page, it requires the
  - **css** style files and
  - **javascript** js files that provide interactivity to this Single Page
    Application (SPA)

- **favicon.ico** will be shown in browser tab

- **MapPinPlace.png** is used by the map for dive site markers

- **json** files are used by javascript code to build the tables for
  Logbook, Trips, Places, Buddies, Equipment, Brevets

- **html** files are pre-rendered views for items you select from for
  Logbook, Trips, Places, Buddies, Equipment, Brevets

  

### git-clone web-logbook-rel1

    # log into server
    ssh yourserver
    # clone the web-logbook repository
    cd dirxxx
    git clone git@github.com:eianlei/web-logbook-rel1.git
    # go to app directory
    cd /dirxxx/web-logbook-rel1
    git pull
    # edit config.yaml first! Continue after you have done that
### create virtual environment, pip install libraries
    ## Create venv, install packages, run main.py
    source venv/bin/activate
    pip install PyYAML
    pip install svg.py
    pip install 'charset_normalizer'

### run content update   
    ## activate venv if needed
    source venv/bin/activate
    ## run the content update
    python3 main.py

### Test with local host using Python\'s built-in we server

Assuming your site was generated to directory output

    cd output
    python -m http.server 8888

You can now browse the web-logbook by

<http://127.0.0.1:8888/logbook.html>

# Hosting web-logbook on GitHub pages
web-logbook can be hosted on GitHub pages for free if you have a Github account. 
You do need to have a computer that can run Python to generate the content.
Next instruction assumes your userid is userid

1.	Create a GitHub repository
    -	Go to GitHub and create a new public repository 
    -	Name it anything you like, for example "my-web-logbook"

2.	Add your website files
    -	run "python main.py" to generate files
    -	in your output directory create local git repo and add the remote, see below how
```
     # intialize git
     git init
     git add .
     git commit -m "first commit"
     git remote add "origin" userid@github.com:userid/my-web-logbook.git
     git push 
```
3.	Enable GitHub Pages
    - Go to your repository on GitHub.
    -	Click on the Settings tab.
    -	on left sidebar click pages
    -	Build and deplyment: Source: Deploy from branch
    -	Branch: main, root, SAVE

Wait a few minutes and your logbook will be at: https://<your_userid>.github.io/my-web-logbook/

After each change:
```
     # stage, commit and push
     git add -A
     git commit -m "Your commit message"
     git push 
```


# Hosting web-logbook on a Linux server with Apache

Here is an example how to install and configure web-logbook to a linux
host with following pre-requisites:

- linux host for which you have ssh access and sudo permissions
- host has public IP-address
- you can configure DNS A records to the host IP-address
- there is Apache running
- you have Python 3.6 or newer and can use a venv to install pip
  packages
- you have git installed
- you have certbot installed for https/SSL
- you can copy or sync your logbook.sql database to this host

### Configure your Apache virtual server

Assuming you want to configure your logbook to divelogs.yourdomain.com.
And that the server root is located at /var/www/divelogs, which is what
you would configure into config.yaml as out_directory.

Configure in your DNS configuration divelogs.yourdomain.com to have A
record to your server\'s IP address.

Then configure /etc/apache2/sites-available/divelogs.yourdomain.com.conf

    # divelogs.yourdomain.com
    # plain HTML, CSS, JS served for divelogs.yourdomain.com
    # content from github.com:eianlei/web-logbook-rel1.git
    UseCanonicalName On

    <VirtualHost *:80>
            ServerAdmin admin@xxmail.com
            ServerName divelogs.yourdomain.com
            DocumentRoot /var/www/divelogs
            <Directory /var/www/divelogs/>
                DirectoryIndex logbook.html
                Options -Indexes +FollowSymLinks +MultiViews
                AllowOverride All
                Require all granted
            </Directory>

            ErrorLog ${APACHE_LOG_DIR}/dlog_error.log
            CustomLog ${APACHE_LOG_DIR}/dlog_access.log combined

Then enable the new site and restart apache.

sudo a2ensite divelogs.yourdomain.com.conf

    sudo systemctl reload apache2

Now you can serve http://divelogs.yourdomain.com

Then to get https working you need SSL certificate, here an example
using Lets Encrypt and certbot

    sudo certbot –apache
    sudo systemctl reload apache2

Now you can serve <https://divelogs.yourdomain.com>

The site will serve now your logbook if you have configured in
config.yaml

    out_directory: "/var/www/divelogs"


# Media gallery integration

By setting in config.yaml the variable **\"gallery_use: true\"** you can enable the media gallery integration feature, which is currently only supporting the \"[kuvat.fi](https://kuvat.fi/)\" or
[mediadrive.com](https://mediadrive.com/) media gallery, but you can of course modify the code to suit some other gallery system.

Two separate methods are available to configure the linking of galleries to dives. This is configured by config.yaml variable **\"gallery_type:\"**
- **database**, another sqlite database which contains gallery URLs linked to dive numbers.
  - if using this method then **"gallery_db"** specifies the database file name
- **logbook**, the logbook database itself contains a Userdefined table, which contains column "GalleryUrl" that gallery URLs linked to each dive

## gallery_type: "logbook"
The logbook database itself contains a Userdefined table, which contains column "GalleryUrl" that gallery URLs linked to each dive.

In the [Diving Log](https://www.divinglog.com) application you use this feature by opening in the the Logbook window the tab "Additional", the "User-Defined Fields". Then rename one of the Fields (for example "Field1") as "GalleryUrl". Now you can insert to the "GalleryUrl" for each dive the URL that contains URL to a media linked to that gallery. web-logbook will use this information when generating the web view.

Following example config.yaml will enable this feature:

    ---
    logbook_file: "/path-to-your-db/logbook.sql"
    out_directory: "/var/www/divelogs"
    gallery_use: true
    gallery_type: "logbook"

Example:
![image](divelogs-userdefined.png)

## gallery_type: "database" (database method)
You use another sqlite database which contains gallery URLs linked to dive numbers.
Following example config.yaml will enable this feature:

    ---
    logbook_file: "/path-to-your-db/logbook.sql"
    out_directory: "/var/www/divelogs"
    gallery_use: true
    gallery_type: "database"
    gallery_db: "/path/to/your/gallery.db"

**gallery_type** must be set to \"database\". 

**gallery_db** must be set to the relative or full path to a sqlite database file that has following schema:

table \"Gallery\", has columns:

- ID, INT or TEXT, dive number that matches dive number in logbook
  database, TEXT will be converted to INT if not INT already

- Url, TEXT, url to a kuvat.fi gallery,

  - example:
    \"https://leiman.kuvat.fi/kuvat/Sukellus-SCUBA/2015/2015-04-13+D0508+Dunraven"

- Date, TEXT, date of the dive in ISO format YYYY-MM-DD

- Sitename, TEXT, dive site name, does not have to match the \"Place\"
  in logbook

TEXT columns assumed to be UTF-8 encoded.

If there is no media gallery associated to the dive number, then the
database should not have row with that ID.

## gallery_use: true
If gallery_use: true then

- the \"Photos\" tab in web-logbook menu is displayed, otherwise it is
  hidden.

  - This view will contain an iframe to the kuvat.fi gallery

- \"Dive\" tab will show

  - \"PHOTOS\" button when media available for that dive number,
    otherwise \"NO PHOTO\" text. Clicking this button opens \"Photos\"
    menu tab

  - \"Url\" box has link to the media gallery that opens a new browser
    tab

# Notes on [Diving Log](https://www.divinglog.com) usage
## UTF-16/UTF-8 character set interoperability
**web-logbook** has a built-in function that attempts to fix problems that may (or WILL) arise from UTF-16/UTF-8 character set interoperability issue. This concerns languages that use characters such as äöåÄÖÅ, which encode differently in Windows and in the web.

[Diving Log](https://www.divinglog.com) is a Windows application and as such it saves strings in the Windows native [UTF-16](https://en.wikipedia.org/wiki/UTF-16) encoding also known as [Windows-1252](https://en.wikipedia.org/wiki/Windows-1252) (a variant of ISO-8859-1).

**web-logbook** on the other hand is producing strings using web-native [UTF-8](https://en.wikipedia.org/wiki/UTF-8) encoding. When Windows encoded special characters are encountered, they much be converted to UTF-8 so that they do not show as garbeled. This is especially important when producing URLs, that would not then be found if not encoded as UTF-8. See next table of some examples how different encodins show up in different systems.

|encoding  |Lixux, web view|	Windows view, CHCP 1252|
|--|---|----|
|utf-8 | äöåÖÄÅ |	Ã¤Ã¶Ã¥ÃÃÃ |
|windows |'$'\344\366\345\304\326\305''|	 äöåÄÖÅ |

The safest approach would be to always use plain [ASCII](https://en.wikipedia.org/wiki/ASCII) and avoid non-ASCII, as ASCII characters are always shown the same way everywhere.

## Linked Country, City, Dive Site, Buddy
**web-logbook** works properly only if you link the fields for Country, City, Dive Site, Buddy to detail records.

![linked](dl6-linked.png)

## Dive site GPS
The map function requires that for a dive the "Dive Site" is linked to a "Dive Site" record, and the dive site record has GPS coordinates.
![gps](dp6-gps.png)

## URLs in Comments
Any URLs found in Comments become links that can be clicked and opened in web-logbook. 



# License

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

