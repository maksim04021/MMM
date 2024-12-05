import pygame
import sys
import logging
import os
import io

from PyQt6 import uic, QtWidgets
from PyQt6.QtCore import pyqtSignal, QObject, QSize, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QListWidgetItem
from PyQt6.QtGui import QIcon

from check import CheckThread
from metadata_handler import *

auth = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>284</width>
    <height>139</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>М Музыка</string>
  </property>
  <property name="styleSheet">
   <string notr="true">QFrame {
	background: #353535; 
}</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <property name="styleSheet">
    <string notr="true">QWidget {
            background-color: #353535;
            color: #ffffff;
}

QMenu {
    background-color: #353535;
    color: white;
    margin: 2px;
    border-radius: 8px;
}

QMenu::item {
    padding: 5px 30px;
    border-radius: 8px;
}

QMenu::item:selected {
    border: 1px solid black;
    border-radius: 8px;
    font-weight: bold;
}

QMenu::separator {
    height: 1px;
    background-color: black;
    margin-left: 10px;
    margin-right: 5px;
    border-radius: 8px;
}</string>
   </property>
   <widget class="QWidget" name="layoutWidget">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>0</y>
      <width>261</width>
      <height>131</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="verticalLayout">
     <item>
      <widget class="QLineEdit" name="Login">
       <property name="styleSheet">
        <string notr="true">QLineEdit {
	background-color: rgb(74, 74, 74);
	border-radius: 5px;
	padding: 2px;
	color: white;
	border-bottom:1px solid rgb(216, 13, 252);
}</string>
       </property>
       <property name="text">
        <string/>
       </property>
       <property name="placeholderText">
        <string>Login..</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QLineEdit" name="Password">
       <property name="styleSheet">
        <string notr="true">QLineEdit {
	background-color: rgb(74, 74, 74);
	border-radius: 5px;
	padding: 2px;
	color: white;
	border-bottom:1px solid rgb(216, 13, 252);
}</string>
       </property>
       <property name="text">
        <string/>
       </property>
       <property name="placeholderText">
        <string>Password..</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="sup">
       <property name="font">
        <font>
         <family>Arial</family>
         <weight>75</weight>
         <bold>true</bold>
        </font>
       </property>
       <property name="text">
        <string>Sign in</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="sin">
       <property name="font">
        <font>
         <family>Arial</family>
         <weight>75</weight>
         <bold>true</bold>
        </font>
       </property>
       <property name="text">
        <string>Sign up</string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

main = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>769</width>
    <height>556</height>
   </rect>
  </property>
  <property name="sizePolicy">
   <sizepolicy hsizetype="Maximum" vsizetype="Preferred">
    <horstretch>0</horstretch>
    <verstretch>0</verstretch>
   </sizepolicy>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <property name="styleSheet">
   <string notr="true"/>
  </property>
  <widget class="QWidget" name="Search_Window">
   <property name="font">
    <font>
     <family>Arial</family>
     <weight>75</weight>
     <bold>true</bold>
    </font>
   </property>
   <property name="toolTipDuration">
    <number>1</number>
   </property>
   <property name="styleSheet">
    <string notr="true">QWidget {
            background-color: #353535;
            color: #ffffff;
}

QMenu {
    background-color: #353535;
    color: white;
    margin: 2px;
    border-radius: 8px;
}

QMenu::item {
    padding: 5px 30px;
    border-radius: 8px;
}

QMenu::item:selected {
    border: 1px solid black;
    border-radius: 8px;
    font-weight: bold;
}

QMenu::separator {
    height: 1px;
    background-color: black;
    margin-left: 10px;
    margin-right: 5px;
    border-radius: 8px;
}</string>
   </property>
   <layout class="QHBoxLayout" name="horizontalLayout">
    <property name="spacing">
     <number>0</number>
    </property>
    <property name="leftMargin">
     <number>0</number>
    </property>
    <property name="topMargin">
     <number>0</number>
    </property>
    <property name="rightMargin">
     <number>0</number>
    </property>
    <property name="bottomMargin">
     <number>0</number>
    </property>
    <item>
     <widget class="QFrame" name="side_menu">
      <property name="sizePolicy">
       <sizepolicy hsizetype="Preferred" vsizetype="Preferred">
        <horstretch>0</horstretch>
        <verstretch>0</verstretch>
       </sizepolicy>
      </property>
      <property name="maximumSize">
       <size>
        <width>16777215</width>
        <height>16777215</height>
       </size>
      </property>
      <property name="styleSheet">
       <string notr="true">background: rgb(42, 42, 42)</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Raised</enum>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout_6">
       <property name="spacing">
        <number>0</number>
       </property>
       <property name="leftMargin">
        <number>0</number>
       </property>
       <property name="topMargin">
        <number>0</number>
       </property>
       <property name="rightMargin">
        <number>0</number>
       </property>
       <property name="bottomMargin">
        <number>0</number>
       </property>
       <item alignment="Qt::AlignTop">
        <widget class="QFrame" name="frame">
         <property name="styleSheet">
          <string notr="true"/>
         </property>
         <property name="frameShape">
          <enum>QFrame::StyledPanel</enum>
         </property>
         <property name="frameShadow">
          <enum>QFrame::Raised</enum>
         </property>
         <layout class="QVBoxLayout" name="verticalLayout_7">
          <property name="spacing">
           <number>20</number>
          </property>
          <property name="leftMargin">
           <number>5</number>
          </property>
          <property name="topMargin">
           <number>5</number>
          </property>
          <property name="rightMargin">
           <number>5</number>
          </property>
          <property name="bottomMargin">
           <number>5</number>
          </property>
          <item>
           <widget class="QPushButton" name="main_btn1">
            <property name="toolTip">
             <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;About&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
            </property>
            <property name="whatsThis">
             <string/>
            </property>
            <property name="styleSheet">
             <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
}

QPushButton {
			color: #ffffff;
            border: none;
            padding: 2px 6px;
            border-radius: 5px; 
}

