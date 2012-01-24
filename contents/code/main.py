"""
main.py

@author: Ian Beaver
@organization: NextIT Corporation
@copyright: Copyright (C) 2011 NextIT Corporation, Inc. Spokane, WA. All Rights Reserved.
@license: BSD 2-Clause

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice,
        this list of conditions and the following disclaimer.
    Redistributions in binary form must reproduce the above copyright notice,
        this list of conditions and the following disclaimer in the documentation and/or
        other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS 
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER
OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.

@contact: ibeaver@nextit.com

Sublime Text 2 project launcher Plasma widget for KDE 4.x.  Allows projects to be 
created and launched from the desktop widget.
"""
import glob
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.plasma import Plasma
from PyKDE4.kdeui import KIcon, KDialog
from PyKDE4.kio import KDirWatch
from PyKDE4 import plasmascript
from subprocess import Popen
    
class SublimeText2Applet(plasmascript.Applet):
    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)
    
    def init(self):
        """ Setup plasma layout """
        # Set initial paths
        self.project_path = '~/.sublimetext2/projects'
        self.projects = ""
        self.exe_path = '~/Sublime Text 2/sublime_text'
        self.exe = ""
        self.project_map = {}
        
        # Watch the project directory for updates
        self.dirwatch = KDirWatch(self.applet)
        self.dirwatch.addDir(QString(self.project_path))
        self.connect(self.dirwatch, SIGNAL("dirty(QString)"), self.configChanged)
        
        # Setup layout
        self.setHasConfigurationInterface(True)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.layout = QGraphicsLinearLayout(self.applet)
        self.makeWidget()
        self.layout.addItem(self.list_view)
        self.setLayout(self.layout)
        self.resize(300,200)
    
    def makeWidget(self):
        """ Create the TreeView widget and connect the clicked signal """
        self.list_view = Plasma.TreeView()
        self.list_view.nativeWidget().header().hide()
        self.list_view.nativeWidget().setRootIsDecorated(False)
        self.st2_model = QStandardItemModel()
        self.list_view.setModel(self.st2_model)
        self.initSessionFiles()
        self.connect(self.list_view.nativeWidget(), SIGNAL("activated(const QModelIndex &)"), self.slotOnItemClicked)
        
 
    def initSessionFiles(self):
        """ Create the list items for the TreeView from the project directory """
        index = 1
        item = QStandardItem()
        item.setData("Start Sublime Text 2 (New Project)", role=Qt.DisplayRole)
        item.setIcon(KIcon("document-new"))
        item.setData(index, role=Qt.UserRole+1)
        self.st2_model.appendRow(item)
        
        index += 1
        item = QStandardItem()
        item.setData("Start Sublime Text 2 (Previous Session)", role=Qt.DisplayRole)
        item.setIcon(KIcon("document-edit"))
        item.setData(index, role=Qt.UserRole+1)
        self.st2_model.appendRow(item)
        
        fnames = sorted(glob.iglob(self.project_path+"/*.sublime-project"))
        for fname in fnames:
            name = os.path.basename(fname).rsplit('.')[0]
            if name == 'blank':
                continue
            index += 1
            item = QStandardItem()
            item.setData(name, role=Qt.DisplayRole)
            item.setData(index, role=Qt.UserRole+1)
            self.st2_model.appendRow(item)
            self.project_map[index] = fname
    
    def slotOnItemClicked(self,selection):
        """ Launch the application with the correct arguments """
        index = selection.data(Qt.UserRole+1).toInt()[0]
        if index == 1:
            """ 
                Hack: create a blank project to open to simulate a new blank project
                similar to Kate's behavior.  Hopefully in the future there will be a
                flag for a new project in sublime text that does not also open 
                previous session files.
            """
            with open(self.project_path+"/blank.sublime-project",'w') as blank_proj:
                blank_proj.write('{ "folders":[{}] }')
            with open(self.project_path+"/blank.sublime-workspace",'w') as blank_proj:
                blank_proj.write('''{ "auto_complete":
                                        {
                                                "selected_items":
                                                [
                                                ]
                                        },
                                        "buffers":
                                        [
                                        ],
                                        "build_system": "",
                                        "command_palette":
                                        {
                                                "height": 345.0,
                                                "selected_items":
                                                [
                                                ],
                                                "width": 449.0
                                        },
                                        "console":
                                        {
                                                "height": 0.0
                                        },
                                        "distraction_free":
                                        {
                                                "menu_visible": true,
                                                "show_minimap": false,
                                                "show_open_files": false,
                                                "show_tabs": false,
                                                "side_bar_visible": false,
                                                "status_bar_visible": false
                                        },
                                        "file_history":
                                        [
                                        ],
                                        "find":
                                        {
                                                "height": 0.0
                                        },
                                        "find_in_files":
                                        {
                                                "height": 0.0,
                                                "where_history":
                                                [
                                                ]
                                        },
                                        "find_state":
                                        {
                                                "case_sensitive": false,
                                                "find_history":
                                                [
                                                ],
                                                "highlight": true,
                                                "in_selection": false,
                                                "preserve_case": false,
                                                "regex": false,
                                                "replace_history":
                                                [
                                                ],
                                                "reverse": false,
                                                "show_context": true,
                                                "use_buffer2": true,
                                                "whole_word": false,
                                                "wrap": true
                                        },
                                        "groups":
                                        [
                                                {
                                                        "sheets":
                                                        [
                                                        ]
                                                }
                                        ],
                                        "incremental_find":
                                        {
                                                "height": 0.0
                                        },
                                        "input":
                                        {
                                                "height": 0.0
                                        },
                                        "layout":
                                        {
                                                "cells":
                                                [
                                                        [
                                                                0,
                                                                0,
                                                                1,
                                                                1
                                                        ]
                                                ],
                                                "cols":
                                                [
                                                        0.0,
                                                        1.0
                                                ],
                                                "rows":
                                                [
                                                        0.0,
                                                        1.0
                                                ]
                                        },
                                        "menu_visible": true,
                                        "replace":
                                        {
                                                "height": 0.0
                                        },
                                        "save_all_on_build": true,
                                        "select_file":
                                        {
                                                "height": 0.0,
                                                "selected_items":
                                                [
                                                ],
                                                "width": 0.0
                                        },
                                        "select_project":
                                        {
                                                "height": 0.0,
                                                "selected_items":
                                                [
                                                ],
                                                "width": 0.0
                                        },
                                        "show_minimap": true,
                                        "show_open_files": true,
                                        "show_tabs": false,
                                        "side_bar_visible": true,
                                        "side_bar_width": 303.0,
                                        "status_bar_visible": true
                                }''')
            pid = Popen([self.exe_path,'--project','%s' % self.project_path+"/blank.sublime-project"]).pid
        elif index == 2:
            # Open a new window with the previus contents
            pid = Popen([self.exe_path,'-n']).pid
        else:
            # Open a specific project file
            pid = Popen([self.exe_path,'--project','%s' % self.project_map[index]]).pid
    
    def createConfigurationInterface(self, dlg):
        """ Create the settings menu item to allow the user to set the paths """
        self.groupBox = QGroupBox()
        self.groupBox.setTitle('Projects')
        self.projects = QLineEdit(QString(self.project_path))
        self.exe = QLineEdit(QString(self.exe_path))
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(QLabel(QString('Path to project files')))
        self.vbox.addWidget(self.projects)
        self.vbox.addWidget(QLabel(QString('Path to Sublime Text 2 executable')))
        self.vbox.addWidget(self.exe)
        self.groupBox.setLayout(self.vbox) 
        p = dlg.addPage(self.groupBox, "Settings" )
        p.setIcon( KIcon("preferences-system-windows-actions") )
        dlg.setButtons(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel))
        self.connect(dlg, SIGNAL("okClicked()"), self.configChanged)
    
    def configChanged(self):
        """ A change was made so update the list of projects """
        if self.projects and os.path.exists(self.projects.text()):
            self.dirwatch.removeDir(QString(self.project_path))
            self.project_path = str(self.projects.text())
            self.dirwatch.addDir(QString(self.project_path))
            self.dirwatch.startScan()
        if self.exe and os.path.exists(str(self.exe.text())):
            self.exe_path = str(self.exe.text())
        
        self.st2_model.clear()
        self.project_map = {}
        self.initSessionFiles()
        
    
def CreateApplet(parent):
    return SublimeText2Applet(parent)
