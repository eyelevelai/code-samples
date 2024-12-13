from MySQLdb import _mysql

from config import rows


def getFile(db, rid):
    db.query(
        """
        SELECT
            %s
        FROM
            lonny_docs
        WHERE
            record_id = %d
        """
        % (rowStr(rows), rid)
    )

    return db.store_result()


def getFiles(db, status, n):
    lm = ""
    if n > 0:
        lm = "LIMIT %d" % n
    db.query(
        """
        SELECT
            %s
        FROM
            lonny_docs
        WHERE
            status = '%s'
        %s
        """
        % (rowStr(rows), status, lm)
    )

    return db.store_result()


def getRecord(r):
    record = r.fetch_row()
    result = dict()
    if len(record) == 1:
        idx = 0
        for i in record[0]:
            if isinstance(i, bytes):
                i = i.decode()
            result[rows[idx]] = i
            idx += 1
    elif len(record) > 1:
        print(record)
        raise Exception("Unexpected record length [%d]" % len(record))
    else:
        raise Exception("empty result")

    return result


def completeRecords(db, prs, dids):
    idx = 0
    ds = []
    for d in dids:
        ds.append("('complete', '%s', %d)" % (d, prs[idx]))
        idx += 1
    db.query(
        """
        INSERT INTO
            lonny_docs
            (status, document_id, record_id)
        VALUES
            %s
        ON DUPLICATE KEY UPDATE
            status = VALUES(status),
            document_id = VALUES(document_id)
        """
        % (rowStr(ds))
    )


def completeRecords(db, prs, dids):
    idx = 0
    ds = []
    for d in dids:
        ds.append("('complete', '%s', %d)" % (d, prs[idx]))
        idx += 1
    db.query(
        """
        INSERT INTO
            lonny_docs
            (status, document_id, record_id)
        VALUES
            %s
        ON DUPLICATE KEY UPDATE
            status = VALUES(status),
            document_id = VALUES(document_id)
        """
        % (rowStr(ds))
    )


def updateRecordStatus(db, rid, st):
    db.query(
        """
        UPDATE
            lonny_docs
        SET
            status='%s'
        WHERE
            record_id = %d
        """
        % (st, rid)
    )


def initDB():
    return _mysql.connect(host="localhost", user="root", database="lonny")


def rowStr(arr):
    return ",".join(str(x) for x in arr)
