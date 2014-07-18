import subprocess
import objc
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

class FUSLight(NSApplication):

    def finishLaunching(self):
        # Make statusbar item
        statusbar = NSStatusBar.systemStatusBar()
        self.statusitem = statusbar.statusItemWithLength_(NSVariableStatusItemLength)
        #--- If you want icon, uncomment the code below ---#        
        self.icon = NSImage.alloc().initByReferencingFile_('UiBmerke_grayscale_96.png')
        self.icon.setScalesWhenResized_(True)
        self.icon.setSize_((19, 19))
        self.statusitem.setImage_(self.icon)
        
        self.statusitem.setHighlightMode_(True)
        self.statusitem.setTitle_('')
        self.statusitem.setAttributedTitle_('')

        #make the menu


        #NSFullUserName()
        self.menubarMenu = NSMenu.alloc().init()

        #Add the users name
        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(NSFullUserName(), '', '')
        self.menubarMenu.addItem_(self.menuItem)

        #[newMenu addItem:[NSMenuItem separatorItem]];
        self.menuitem = NSMenuItem.separatorItem()        
        self.menubarMenu.addItem_(self.menuitem)
        
        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Login window', 'loginWindow:', '')
        self.menubarMenu.addItem_(self.menuItem)
        
        #[newMenu addItem:[NSMenuItem separatorItem]];
        self.menuitem = NSMenuItem.separatorItem()        
        self.menubarMenu.addItem_(self.menuitem)
    
        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit', 'terminate:', '')
        self.menubarMenu.addItem_(self.quit)

        #add menu to statusitem
        self.statusitem.setMenu_(self.menubarMenu)
        self.statusitem.setToolTip_('FUS Light')

    def loginWindow_(self, notification):
        #notification is <NSMenuItem: 0x1020c4370 Switch user>
        try:
            proc = subprocess.Popen(["/System/Library/CoreServices/Menu Extras/User.menu/Contents/Resources/CGSession","-suspend"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
        except (OSError) as e:
            NSLog(e)


if __name__ == "__main__":
    app = FUSLight.sharedApplication()
    AppHelper.runEventLoop()