QPushButton:hover {
	background-color: rgb(74, 74, 74);
}

QPushButton:pressed {
	background-color: rgb(53, 53, 53);
}</string>
            </property>
            <property name="text">
             <string/>
            </property>
            <property name="icon">
             <iconset>
              <normaloff>:/icons/icons/folder.svg</normaloff>:/icons/icons/folder.svg</iconset>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QPushButton" name="search_btn">
            <property name="toolTip">
             <string>&lt;html&gt;&lt;head/&gt;&lt;body&gt;&lt;p&gt;Search&lt;/p&gt;&lt;/body&gt;&lt;/html&gt;</string>
            </property>
            <property name="styleSheet">
             <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
}

QPushButton {
            color: #ffffff;
            border: none;
            padding: 2px 6px;
            border-radius: 5px; 
}

QPushButton:hover {
	background-color: rgb(74, 74, 74);
}

QPushButton:pressed {
	background-color: rgb(53, 53, 53);
}
</string>
            </property>
            <property name="text">
             <string/>
            </property>
            <property name="icon">
             <iconset>
              <normaloff>:/icons/icons/file-plus.svg</normaloff>:/icons/icons/file-plus.svg</iconset>
            </property>
            <property name="iconSize">
             <size>
              <width>16</width>
              <height>16</height>
             </size>
            </property>
           </widget>
          </item>
          <item>
           <widget class="QPushButton" name="add_sound">
            <property name="toolTip">
             <string>Add song</string>
            </property>
            <property name="styleSheet">
             <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
}

QPushButton {
            color: #ffffff;
            border: none;
            padding: 2px 6px;
            border-radius: 5px; 
}

QPushButton:hover {
	background-color: rgb(74, 74, 74);
}

QPushButton:pressed {
	background-color: rgb(53, 53, 53);
}
</string>
            </property>
            <property name="text">
             <string/>
            </property>
            <property name="icon">
             <iconset>
              <normaloff>:/icons/icons/file-text.svg</normaloff>:/icons/icons/file-text.svg</iconset>
            </property>
           </widget>
          </item>
         </layout>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
    <item>
     <widget class="QFrame" name="main_body">
      <property name="styleSheet">
       <string notr="true">QFrame {
	background: #353535; 
}</string>
      </property>
      <property name="frameShape">
       <enum>QFrame::StyledPanel</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Raised</enum>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout">
       <property name="spacing">
        <number>0</number>
       </property>
       <property name="leftMargin">
        <number>0</number>
       </property>
       <property name="topMargin">
        <number>0</number>
       </property>
       <property name="rightMargin">
        <number>0</number>
       </property>
       <property name="bottomMargin">
        <number>0</number>
       </property>
       <item alignment="Qt::AlignTop">
        <widget class="QFrame" name="header">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Preferred" vsizetype="Preferred">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="styleSheet">
          <string notr="true">background: #353535;</string>
         </property>
         <property name="frameShape">
          <enum>QFrame::StyledPanel</enum>
         </property>
         <property name="frameShadow">
          <enum>QFrame::Raised</enum>
         </property>
         <layout class="QVBoxLayout" name="verticalLayout_3">
          <property name="spacing">
           <number>0</number>
          </property>
          <property name="leftMargin">
           <number>0</number>
          </property>
          <property name="topMargin">
           <number>0</number>
          </property>
          <property name="rightMargin">
           <number>0</number>
          </property>
          <property name="bottomMargin">
           <number>0</number>
          </property>
          <item>
           <widget class="QFrame" name="frame_12">
            <property name="styleSheet">
             <string notr="true"/>
            </property>
            <property name="frameShape">
             <enum>QFrame::StyledPanel</enum>
            </property>
            <property name="frameShadow">
             <enum>QFrame::Raised</enum>
            </property>
            <layout class="QVBoxLayout" name="verticalLayout_4">
             <property name="spacing">
              <number>0</number>
             </property>
             <property name="leftMargin">
              <number>5</number>
             </property>
             <property name="topMargin">
              <number>5</number>
             </property>
             <property name="rightMargin">
              <number>5</number>
             </property>
             <property name="bottomMargin">
              <number>5</number>
             </property>
             <item>
              <widget class="QLineEdit" name="search_line_edit">
               <property name="styleSheet">
                <string notr="true">QLineEdit {
	background-color: rgb(74, 74, 74);
	border-radius: 5px;
	padding: 2px;
	color: white;
	border-bottom:1px solid rgb(216, 13, 252);
}</string>
               </property>
               <property name="placeholderText">
                <string>Search</string>
               </property>
               <property name="cursorMoveStyle">
                <enum>Qt::LogicalMoveStyle</enum>
               </property>
               <property name="clearButtonEnabled">
                <bool>true</bool>
               </property>
              </widget>
             </item>
            </layout>
           </widget>
          </item>
         </layout>
        </widget>
       </item>
       <item>
        <widget class="QFrame" name="body_content">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Preferred" vsizetype="Expanding">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="styleSheet">
          <string notr="true"/>
         </property>
         <property name="frameShape">
          <enum>QFrame::StyledPanel</enum>
         </property>
         <property name="frameShadow">
          <enum>QFrame::Raised</enum>
         </property>
         <layout class="QVBoxLayout" name="verticalLayout_5">
          <property name="spacing">
           <number>9</number>
          </property>
          <property name="leftMargin">
           <number>5</number>
          </property>
          <property name="topMargin">
           <number>0</number>
          </property>
          <property name="rightMargin">
           <number>2</number>
          </property>
          <property name="bottomMargin">
           <number>2</number>
          </property>
          <item>
           <widget class="QScrollArea" name="scrollArea">
            <property name="font">
             <font>
              <family>MS Outlook</family>
              <pointsize>8</pointsize>
             </font>
            </property>
            <property name="styleSheet">
             <string notr="true">/* VERTICAL SCROLLBAR */
 QScrollBar:vertical {
	border: none;
    background:#393939;
    width: 14px;
    margin: 15px 0 15px 0;
	border-radius: 0px;
 }

