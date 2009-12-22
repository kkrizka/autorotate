#!/usr/bin/python
from distutils.core import setup

setup (name='autorotate',
       version='0.4',
       description='Automatically rotates the screen of a tablet laptop based on orientation.',
       author='Karol Krizka',
       author_email='kkrizka@gmail.com',
       maintainer='Karol Krizka',
       maintainer_email='kkrizka@gmail.com',
       url='http://www.krizka.net/',
       license='GPL',
       py_modules=['libautorotate'],
       scripts=['auto-rotate.py','manual-rotate.py'],
       data_files = [('share/doc/autorotate',['LICENSE','README']),
                     ('share/dbus-1/system-services',['net.krizka.autorotate.service']),
                     ('/etc/dbus-1/system.d',['net.krizka.autorotate.conf'])]
)
