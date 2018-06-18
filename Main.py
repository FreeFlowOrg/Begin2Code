import gi
import os
import sqlite3
import subprocess

try:
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
except:
    pass
    
class Main:


    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(os.getcwd() + "\Glade\Maingui.glade")
        self.window = self.builder.get_object("Mainwindow")
        self.window.set_position(Gtk.WindowPosition.CENTER)
        self.window.show()
        self.builder.connect_signals(self)
        self.tbox = self.builder.get_object("tbox")
        self.msave = self.builder.get_object("mnusave")
        self.mauto = self.builder.get_object("mnuauto")
        self.tsave = self.builder.get_object("savefile")
        self.tauto = self.builder.get_object("autoclean")
        self.mopen = self.builder.get_object("mnuopen")
        self.topen = self.builder.get_object("openfile")
        self.msave.set_sensitive(False)
        self.mauto.set_sensitive(False)
        self.tauto.set_sensitive(False)
        self.tsave.set_sensitive(False)

        self.filename=""



    def on_Destroy(self, *args):
        Gtk.main_quit(*args)

    def openfile_clicked_cb(self, *args):
        self.dialog = Gtk.FileChooserDialog("Please choose a file",self.window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        self.add_fi(self.dialog)

        response = self.dialog.run()
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + self.dialog.get_filename())
            file = self.dialog.get_filename()
            self.filename=file
            fd = open( file , "r" )
            str = fd.read()
            buf = self.tbox.get_buffer()
            buf.set_text(str)
            self.tbox.set_buffer(buf)
            fd.close()
            self.mopen.set_sensitive(False)
            self.topen.set_sensitive(False)
            self.msave.set_sensitive(True)
            self.mauto.set_sensitive(True)
            self.tauto.set_sensitive(True)
            self.tsave.set_sensitive(True)
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")


        self.dialog.destroy()

    def openclicked(self):
        None


    def add_fi(self,dialog):
        filter_py = Gtk.FileFilter()
        filter_py.set_name("C Files")
        filter_py.add_pattern("*.c")
        dialog.add_filter(filter_py)


    def code_cleaner(self, *args):
        try:
            temp_file = self.filename[0:(len(self.filename)-2)] + "_temp.c"	#Adding the "_temp.c" to filename
            main_file_ptr = open(self.filename,"r")	#Creating file pointer for the main code file
            temp_file_ptr = open(temp_file,"w")	#Creating file pointer for temp file
            count=0				#variable to keep count of the number of "{" or "}"
            count_close = 0
            count_open = 0
            for line in main_file_ptr:
                spaces = '\t'*count		#Giving count number of tabs from next line onwards
                if "{" in line:
                    count+=1	#incrementing count whenever "{"
                    #print count
                    count_open +=1
                if "}" in line:
                    count-=1		#Decrementing count whenever "}"
                    spaces = '\t'*count
                    count_close +=1
                    #print count
                temp_file_ptr.write(spaces)	#First writing spaces into every line
                temp_file_ptr.write(line)	#Then copy contents of every line from main code


            #print count_close, count_open
            temp_file_ptr.close()
            main_file_ptr.close()
            readfile = open( temp_file , "r" )
            str = readfile.read()
            buf = self.tbox.get_buffer()
            buf.set_text(str)
            self.tbox.set_buffer(buf)
            readfile.close()

            if((count_close - count_open) > 0):
                print("Looks like you have more number of \"}\" somewhere")
            if((count_close - count_open) < 0):
                print("Looks like you have more number of \"{\" somewhere")
            return count
        except IOError:
            print("Sorry, but no such file exists in your current working directory")

    def code_execute(exec_filename):
        exec_file = "./"+exec_filename
        subprocess.call([exec_file])


    def save_file(self,*args):
        try:
            temp_file=self.filename[0:(len(self.filename)-2)] + "_temp.c"
            os.remove(self.filename)			#Deleting main code file
            os.rename(temp_file,self.filename)		#Renaming the temp file with main code file

            str = ""
            buf = self.tbox.get_buffer()
            buf.set_text(str)
            self.tbox.set_buffer(buf)

            self.mopen.set_sensitive(True)
            self.topen.set_sensitive(True)
            self.msave.set_sensitive(False)
            self.mauto.set_sensitive(False)
            self.tauto.set_sensitive(False)
            self.tsave.set_sensitive(False)


            dialog = Gtk.MessageDialog(self.window, 0, Gtk.MessageType.INFO,
            Gtk.ButtonsType.OK, "File Saved")
            dialog.format_secondary_text("")
            dialog.run()
            dialog.destroy()
        except IOError:
            dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
            Gtk.ButtonsType.CANCEL, "Cannot Save File")
            dialog.format_secondary_text(
            "Some error Occured.")
            dialog.run()
            dialog.destroy()


        
if __name__ == '__main__':
    Window = Main()
    Gtk.main()