/*  HANDLE BAR VERTICAL */
QScrollBar::handle:vertical {	
	background-color: rgb(74, 74, 74);
	min-height: 30px;
	border-radius: 7px;
}
QScrollBar::handle:vertical:hover{	
	background-color: rgb(74, 74, 74);
}
QScrollBar::handle:vertical:pressed {	
	background-color: rgb(85, 255, 127);
}

/* BTN TOP - SCROLLBAR */
QScrollBar::sub-line:vertical {
	border: none;
	background-color: rgb(74, 74, 74);
	height: 15px;
	border-top-left-radius: 7px;
	border-top-right-radius: 7px;
	subcontrol-position: top;
	subcontrol-origin: margin;
}
QScrollBar::sub-line:vertical:hover {	
	background-color: rgb(74, 74, 74);
}
QScrollBar::sub-line:vertical:pressed {	
	background-color: rgb(85, 255, 127);
}

/* BTN BOTTOM - SCROLLBAR */
QScrollBar::add-line:vertical {
	border: none;
	background-color: rgb(74, 74, 74);
	height: 15px;
	border-bottom-left-radius: 7px;
	border-bottom-right-radius: 7px;
	subcontrol-position: bottom;
	subcontrol-origin: margin;
}
QScrollBar::add-line:vertical:hover {	
	background-color: rgb(74, 74, 74);
}
QScrollBar::add-line:vertical:pressed {	
	background-color: rgb(85, 255, 127);
}

/* RESET ARROW */
QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
	background: none;
}
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
	background: none;
}








/* HORIZONTAL SCROLLBAR */
QScrollBar:horizontal {
    border: none;
    background: #393939;
    height: 14px; /* Set the width instead of the height */
    margin: 0 15px 0 15px; /* Adjust the margins accordingly */
    border-radius: 0px;
}

/* HANDLE BAR HORIZONTAL */
QScrollBar::handle:horizontal {
    background-color: rgb(74, 74, 74);
    min-width: 30px; /* Set the height instead of the width */
    border-radius: 7px;
}
QScrollBar::handle:horizontal:hover {
    background-color: rgb(74, 74, 74);
}
QScrollBar::handle:horizontal:pressed {
    background-color: rgb(85, 255, 127);
}

/* BTN LEFT - SCROLLBAR */
QScrollBar::sub-line:horizontal {
    border: none;
   	background-color: rgb(74, 74, 74);
    width: 15px; /* Set the height instead of the width */
    border-top-left-radius: 7px;
    border-bottom-left-radius: 7px;
    subcontrol-position: left; /* Change subcontrol position to left */
    subcontrol-origin: margin;
}
QScrollBar::sub-line:horizontal:hover {
    background-color: rgb(74, 74, 74);
}
QScrollBar::sub-line:horizontal:pressed {
    background-color: rgb(85, 255, 127);
}

/* BTN RIGHT - SCROLLBAR */
QScrollBar::add-line:horizontal {
    border: none;
    background-color: rgb(74, 74, 74);
    width: 15px; /* Set the height instead of the width */
    border-top-right-radius: 7px;
    border-bottom-right-radius: 7px;
    subcontrol-position: right; /* Change subcontrol position to right */
    subcontrol-origin: margin;
}
QScrollBar::add-line:horizontal:hover {
    background-color: rgb(74, 74, 74);
}
QScrollBar::add-line:horizontal:pressed {
    background-color: rgb(85, 255, 127);
}

/* RESET ARROW */
QScrollBar::left-arrow:horizontal,
QScrollBar::right-arrow:horizontal {
    background: none;
}
QScrollBar::add-page:horizontal,
QScrollBar::sub-page:horizontal {
    background: none;
}</string>
            </property>
            <property name="frameShape">
             <enum>QFrame::NoFrame</enum>
            </property>
            <property name="widgetResizable">
             <bool>true</bool>
            </property>
            <widget class="QListWidget" name="playlist_widget">
             <property name="geometry">
              <rect>
               <x>0</x>
               <y>0</y>
               <width>708</width>
               <height>434</height>
              </rect>
             </property>
             <property name="font">
              <font>
               <family>Victoria</family>
               <pointsize>10</pointsize>
              </font>
             </property>
             <property name="focusPolicy">
              <enum>Qt::NoFocus</enum>
             </property>
             <property name="autoFillBackground">
              <bool>true</bool>
             </property>
             <property name="styleSheet">
              <string notr="true">QListWidget {
    background-color: #353535;
    padding: 5px;
    border: none;
    border-radius: 10px;
}

QListWidget::item {
    background-color: #353535;
    padding: 5px;
    border: none;
    border-radius: 10px;
	color: white;
	letter-spacing: 3px;
}

QListWidget::item:hover {
    background-color: rgb(74, 74, 74);
}

QListWidget::item:selected {
    color: rgb(85, 255, 127);
}</string>
             </property>
             <property name="dragEnabled">
              <bool>false</bool>
             </property>
             <property name="dragDropOverwriteMode">
              <bool>false</bool>
             </property>
             <property name="dragDropMode">
              <enum>QAbstractItemView::NoDragDrop</enum>
             </property>
             <property name="defaultDropAction">
              <enum>Qt::MoveAction</enum>
             </property>
             <property name="alternatingRowColors">
              <bool>false</bool>
             </property>
             <property name="selectionMode">
              <enum>QAbstractItemView::SingleSelection</enum>
             </property>
             <property name="selectionBehavior">
              <enum>QAbstractItemView::SelectItems</enum>
             </property>
             <property name="verticalScrollMode">
              <enum>QAbstractItemView::ScrollPerPixel</enum>
             </property>
             <property name="horizontalScrollMode">
              <enum>QAbstractItemView::ScrollPerPixel</enum>
             </property>
             <property name="spacing">
              <number>3</number>
             </property>
            </widget>
           </widget>
          </item>
         </layout>
        </widget>
       </item>
       <item alignment="Qt::AlignBottom">
        <widget class="QFrame" name="footer">
         <property name="styleSheet">
          <string notr="true">background: #353535;
