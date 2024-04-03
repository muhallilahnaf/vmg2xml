# vmg2xml

Convert VMG files to XML and restore into Android using [SMS Backup & Restore](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore&hl=en&gl=US&pli=1) app.

This repository contains a python script `vmg2xml_script.py` and the code for a Windows executable `.exe`. Both the script and the executable perform the same task: **Convert VMG files to a single XML file**.

VMG files are old SMS backup files having the `.vmg` extension, used primarily by Nokia and Samsung.

The XML file can be read by an app like [SMS Backup & Restore](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore&hl=en&gl=US&pli=1) and you can restore the old SMS from your old Nokia/Samsung phone into an Android smartphone.

Steps:
1. Download [vmg2xml.exe](https://github.com/muhallilahnaf/vmg2xml).
2. Select the **folder** which contains the VMG files.
3. Enter the **country code** *(e.g. +88)*.
4. Click **Start**. VMG files will be converted to a single XML file.
5. **Save** the XML file.
6. **Transfer** the XML file to the Android phone.
7. Install the [SMS Backup & Restore](https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore&hl=en&gl=US&pli=1) app.
8. Open **SMS Backup & Restore** and open the side-menu.
9. Select **Restore > Local Backup Location**.
10. Select **Messages** and locate the XML file.
11. Select **Restore**.

**OR**
use the Python script `vmg2xml_script.py` if you're comfortable with it.