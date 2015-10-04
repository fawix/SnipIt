'''
Created on Sep 26, 2015

This is my attempt of creating a simple and sleek ScreenShot application.
  Inspired by MS Snipping Tool.

Disclaimer: it's meant to work on GNOME3 evironment and it "tries" to use PyGObject 


I am not liable for any loss or damage that might be caused by the use of the software.
Use at your own risk.

@author: Fawix
'''
'''
Disclaimer: this is actually my first time programming in phyton and Gtk!

Structure overview
self.vbox (full window)
+---------------+
| N | S | E | P | << hbox (New / Save / eMail / Pen) ... currently last two buttons are omitted.
+---------------+
|               |
|               | << image
+---------------+


Things to fix later:

1. If user presses SUPER should cancel action and propagate super (no idea how to do that yet)     
4. Send to email client
6. add pen / highlight capabilities
7. edge cases handling on saving file... if file already exists etc 
8. would be nice if dialog could remember last place the user selected 
(no idea how to do that without actually storing the path somewhere yet... gnome probably have a feature for that tho)     
'''

from gi.repository import Gtk, Gdk
from os import path
import sys, cairo, re

class SnipitGUI:

    start_x_cood  = 0 #starting X
    start_y_cood  = 0 #starting Y
    ending_x_cood = 0 #ending X
    ending_y_cood = 0 #ending Y
    firstClickDone = False
    screenShotMode = False
    image = None
    clipboard = None

    def __init__(self):

        self.window = Gtk.Window()
        self.window.set_title("Snip-It")
        self.window.set_icon_from_file('snipit.ico')
        self.window.set_border_width(0)
        self.window.set_default_size(400, 200)

        self.window.connect_after('destroy', self.destroy)
        self.window.connect('key-press-event', self.on_key_function)

        self.create_vbox()
        self.window.add(self.vbox)

        self.area = Gtk.DrawingArea()
        self.area.connect('draw', self.on_draw)
        self.window.connect("motion_notify_event", self.on_motion_notify_event)
        self.window.connect("button_press_event", self.on_button_press_event)
        self.window.connect("button_release_event", self.on_button_release_event)
        self.area.set_events(Gdk.EventType.MOTION_NOTIFY)
        self.vbox.add(self.area)
        self.area.props.expand = True

        self.tranparency_setup()
        self.window.show_all()

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.enter_screenshot_mode()

    def on_motion_notify_event(self, widget, event):
        if event.is_hint:
            x, y, state = event.window.get_pointer()
        else:
            x = event.x
            y = event.y

        if self.firstClickDone:
            self.ending_x_cood = x
            self.ending_y_cood = y
            self.area.queue_draw()

        return True

    def on_button_press_event(self, widget, event):
        if event.button == 1:
            self.firstClickDone = True
            self.start_x_cood  = event.x
            self.start_y_cood  = event.y
            self.ending_x_cood = event.x
            self.ending_y_cood = event.y
            self.area.queue_draw()

    def on_button_release_event(self, widget, event):
        if self.firstClickDone and self.start_x_cood != self.ending_x_cood and self.start_y_cood != self.ending_y_cood:
            self.firstClickDone = False
            self.capture_area()

    def on_key_function(self, widget, event):
        #would be nice to have the super key cancel the action before opening the app browser but is not working
        if event.keyval == Gdk.KEY_Escape or event.keyval == Gdk.KEY_Super_L or event.keyval == Gdk.KEY_Super_R:
            self.on_cancel_action()

    def create_vbox(self):
        self.vbox = Gtk.Box()
        self.vbox.set_spacing(0)
        self.vbox.set_orientation(Gtk.Orientation.VERTICAL)

        self.hbox = Gtk.ButtonBox()
        self.hbox.set_spacing(5)
        self.hbox.set_layout(Gtk.ButtonBoxStyle.CENTER)

        #(type(0-icon 1-label), label or stock icon , click callback)  
        buttons = [(0, "document-new", self.on_new_clicked),
                   (0, "document-save", self.on_save_clicked)
                   #(0, "mail-message-new", self.on_email_clicked),
                   #(0, "mail-send", self.on_pen_clicked)] 
                   #I'll add mail and pen eventually :)
                   ]

        for btype, label, callback in buttons:
            if btype == 0:
                b = Gtk.Button.new_from_icon_name(label, Gtk.IconSize.SMALL_TOOLBAR)
                b.connect("clicked", callback)
                self.hbox.pack_start(b, False, False, 0)
                continue

            elif btype == 1:
                b = Gtk.Button.new_with_label(label)
                b.connect("clicked", callback)
                self.hbox.pack_start(b, False, False, 0)
                continue

            else:
                print("Button with label {0} and type {1} was not added".format(label, btype))

        self.vbox.add(self.hbox)

    def on_save_clicked(self, widget):
        if self.image is not None:
            dialog = Gtk.FileChooserDialog("Please choose a file", self.window,
                Gtk.FileChooserAction.SAVE,
                (("_Cancel"), Gtk.ResponseType.CANCEL,
                 ("_Save"), Gtk.ResponseType.ACCEPT))

            filefilter = Gtk.FileFilter()
            filefilter.add_pixbuf_formats()

            dialog.set_filter(filefilter)
            dialog.set_current_folder(path.expanduser("~"))
            dialog.set_current_name("untitled.png")

            response = dialog.run()

            if response == Gtk.ResponseType.ACCEPT:
                filename = dialog.get_filename()

                if not (re.search("[.](jpg|png|gif)$", filename, flags=0)):
                    filename += ".png"

                self.image.get_pixbuf().savev(filename, path.splitext(filename)[1][1:],"","")

            dialog.destroy()

    def on_email_clicked(self, widget):
        print("fixme: eMail Clicked")

    def on_pen_clicked(self, widget):
        print("fixme: Pen Clicked") 

    def on_new_clicked(self, button):
        self.enter_screenshot_mode()

    def on_cancel_action(self):
        self.remove_tranparency_setup()         
        self.screenShotMode = False
        self.window.unfullscreen()
        self.window.show_all()

    def tranparency_setup(self):    
        screen = self.window.get_screen()
        self.window.set_app_paintable(True)  

        visual = screen.get_rgba_visual()       
        if visual is not None and screen.is_composited():
            self.window.set_visual(visual)

    def remove_tranparency_setup(self):    
        self.window.set_app_paintable(False)  

    def enter_screenshot_mode(self):
        self.tranparency_setup()    
        self.screenShotMode = True
        self.reset()
        self.hbox.hide()
        self.area.show()
        self.window.fullscreen()              
        #self.window.set_opacity(0.5)

    def exit_screenshot_mode(self):
        if self.image is None : 
            self.on_cancel_action();
        else:
            self.remove_tranparency_setup()
            self.screenShotMode = False
            self.vbox.add(self.image)
            self.window.unfullscreen()
            self.window.show_all()
            self.area.hide()

            if self.image.get_storage_type() == Gtk.ImageType.PIXBUF:
                self.clipboard.set_image(self.image.get_pixbuf())
            else:
                print("error: could not put image on clipboard.")

    def on_draw(self, widget, cr):  
        if self.screenShotMode:
            cr.set_source_rgba(0.2, 0.2, 0.2, 0.1)
            cr.rectangle(0, 0, widget.get_allocated_width(), widget.get_allocated_height())
            cr.fill()

            if  self.firstClickDone:
                cr.set_source_rgba(1, 1, 1, 0)
                cr.set_operator(cairo.OPERATOR_CLEAR)
                cr.rectangle(self.start_x_cood, self.start_y_cood, self.ending_x_cood-self.start_x_cood, self.ending_y_cood-self.start_y_cood)
                cr.fill()
        else:
            cr.set_source_rgba(277, 277, 277,0)
            cr.fill()

    def reset(self):
        self.start_x_cood  = 0
        self.start_y_cood  = 0
        self.ending_x_cood = 0
        self.ending_y_cood = 0
        self.firstClickDone = False

        if self.image is not None:
            self.vbox.remove(self.image)

        self.image = None

    def destroy(self, window):
        #self.clipboard.clear() # avoid memory leak ?
        Gtk.main_quit()

    def capture_area(self):
        screen_area = Gdk.get_default_root_window()
        pb = 0

        if self.ending_x_cood > self.start_x_cood:
            pb = Gdk.pixbuf_get_from_window(screen_area, self.start_x_cood, self.start_y_cood, self.ending_x_cood-self.start_x_cood, self.ending_y_cood-self.start_y_cood)
        else:
            pb = Gdk.pixbuf_get_from_window(screen_area, self.ending_x_cood, self.ending_y_cood, self.start_x_cood-self.ending_x_cood, self.start_y_cood-self.ending_y_cood)

        self.image = Gtk.Image.new_from_pixbuf(pb)
        self.exit_screenshot_mode()

def main():
    win = SnipitGUI()
    Gtk.main()

if __name__ == "__main__":
    sys.exit(main())