</string>
         </property>
         <property name="frameShape">
          <enum>QFrame::StyledPanel</enum>
         </property>
         <property name="frameShadow">
          <enum>QFrame::Raised</enum>
         </property>
         <layout class="QVBoxLayout" name="verticalLayout_2">
          <property name="spacing">
           <number>0</number>
          </property>
          <property name="leftMargin">
           <number>0</number>
          </property>
          <property name="topMargin">
           <number>0</number>
          </property>
          <property name="rightMargin">
           <number>0</number>
          </property>
          <property name="bottomMargin">
           <number>0</number>
          </property>
          <item alignment="Qt::AlignVCenter">
           <widget class="QFrame" name="frame_7">
            <property name="styleSheet">
             <string notr="true">background: rgb(53,53,53)</string>
            </property>
            <property name="frameShape">
             <enum>QFrame::StyledPanel</enum>
            </property>
            <property name="frameShadow">
             <enum>QFrame::Raised</enum>
            </property>
            <layout class="QHBoxLayout" name="horizontalLayout_6">
             <property name="spacing">
              <number>0</number>
             </property>
             <property name="leftMargin">
              <number>5</number>
             </property>
             <property name="topMargin">
              <number>2</number>
             </property>
             <property name="rightMargin">
              <number>5</number>
             </property>
             <property name="bottomMargin">
              <number>2</number>
             </property>
             <item>
              <widget class="QLabel" name="song_label">
               <property name="styleSheet">
                <string notr="true">color: white;
font-weight:bold;</string>
               </property>
               <property name="text">
                <string/>
               </property>
              </widget>
             </item>
            </layout>
           </widget>
          </item>
          <item alignment="Qt::AlignVCenter">
           <widget class="QFrame" name="frame_5">
            <property name="styleSheet">
             <string notr="true">background: #353535;</string>
            </property>
            <property name="frameShape">
             <enum>QFrame::StyledPanel</enum>
            </property>
            <property name="frameShadow">
             <enum>QFrame::Raised</enum>
            </property>
            <layout class="QHBoxLayout" name="horizontalLayout_5">
             <property name="spacing">
              <number>10</number>
             </property>
             <property name="leftMargin">
              <number>5</number>
             </property>
             <property name="topMargin">
              <number>0</number>
             </property>
             <property name="rightMargin">
              <number>5</number>
             </property>
             <property name="bottomMargin">
              <number>0</number>
             </property>
             <item alignment="Qt::AlignLeft|Qt::AlignVCenter">
              <widget class="QLabel" name="duration_label">
               <property name="styleSheet">
                <string notr="true">color: white;
font-weight: bold;</string>
               </property>
               <property name="text">
                <string>00:00</string>
               </property>
              </widget>
             </item>
             <item alignment="Qt::AlignVCenter">
              <widget class="QSlider" name="duration_slider">
               <property name="styleSheet">
                <string notr="true">QSlider::groove:horizontal {
	background-color: grey;
	height: 4px;
	border-radius: 2px;
}

QSlider::sub-page:horizontal {
	background-color:rgb(255, 0, 230);
	border-radius: 2px;
}

QSlider::handle:horizontal {
	background-color: rgb(216, 13, 252);
	border: none;
	width: 10px;
	height: 10px;
	margin: -3px 0;
	border-radius: 5px;
}</string>
               </property>
               <property name="orientation">
                <enum>Qt::Horizontal</enum>
               </property>
              </widget>
             </item>
             <item alignment="Qt::AlignRight|Qt::AlignVCenter">
              <widget class="QLabel" name="duration_label_2">
               <property name="styleSheet">
                <string notr="true">color: white;
font-weight: bold;</string>
               </property>
               <property name="text">
                <string>00:00</string>
               </property>
              </widget>
             </item>
            </layout>
           </widget>
          </item>
          <item>
           <widget class="QFrame" name="frame_6">
            <property name="styleSheet">
             <string notr="true">background: #353535;
</string>
            </property>
            <property name="frameShape">
             <enum>QFrame::StyledPanel</enum>
            </property>
            <property name="frameShadow">
             <enum>QFrame::Raised</enum>
            </property>
            <layout class="QHBoxLayout" name="horizontalLayout_2">
             <property name="spacing">
              <number>0</number>
             </property>
             <property name="leftMargin">
              <number>0</number>
             </property>
             <property name="topMargin">
              <number>0</number>
             </property>
             <property name="rightMargin">
              <number>0</number>
             </property>
             <property name="bottomMargin">
              <number>0</number>
             </property>
             <item alignment="Qt::AlignLeft|Qt::AlignVCenter">
              <widget class="QFrame" name="frame_10">
               <property name="frameShape">
                <enum>QFrame::StyledPanel</enum>
               </property>
               <property name="frameShadow">
                <enum>QFrame::Raised</enum>
               </property>
               <layout class="QHBoxLayout" name="horizontalLayout_4">
                <property name="spacing">
                 <number>5</number>
                </property>
                <property name="leftMargin">
                 <number>5</number>
                </property>
                <property name="topMargin">
                 <number>5</number>
                </property>
                <property name="rightMargin">
                 <number>5</number>
                </property>
                <property name="bottomMargin">
                 <number>5</number>
                </property>
                <item>
                 <widget class="QPushButton" name="sound_button">
                  <property name="toolTip">
                   <string>Mute</string>
                  </property>
                  <property name="styleSheet">
                   <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
	border-radius: 3px;
}
QPushButton {
            color: #ffffff;
            border: none;
            padding: 2px 6px;
            border-radius: 5px;  
}

QPushButton:hover {
	background-color: rgb(74, 74, 74);
}

