import sys
from MySQLdb import _mysql

with open("a.dat") as fl:
    idx = 0

    sql_file = open("out.sql", "w")
    for line in fl:
        line = line.replace("þ\n", "")
        if len(line) > 1:
            if line[0] == "\ufeff" and line[1] == "þ":
                line = line[2:]
            elif line[0] == "þ":
                line = line[1:]
        lineArr = line.split("þ\x14þ")

        if len(lineArr) != 34:
            sys.exit("lineArr not equal to 34")

        createStr = ""
        columnNames = []
        if idx == 0:
            createStr = "insert into lonny_docs ("
            for a in lineArr:
                na = a.lower()
                na = na.replace("::", "_")
                na = na.replace(" - ", "_")
                na = na.replace(" (email", "_email")
                na = na.replace("files)", "files")
                na = na.replace(" ", "_")
                na = na.replace("combined_date_time_", "")
                if na == "cc":
                    na = "email_cc"
                elif na == "bcc":
                    na = "email_bcc"
                elif na == "from":
                    na = "email_from"
                elif na == "to":
                    na = "email_to"
                elif na == "hash":
                    na = "file_hash"
                if len(columnNames) > 0:
                    createStr += ","
                createStr += na
                columnNames.append(na)
            if len(columnNames) != 34:
                sys.exit("columnNames not equal to 34")
            createStr += ") values "
        else:
            jdx = 0
            if idx > 1:
                createStr += ", "
            createStr += "("
            for j in lineArr:
                if jdx > 0:
                    createStr += ","
                if j == "":
                    createStr += "NULL"
                else:
                    createStr += "'%s'" % bytes.decode(_mysql.escape_string(j), "utf-8")
                jdx += 1
            createStr += ")"

        n = sql_file.write(createStr)
        idx += 1

    sql_file.close()
