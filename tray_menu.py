#!/usr/bin/python3

# GPL3 License

# Copyright (C) 2020 Morten Eek

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import gi
import subprocess
gi.require_version("Gtk", "3.0")
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk as gtk, AppIndicator3 as appindicator

DEBUG = False


def message(data=None):
    msg=gtk.MessageDialog(parent= None,message_type= gtk.MessageType.INFO,buttons= gtk.ButtonsType.OK,text = data)
    msg.run()
    msg.destroy() 


def exec_comm(cmd, service):
    msg = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    msg = msg.strip()
    if not msg:
        msg = "'" + service + "' executed successfully"
    if DEBUG:
        print(msg)
    return msg


def cmd_item(service, cmd):
  item = gtk.MenuItem(label=service)
  item.connect_object("activate", lambda x: message(exec_comm(cmd, service)), None)
  return item


def menu():
  menu = gtk.Menu()

  menu.append(cmd_item('Start SQL Server', "sudo systemctl start mssql-server"))
  menu.append(cmd_item('Stop SQL Server', "sudo systemctl stop mssql-server"))
  menu.append(gtk.SeparatorMenuItem())  

  menu.append(cmd_item('Start MySQL', "sudo systemctl start mysql"))
  menu.append(cmd_item('Stop MySQL', "sudo systemctl stop mysql"))
  menu.append(gtk.SeparatorMenuItem())

  menu.append(cmd_item('Start PostgreSQL', "sudo systemctl start postgresql"))
  menu.append(cmd_item('Stop PostgreSQL', "sudo systemctl stop postgresql"))
  menu.append(gtk.SeparatorMenuItem())

  menu.append(cmd_item('Start Oracle', "sudo /etc/init.d/oracle-xe start"))
  menu.append(cmd_item('Stop Oracle', "sudo /etc/init.d/oracle-xe stop"))
  menu.append(gtk.SeparatorMenuItem())

  exittray = gtk.MenuItem('Exit Tray')
  exittray.connect('activate', quit)
  menu.append(exittray)
  
  menu.show_all()
  return menu


def quit(_):
  gtk.main_quit()


def main():
  indicator = appindicator.Indicator.new("customtray", "document-properties-symbolic", appindicator.IndicatorCategory.APPLICATION_STATUS)
  indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
  indicator.set_menu(menu())
  gtk.main()


if __name__ == "__main__":
  main()