QPushButton:pressed {
	background-color: rgb(53, 53, 53);
}</string>
                  </property>
                  <property name="text">
                   <string/>
                  </property>
                  <property name="icon">
                   <iconset>
                    <normaloff>:/icons/icons/volume-2.svg</normaloff>:/icons/icons/volume-2.svg</iconset>
                  </property>
                  <property name="iconSize">
                   <size>
                    <width>20</width>
                    <height>20</height>
                   </size>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QSlider" name="volume_slider">
                  <property name="sizePolicy">
                   <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                    <horstretch>0</horstretch>
                    <verstretch>0</verstretch>
                   </sizepolicy>
                  </property>
                  <property name="styleSheet">
                   <string notr="true">QSlider::groove:horizontal {
    background-color: grey;
    height: 4px;
    border-radius: 2px;
}

QSlider::sub-page:horizontal {
    background-color:rgb(255, 0, 230);
    border-radius: 2px;
}

QSlider::handle:horizontal {
    background-color: rgb(216, 13, 252);
    border: none;
    width: 10px;
    height: 10px;
    margin: -3px 0;
    border-radius: 5px;
}

QSlider {
	border-radius: 2px;
}</string>
                  </property>
                  <property name="value">
                   <number>99</number>
                  </property>
                  <property name="orientation">
                   <enum>Qt::Horizontal</enum>
                  </property>
                 </widget>
                </item>
               </layout>
              </widget>
             </item>
             <item alignment="Qt::AlignHCenter">
              <widget class="QFrame" name="frame_9">
               <property name="frameShape">
                <enum>QFrame::StyledPanel</enum>
               </property>
               <property name="frameShadow">
                <enum>QFrame::Raised</enum>
               </property>
               <layout class="QHBoxLayout" name="horizontalLayout_3">
                <property name="spacing">
                 <number>5</number>
                </property>
                <property name="leftMargin">
                 <number>0</number>
                </property>
                <property name="topMargin">
                 <number>0</number>
                </property>
                <property name="rightMargin">
                 <number>0</number>
                </property>
                <property name="bottomMargin">
                 <number>0</number>
                </property>
                <item>
                 <widget class="QPushButton" name="previous_button">
                  <property name="sizePolicy">
                   <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                    <horstretch>0</horstretch>
                    <verstretch>0</verstretch>
                   </sizepolicy>
                  </property>
                  <property name="minimumSize">
                   <size>
                    <width>0</width>
                    <height>0</height>
                   </size>
                  </property>
                  <property name="toolTip">
                   <string>Previous</string>
                  </property>
                  <property name="styleSheet">
                   <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
	border-radius: 3px;
}
QPushButton {
            color: #ffffff;
            border: none;
            padding: 4px 8px;
            border-radius: 12px;  
}

QPushButton:hover {
	background-color: rgb(74, 74, 74);
}

QPushButton:pressed {
	background-color: rgb(53, 53, 53);
}</string>
                  </property>
                  <property name="text">
                   <string/>
                  </property>
                  <property name="icon">
                   <iconset>
                    <normaloff>:/icons/icons/skip-back.svg</normaloff>:/icons/icons/skip-back.svg</iconset>
                  </property>
                  <property name="iconSize">
                   <size>
                    <width>20</width>
                    <height>20</height>
                   </size>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QPushButton" name="pre_button">
                  <property name="sizePolicy">
                   <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                    <horstretch>0</horstretch>
                    <verstretch>0</verstretch>
                   </sizepolicy>
                  </property>
                  <property name="minimumSize">
                   <size>
                    <width>0</width>
                    <height>0</height>
                   </size>
                  </property>
                  <property name="toolTip">
                   <string>- 15</string>
                  </property>
                  <property name="styleSheet">
                   <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
	border-radius: 3px;
}
QPushButton {
            color: #ffffff;
            border: none;
            padding: 4px 8px;
            border-radius: 12px;  
}

QPushButton:hover {
	background-color: rgb(74, 74, 74);
}

QPushButton:pressed {
	background-color: rgb(53, 53, 53);
}</string>
                  </property>
                  <property name="text">
                   <string/>
                  </property>
                  <property name="icon">
                   <iconset>
                    <normaloff>:/icons/icons/rewind.svg</normaloff>:/icons/icons/rewind.svg</iconset>
                  </property>
                  <property name="iconSize">
                   <size>
                    <width>20</width>
                    <height>20</height>
                   </size>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QPushButton" name="play_button">
                  <property name="sizePolicy">
                   <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                    <horstretch>0</horstretch>
                    <verstretch>0</verstretch>
                   </sizepolicy>
                  </property>
                  <property name="toolTip">
                   <string>Play</string>
                  </property>
                  <property name="styleSheet">
                   <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
	border-radius: 3px;
}
QPushButton {
            color: #ffffff;
            border: none;
            padding: 4px 8px;
            border-radius: 12px;  
}

QPushButton:hover {
	background-color: rgb(74, 74, 74);
}

QPushButton:pressed {
	background-color: rgb(53, 53, 53);
}</string>
                  </property>
                  <property name="text">
                   <string/>
                  </property>
                  <property name="icon">
                   <iconset>
                    <normaloff>:/icons/icons/play-circle.svg</normaloff>:/icons/icons/play-circle.svg</iconset>
                  </property>
                  <property name="iconSize">
                   <size>
                    <width>32</width>
                    <height>32</height>
                   </size>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QPushButton" name="forw_button">
                  <property name="sizePolicy">
                   <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                    <horstretch>0</horstretch>
                    <verstretch>0</verstretch>
                   </sizepolicy>
                  </property>
                  <property name="minimumSize">
                   <size>
                    <width>0</width>
                    <height>0</height>
                   </size>
                  </property>
                  <property name="toolTip">
                   <string>+ 15 </string>
                  </property>
                  <property name="styleSheet">
                   <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
	border-radius: 3px;
}
QPushButton {
            color: #ffffff;
            border: none;
            padding: 4px 8px;
            border-radius: 12px;  
}

QPushButton:hover {
	background-color: rgb(74, 74, 74);
}

