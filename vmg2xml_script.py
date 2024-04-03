import os
import re
import chardet
from datetime import datetime
from urllib.parse import unquote


# CHANGE path AND countrycode AS REQUIRED
path = "./Message"
countrycode = "+88"

count = len(os.listdir(path))
xml = "<?xml version='1.0' encoding='UTF-8' standalone='yes' ?>\n"
xml = (
    xml
    + f'<smses count="{count}" backup_set="3ff83320-2c57-44c2-bdd5-7eae6758fcef" backup_date="1711616976109" type="full">\n'
)

for file in os.listdir(path):
    if file.lower().endswith(".vmg"):
        fname = os.path.join(path, file)

        # default encoding
        encoding = "utf-8"
        with open(fname, "rb") as f:
            content = f.read()
            encoding = chardet.detect(content).get("encoding")  # guess encoding

        # open with guessed encoding
        with open(fname, "r", encoding=encoding) as f:

            # assuming vmg file names are in the format: date_contactname.vmg
            [timestamp, contact] = file.split("_")

            # unix timestamp from date
            timestamp = int(datetime.strptime(timestamp, "%Y%m%d%H%M%S").timestamp())

            # if contact not saved in phonebook, contact=(Unknown)
            contact = re.sub(".vmg", "", contact, flags=re.IGNORECASE)
            if contact.startswith(countrycode):
                contact = "(Unknown)"

            content = f.read()

            # read status
            read = 0
            match = re.search(r"X-IRMC-STATUS.+\n", content)
            if match:
                readText = match.group()
                readText = readText.replace("X-IRMC-STATUS:", "").strip()
                if readText == "READ":
                    read = 0
                if readText == "UNREAD":
                    read = 1

            # message type
            msgtype = 1
            match = re.search(r"X-MESSAGE-TYPE.+\n", content)
            if match:
                typeText = match.group()
                typeText = typeText.replace("X-MESSAGE-TYPE:", "").strip()
                if typeText == "DELIVER":
                    msgtype = 1
                if typeText == "SUBMIT":
                    msgtype = 2

            # contact number
            number = ""
            match = re.search(r"CELL.+\n", content)
            if match:
                number = match.group()
                number = number.replace("CELL:", "").strip()
            if number == "":
                match = re.search(r"TEL.+\n", content)
                if match:
                    number = match.group()
                    number = number.replace("TEL:", "").strip()

            # date convert from {16.03.2024 16:15:17} to {16 Mar 2024 4:15:17 pm}
            date = ""
            match = re.search(r"VBODY\nDate:.+\n", content)
            if match:
                date = match.group()
                date = date.replace("VBODY\nDate:", "").strip()
                date_part, time_part = date.split(" ")
                date_obj = datetime.strptime(date_part, "%d.%m.%Y")
                formatted_date = date_obj.strftime("%d %b %Y")
                time_with_meridiem = f"{time_part} {'pm' if int(time_part.split(':')[0]) >= 12 else 'am'}"
                date = f"{formatted_date} {time_with_meridiem}"

            # message body
            body = ""
            match = re.search(
                r"TEXT;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:[\S\s]+END:VBODY",
                content,
            )
            if match:
                body = match.group()
                body = (
                    body.replace("TEXT;CHARSET=UTF-8;ENCODING=QUOTED-PRINTABLE:", "")
                    .replace("END:VBODY", "")
                    .replace("=\n", "")
                    .replace("=0A", "\n")
                    .strip()
                )
                # for text other than english
                # if body.startswith("="):
                #     body = body.replace("=", "%")
                #     body = unquote(body)

            line = f'<sms protocol="0" address="{number}" date="{timestamp}" type="{msgtype}" subject="null" body="{body}" toa="null" sc_toa="null" service_center="null" read="{read}" status="-1" locked="0" date_sent="{timestamp}" sub_id="-1" readable_date="{date}" contact_name="{contact}" />\n'
            xml = xml + line

xml = xml + "</smses>"

# write to xml file
with open("msg.xml", "w", encoding="utf-8") as f:
    f.write(xml)
