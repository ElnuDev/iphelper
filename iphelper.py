from datetime import datetime
import gi
import os.path
import re
import urllib.request

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

LOG = "iphelper.log"
IP_SERVER = "https://ident.me"
INTERNET_SERVER = "https://google.com"

OK = "#40c040"
WARN = "#ff8040"
ERROR = "#ff4040"

class Main:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("iphelper.glade")
        self.builder.connect_signals({
            "gtk_main_quit": Gtk.main_quit,
            "on_button_refresh_clicked": self.load
        })

        window = self.builder.get_object("window")
        window.show()

        self.label_previous_ip = self.builder.get_object("label_previous_ip")
        self.label_current_ip = self.builder.get_object("label_current_ip")
        self.label_ip_status = self.builder.get_object("label_ip_status")
        self.label_updated = self.builder.get_object("label_updated")

        self.load()

    def load(self, *args):
        self.label_previous_ip.set_text("Loading...")
        self.label_current_ip.set_text("Loading...")
        self.label_ip_status.set_text("Loading...")
        self.label_updated.set_text("Loading...")

        if os.path.exists(LOG):
            with open(LOG, 'r') as f:
                self.previous_ip = f.read()
                self.label_previous_ip.set_markup("<span weight=\"ultrabold\">Previous IP</span>\n{}".format(self.previous_ip))
        else:
            self.previous_ip = None
            self.label_previous_ip.set_markup("<span weight=\"ultrabold\">Previous IP</span>\n<span weight=\"ultrabold\" color=\"{}\">Not found</span>".format(WARN))

        try:
                self.current_ip = urllib.request.urlopen(IP_SERVER).read().decode('utf8')
                self.label_current_ip.set_markup("<span weight=\"ultrabold\">Current IP</span>\n{}".format(self.current_ip))
                if self.current_ip == self.previous_ip:
                    self.label_ip_status.set_markup("<span weight=\"ultrabold\" color=\"{}\">Your IP hasn't changed.</span>".format(OK))
                else:
                    self.label_ip_status.set_markup("<span weight=\"ultrabold\" color=\"{}\">Your IP has changed.</span>".format(WARN))
        except:
                self.current_ip = None
                self.label_ip_status.set_markup("<span weight=\"ultrabold\" color=\"{}\">Failed to access <a href=\"{}\">{}</a></span>".format(ERROR, IP_SERVER, IP_SERVER))
                self.label_current_ip.set_markup("<span weight=\"ultrabold\">Current IP</span>\n<span weight=\"ultrabold\" color=\"{}\">Error</span>".format(ERROR))
                try:
                    urllib.request.urlopen(INTERNET_SERVER, timeout=1)
                except urllib.request.URLError as err:
                    self.label_ip_status.set_markup("<span weight=\"ultrabold\" color=\"{}\">No internet.</span>".format(ERROR))
        
        if self.current_ip:
            with open(LOG, 'w') as f:
                f.write(self.current_ip)
        
        self.label_updated.set_markup("<span weight=\"ultrabold\">Last updated</span>\n{}".format(datetime.now().strftime("%d/%m/%Y %H:%M:%S")))

if __name__ == '__main__':
        main = Main()
        Gtk.main()