QPushButton:pressed {
	background-color: rgb(53, 53, 53);
}</string>
                  </property>
                  <property name="text">
                   <string/>
                  </property>
                  <property name="icon">
                   <iconset>
                    <normaloff>:/icons/icons/fast-forward.svg</normaloff>:/icons/icons/fast-forward.svg</iconset>
                  </property>
                  <property name="iconSize">
                   <size>
                    <width>20</width>
                    <height>20</height>
                   </size>
                  </property>
                 </widget>
                </item>
                <item>
                 <widget class="QPushButton" name="following_button">
                  <property name="sizePolicy">
                   <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                    <horstretch>0</horstretch>
                    <verstretch>0</verstretch>
                   </sizepolicy>
                  </property>
                  <property name="minimumSize">
                   <size>
                    <width>0</width>
                    <height>0</height>
                   </size>
                  </property>
                  <property name="toolTip">
                   <string>Following</string>
                  </property>
                  <property name="styleSheet">
                   <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
	border-radius: 3px;
}
QPushButton {
            color: #ffffff;
            border: none;
            padding: 4px 8px;
            border-radius: 12px;  
}

QPushButton:hover {
	background-color: rgb(74, 74, 74);
}

QPushButton:pressed {
	background-color: rgb(53, 53, 53);
}</string>
                  </property>
                  <property name="text">
                   <string/>
                  </property>
                  <property name="icon">
                   <iconset>
                    <normaloff>:/icons/icons/skip-forward.svg</normaloff>:/icons/icons/skip-forward.svg</iconset>
                  </property>
                  <property name="iconSize">
                   <size>
                    <width>20</width>
                    <height>20</height>
                   </size>
                  </property>
                 </widget>
                </item>
               </layout>
              </widget>
             </item>
             <item alignment="Qt::AlignRight|Qt::AlignVCenter">
              <widget class="QFrame" name="frame_8">
               <property name="frameShape">
                <enum>QFrame::StyledPanel</enum>
               </property>
               <property name="frameShadow">
                <enum>QFrame::Raised</enum>
               </property>
               <layout class="QGridLayout" name="gridLayout">
                <property name="leftMargin">
                 <number>5</number>
                </property>
                <property name="topMargin">
                 <number>5</number>
                </property>
                <property name="rightMargin">
                 <number>5</number>
                </property>
                <property name="bottomMargin">
                 <number>5</number>
                </property>
                <item row="0" column="0">
                 <widget class="QPushButton" name="replay_button">
                  <property name="toolTip">
                   <string>Replay</string>
                  </property>
                  <property name="styleSheet">
                   <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
	border-radius: 3px;
}
QPushButton {
            color: #ffffff;
            border: none;
            padding: 2px 6px;
            border-radius: 5px;  
}

QPushButton:hover {
	background-color: rgb(64, 64, 64);
}

QPushButton:checked {
    background-color: rgb(74, 74, 74);
}</string>
                  </property>
                  <property name="text">
                   <string/>
                  </property>
                  <property name="icon">
                   <iconset>
                    <normaloff>:/icons/icons/refresh-cw.svg</normaloff>:/icons/icons/refresh-cw.svg</iconset>
                  </property>
                  <property name="checkable">
                   <bool>false</bool>
                  </property>
                 </widget>
                </item>
                <item row="0" column="4">
                 <widget class="QPushButton" name="shuffle_button">
                  <property name="toolTip">
                   <string>Shuffle</string>
                  </property>
                  <property name="styleSheet">
                   <string notr="true">QToolTip {
	padding: 3px; 
 	background-color: #353535;
	color: white;
    font-weight:bold;
	border:1px solid black;
	border-radius: 3px;
}
QPushButton {
            color: #ffffff;
            border: none;
            padding: 2px 6px;
            border-radius: 5px;  
}

QPushButton:hover {
	background-color: rgb(64, 64, 64);
}

QPushButton:checked {
    background-color: rgb(74, 74, 74);
}</string>
                  </property>
                  <property name="text">
                   <string/>
                  </property>
                  <property name="icon">
                   <iconset>
                    <normaloff>:/icons/icons/repeat.svg</normaloff>:/icons/icons/repeat.svg</iconset>
                  </property>
                  <property name="checkable">
                   <bool>false</bool>
                  </property>
                 </widget>
                </item>
               </layout>
              </widget>
             </item>
            </layout>
           </widget>
          </item>
         </layout>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

