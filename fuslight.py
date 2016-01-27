from os import system

import subprocess
import objc
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper

# UiB Tools
import sys
sys.path.append('/usr/local/bin')
import uiblibrary

import time

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

        self.menuitem = NSMenuItem.separatorItem()        
        self.menubarMenu.addItem_(self.menuitem)
        
        self.menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Windows homefolder', 'launchUibMountWindowsfolder:', '')
        self.menubarMenu.addItem_(self.menuitem)
        
        self.menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Unix homefolder', 'launchUibMountUnixfolder:', '')
        self.menubarMenu.addItem_(self.menuitem)
        
        self.menuitem = NSMenuItem.separatorItem()        
        self.menubarMenu.addItem_(self.menuitem)
        
        #self.menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('UiB VPN', 'launchUibVpn:', '')
        #self.menubarMenu.addItem_(self.menuitem)
        
        #self.menuitem = NSMenuItem.separatorItem()        
        #self.menubarMenu.addItem_(self.menuitem)
        
        self.menuitem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('UiB Tools', 'launchUibtools:', '')
        self.menubarMenu.addItem_(self.menuitem)

        self.menuitem = NSMenuItem.separatorItem()        
        self.menubarMenu.addItem_(self.menuitem)
         
        self.menuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Login window', 'loginWindow:', '')
        self.menubarMenu.addItem_(self.menuItem)
        
        self.menuitem = NSMenuItem.separatorItem()        
        self.menubarMenu.addItem_(self.menuitem)
    
        self.quit = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_('Quit menubar item', 'terminate:', '')
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

    def launchUibtools_(self, notification):
        try:
            proc = subprocess.Popen(["/Applications/UiB\ Tools.app/Contents/MacOS/UiB\ Tools",], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            #os.system('/Applications/UiB\ Tools.app/Contents/MacOS/UiB\ Tools')
        except (OSError) as e:
            NSLog(e)
            
    def launchUibVpn_(self, notification):
        try:
            uiblibrary.connectvpn("UiB Ansatt VPN", "%s@ansatt" % NSUserName())
        except (OSError) as e:
            NSLog(e) 
            
    def launchUibMountWindowsfolder_(self, notification):
        try:
            uibip = uiblibrary.getstatusuibnet()
            if (uibip):
                uiblibrary.openuriinfinder(uiblibrary.findwindowshomedirectory(NSUserName()))
                s = NSAppleScript.alloc().initWithSource_("tell app \"Finder\" to activate")
                s.executeAndReturnError_(None)
            else:
                uiblibrary.connectvpn("UiB Ansatt VPN", "%s@ansatt" % NSUserName())
                timeout = 0                
                while not uibip and timeout < 5:
                    time.sleep(1)
                    uibip = uiblibrary.getstatusuibnet()
                    print "DEBUG: Waiting for UiB IP"
                    timeout += 1
                if (uibip):
                    uiblibrary.openuriinfinder(uiblibrary.findwindowshomedirectory(NSUserName()))
                    s = NSAppleScript.alloc().initWithSource_("tell app \"Finder\" to activate")
                    s.executeAndReturnError_(None)
                else:
                    print "DEBUG: Still no UiB IP-address, giving up."
                    self.notify("Cant establish connection", "Missing uib-ip", "Please connect to VPN and retry")
                    pass
        except (OSError) as e:
            NSLog(e)         
            
    def launchUibMountUnixfolder_(self, notification):
        try:
            uiblibrary.openuriinfinder(uiblibrary.findunixhomedirectory(NSUserName()))
            s = NSAppleScript.alloc().initWithSource_("tell app \"Finder\" to activate")
            s.executeAndReturnError_(None)        
        except (OSError) as e:
            NSLog(e) 

    def notify(self, title, subtitle, text):
        notification = NSUserNotification.alloc().init()
        notification.setTitle_(str(title))
        notification.setSubtitle_(str(subtitle))
        notification.setInformativeText_(str(text))
        notification.setSoundName_("NSUserNotificationDefaultSoundName")
        NSUserNotificationCenter.defaultUserNotificationCenter().scheduleNotification_(notification)   
            
if __name__ == "__main__":
    app = FUSLight.sharedApplication()
    AppHelper.runEventLoop()