logging.basicConfig(filename='music_player.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# --- Обработчик сигналов ---
class SignalHandler(QObject):
    open_window2_signal = pyqtSignal()


# --- Окно авторизации ---
class Auth(QMainWindow):
    def __init__(self, signal_handler):
        super().__init__()
        f = io.StringIO(auth)
        uic.loadUi(f, self)
        self.signal_handler = signal_handler
        self.sup.clicked.connect(self.auth)  # Подключение кнопки входа
        self.sin.clicked.connect(self.register)  # Подключение кнопки регистрации
        self.base_line_edit = [self.Login, self.Password]
        self.check = CheckThread()
        self.setWindowTitle("Auth Window")
        self.setFixedSize(280, 143)
        self.check.Mysignal.connect(self.handle_signal)  # Подключение сигнала от CheckThread
        self.check.start()

    def check_in(func):
        def wrapper(self):
            for line_edit in self.base_line_edit:
                if not line_edit.text():  # Проверка на пустые строки
                    QMessageBox.warning(self, "Ошибка", "Пожалуйста, заполните все поля.")
                    return
            func(self)

        return wrapper

    def handle_signal(self, value):
        try:
            if value == 'Успешная авторизация':
                self.signal_handler.open_window2_signal.emit()
                self.hide()
            elif value == 'Регистрация прошла успешно!':
                QMessageBox.information(self, 'Успех!', value)
                self.close()
            else:
                QMessageBox.warning(self, 'Ошибка', value)
        except Exception as e:
            logging.exception(f"Ошибка в handle_signal: {e}")
            QMessageBox.critical(self, "Критическая ошибка", f"Произошла критическая ошибка: {e}")

    @check_in
    def auth(self):  # Обработка попытки входа
        name = self.Login.text()
        passw = self.Password.text()
        self.check.thr_login(name, passw)

    @check_in
    def register(self):  # Обработка попытки регистрации
        name = self.Login.text()
        passw = self.Password.text()
        self.check.thr_register(name, passw)


# --- Главное окно приложения ---
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        f = io.StringIO(main)
        uic.loadUi(f, self)
        self.init_buttons()
        self.muteF = True
        self.playF = False
        self.current_song = None
        self.is_paused = False
        self.playlist_filenames = get_all_songs(db_path)
        self.add_song_to_playlist = ()
        self.shuffle_mode = False
        self.repeat_mode = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_duration_slider)
        self.volume_slider.valueChanged.connect(self.set_volume)
        self.duration_slider.sliderPressed.connect(self.slider_pressed)
        self.duration_slider.sliderReleased.connect(self.slider_released)
        self.load_songs_from_db()
        self.play_button.clicked.connect(self.toggle_play_pause)
        self.playlist_widget.itemDoubleClicked.connect(self.play_selected_song)

    # --- Инициализация кнопок ---
    def init_buttons(self):
        self.sound_button.clicked.connect(self.mute)
        self.add_sound.clicked.connect(self.add_song)  # Переименовано в add_song
        self.replay_button.clicked.connect(self.replay)  # Необходимо реализовать эту функцию
        self.shuffle_button.clicked.connect(self.shuffle)  # Необходимо реализовать эту функцию
        self.main_btn1.clicked.connect(self.run)  # Необходимо реализовать эту функцию
        self.forw_button.clicked.connect(lambda: self.seek(15))  # Перемотка вперед на 15 секунд
        self.following_button.clicked.connect(self.play_next_song)  # Воспроизвести следующую песню
        self.pre_button.clicked.connect(lambda: self.seek(-15))  # Перемотка назад на 15 секунд
        self.previous_button.clicked.connect(self.play_previous_song)  # Воспроизвести предыдущую песню
        self.search_btn.clicked.connect(self.search_song)  # Необходимо реализовать функцию поиска

        self.set_button_icon(self.sound_button, "icon/volumeup.png", QSize(20, 20))
        self.set_button_icon(self.add_sound, "icon/add_box.png", QSize(20, 20))
        self.set_button_icon(self.shuffle_button, "icon/shuffle.png", QSize(20, 20))
        self.set_button_icon(self.replay_button, "icon/replay.png", QSize(20, 20))
        self.set_button_icon(self.main_btn1, "icon/Логоав.png", QSize(20, 20))
        self.set_button_icon(self.play_button, "icon/play.png", QSize(20, 20))
        self.set_button_icon(self.forw_button, "icon/fast_forward.png", QSize(20, 20))
        self.set_button_icon(self.previous_button, "icon/skip_previous.png", QSize(20, 20))
        self.set_button_icon(self.pre_button, "icon/fast_rewind.png", QSize(20, 20))
        self.set_button_icon(self.search_btn, "icon/search.png", QSize(20, 20))
        self.set_button_icon(self.following_button, "icon/skip_next.png", QSize(20, 20))

    def set_button_icon(self, button, icon_path, icon_size):
        try:
            icon = QIcon(icon_path)
            button.setIcon(icon)
            button.setIconSize(icon_size)
        except FileNotFoundError:
            logging.error(f"Файл иконки не найден: {icon_path}")
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить иконку: {icon_path}")

    # --- Длина песни и метаданные ---
    def get_song_length(self, filepath):
        try:
            audio = MP3(filepath)
            length = int(audio.info.length)
            self.duration_label_2.setText(self.format_time(length))
            self.duration_slider.setMaximum(length)
        except Exception as e:
            logging.exception(f"Ошибка при получении длины песни: {e}")
            self.duration_label_2.setText("Неизвестная продолжительность")
            self.duration_slider.setMaximum(0)
            QMessageBox.warning(self, "Error", f"Не удалось получить длину песни: {e}")

    def load_songs_from_db(self):
        try:
            songs = get_all_songs(db_path)
            self.playlist_widget.clear()
            for filepath, title, artist in songs:
                item = QtWidgets.QListWidgetItem(f"{title} - {artist}")
                item.setData(32, filepath)
                self.playlist_widget.addItem(item)
        except Exception as e:
            logging.exception(f"Ошибка загрузки песен из базы данных: {e}")
            QMessageBox.critical(self, "Ошибка базы данных", "Не удалось загрузить песни из базы данных.")

    # --- Управление воспроизведением ---
    def play_selected_song(self, item):
        filepath = item.data(32)
        self.play(filepath)
        self.playlist_widget.setCurrentItem(item)

    def play(self, filepath):
        try:
            pygame.mixer.music.load(filepath)
            pygame.mixer.music.play()
            self.current_song = filepath
            self.update_song_label(filepath)
            self.get_song_length(filepath)
            self.timer.start(1000)
            self.play_button.setIcon(QIcon("icon/pause.png"))
            self.is_paused = False
        except pygame.error as e:
            logging.exception(f"Ошибка воспроизведения песни Pygame: {e}")
            QMessageBox.critical(self, "Pygame Error", f"Ошибка воспроизведения песни: {e}")
        except Exception as e:
            logging.exception(f"Ошибка воспроизведения песни: {e}")
            QMessageBox.critical(self, "Error", f"Произошла ошибка: {e}")

    def toggle_play_pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.play_button.setIcon(QIcon("icon/play.png"))
            self.is_paused = True
        elif self.is_paused:
            pygame.mixer.music.unpause()
            self.play_button.setIcon(QIcon("icon/pause.png"))
            self.is_paused = False

    def seek(self, seconds):
        if self.current_song:
            try:
                current_pos_ms = pygame.mixer.music.get_pos()
                logging.debug(f"Current position before seek: {current_pos_ms} milliseconds")

                new_pos_ms = max(0, min(current_pos_ms + seconds * 1000, self.duration_slider.maximum() * 1000))
                pygame.mixer.music.set_pos(int(new_pos_ms / 1000.0))
                self.duration_slider.setValue(int(new_pos_ms / 1000))
                self.duration_label.setText(self.format_time(int(new_pos_ms / 1000)))

            except pygame.error as e:
                logging.exception(f"Ошибка перехода к позиции: {e}")
                QMessageBox.critical(self, "Pygame Error", f"Ошибка перехода к позиции: {e}")
            except Exception as e:
                logging.exception(f"Во время поиска произошла непредвиденная ошибка: {e}")
                QMessageBox.critical(self, "Error", f"Произошла непредвиденная ошибка: {e}")

    def slider_pressed(self):
        self.timer.stop()  # Остановить обновление ползунка во время перетаскивания

    def slider_released(self):
        if self.current_song:
            position = self.duration_slider.value()
            try:
                pygame.mixer.music.play(start=position)  # Simpler way to seek
                self.duration_label.setText(self.format_time(position))
                self.timer.start(1000)
            except pygame.error as e:
                logging.exception(f"Ошибка установки позиции: {e}")
                QMessageBox.critical(self, "Pygame Error", f"Ошибка установки позиции: {e}")
            except Exception as e:
                logging.exception(f"An unexpected error occurred during slider release: {e}")
                QMessageBox.critical(self, "Error", f"An unexpected error occurred: {e}")

    def mute(self):
        if self.muteF:
            self.set_button_icon(self.sound_button, "icon/volumeoff.png", QSize(20, 20))
            pygame.mixer.music.set_volume(0)
            self.muteF = False
        else:
            self.set_button_icon(self.sound_button, "icon/volumeup.png", QSize(20, 20))
            pygame.mixer.music.set_volume(self.volume_slider.value() / 100.0)
            self.muteF = True

    def replay(self):
        # Реализовать функционал повтора (воспроизведение текущей песни с начала)
        if self.current_song:
            self.play(self.current_song)

    def shuffle(self):
        # Реализовать функционал случайного воспроизведения
        pass

    def run(self):
        QMessageBox.information(self, "О проекте", "автор: Фролов Максим")
        QMessageBox.information(self, "О проекте", "https://github.com/maksim04021/MMM")

    def play_next_song(self):
        count = self.playlist_widget.count()
        if count > 0:
            current_index = self.playlist_widget.currentRow()
            if current_index == -1:
                current_index = 0
            next_index = (current_index + 1) % count
            item = self.playlist_widget.item(next_index)
            if item:
                self.play(item.data(32))
                self.playlist_widget.setCurrentRow(next_index)

    def play_previous_song(self):
        count = self.playlist_widget.count()
        if count > 0:
            current_index = self.playlist_widget.currentRow()
            if current_index == -1:
                current_index = count - 1
            prev_index = (current_index - 1 + count) % count
            item = self.playlist_widget.item(prev_index)
            if item:
                self.play(item.data(32))
                self.playlist_widget.setCurrentRow(prev_index)

    def add_song_to_playlist(self, filepath):
        self.playlist_filenames = get_all_songs(db_path)

        item = QListWidgetItem(os.path.basename(filepath))
        self.playlist_widget.addItem(item)
        self.playlist.append(filepath)
        self.playlist_filenames.append(os.path.basename(filepath))

    def search_song(self):
        '''
        search_term = self.search_line_edit.text().lower()
        results = [song for song in self.playlist if search_term in song[1].lower() or search_term in song[2].lower()]
        self.playlist = results
        self.update_playlist_widget()
        '''

    # --- Форматирование времени ---
    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return "{:02d}:{:02d}".format(minutes, seconds)

    # --- Обновление ползунка длительности ---
    def update_duration_slider(self):
        if self.current_song and pygame.mixer.music.get_busy() and not self.is_paused:
            current_time = pygame.mixer.music.get_pos() / 1000  # Get position in seconds
            self.duration_slider.setValue(int(current_time))
            self.duration_label.setText(self.format_time(int(current_time)))
        elif not pygame.mixer.music.get_busy():
            self.timer.stop()

    # --- Регулировка громкости ---
    def set_volume(self, value):
        pygame.mixer.music.set_volume(value / 100.0)

    # --- Добавление песни ---
    def add_song(self):
        file, _ = QFileDialog.getOpenFileName(parent=None, caption="Выбери песню",
                                              directory="c:",
                                              filter="music (*.mp3 *.wav)",
                                              initialFilter="music (*.mp3 *.wav)")
        if file:
            self.add_to_playlist(file)

    def add_to_playlist(self, file):
        song_metadata = self.get_song_metadata(file)
        if song_metadata:
            item = QtWidgets.QListWidgetItem(f"{song_metadata['title']} - {song_metadata['artist']}")
            item.setData(32, file)
            self.playlist_widget.addItem(item)

    def get_song_metadata(self, filepath):
        try:
            metadata = add_song_metadata(db_path, filepath)
            if metadata:
                return metadata
            else:
                return {'title': os.path.basename(filepath), 'artist': 'Unknown'}
        except Exception as e:
            logging.exception(f"Ошибка при получении метаданных: {e}")
            return {'title': os.path.basename(filepath), 'artist': 'Unknown'}

    def update_song_label(self, filepath):
        try:
            metadata = self.get_song_metadata(filepath)
            song_info = f"{metadata['title']} - {metadata['artist']}"
            self.song_label.setText(song_info)
        except Exception as e:
            logging.exception(f"Ошибка обновления метки песни: {e}")
            self.song_label.setText("Ошибка загрузки информации о песне.")


# --- Главное выполнение ---
if __name__ == "__main__":
    app = QApplication(sys.argv)
    signal_handler = SignalHandler()
    auth_window = Auth(signal_handler)
    main_window = Main()
    signal_handler.open_window2_signal.connect(main_window.show)
    auth_window.show()
    sys.exit(app.exec())
