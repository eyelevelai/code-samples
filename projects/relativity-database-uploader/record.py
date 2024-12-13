import json


def allCustodians(val):
    return (
        """This file was collected and uploaded by "%s". The custodians of this document include "%s". The custodians of record who own this doc are "%s"."""
        % (val, val, val)
    )


def author(val):
    return (
        """This file was authored by "%s". The creator of this document was "%s". This file or document was written by "%s"."""
        % (val, val, val)
    )


def batesNumber(val):
    return val


def controlNumber(val):
    return val


def custodian(val):
    return (
        """This file was collected and uploaded by "%s". The custodian of this document is "%s". The custodian of record who owns this doc is "%s"."""
        % (val, val, val)
    )


def emailBCC(val):
    return (
        """"%s" were added BCC to this email. The following people were blind copied on this email "%s". Other recipients who were blind copied (BCC) on this email included "%s"."""
        % (val, val, val)
    )


def emailCC(val):
    return (
        """"%s" were added CC to this email. The following people were copied on this email "%s". Other recipients who were copied (CC) on this email included "%s"."""
        % (val, val, val)
    )


def emailFrom(val):
    return (
        """This email was sent by "%s". The sender of this email was "%s". This email was written by "%s"."""
        % (val, val, val)
    )


def emailTo(val):
    return (
        """This email was sent to "%s". The recipient of this email was "%s". This email was received by "%s"."""
        % (val, val, val)
    )


def emailTitle(val):
    return (
        """The subject of this email or loose file is "%s". This is an email or loose file with a subject line of "%s". Email or loose file title subject is "%s"."""
        % (val, val, val)
    )


def emailType():
    return "This file is an email. This document is part of an email thread. This contents of this file contain an email message."


def fileType():
    return "This file is a document of some kind. This is likely to be a document of some type. The contents probably came from a document."


def looseType():
    return "This file is a loose file. This document is considered a loose file. This is a loose file."


def title(val):
    return (
        """The title of this file is "%s". This is a document that is titled "%s". You can call this document "%s"."""
        % (val, val, val)
    )


def processRecord(record):
    process = dict()

    meta = dict()
    for key in record:
        val = record[key]

        if key == "text_link":
            if val == None or val == "":
                print(record)
                raise Exception("record text_link missing")
            else:
                process[key] = val.replace("\\", "/")
                pathArr = process[key].split("/")
                process["filename"] = pathArr[len(pathArr) - 1]
        elif key == "record_id":
            if val == None or val == 0:
                print(record)
                raise Exception("record record_id missing")
            else:
                process[key] = int(val)
                meta[key] = int(val)
        elif val != None:
            if key == "all_custodians_deduplication":
                meta[key] = allCustodians(val)
            elif key == "author":
                meta[key] = author(val)
            elif key == "custodian":
                meta[key] = custodian(val)
            elif key == "control_number":
                meta[key] = controlNumber(val)
            elif key == "email_bcc":
                meta[key] = emailBCC(val)
            elif key == "email_cc":
                meta[key] = emailCC(val)
            elif key == "email_from":
                meta[key] = emailFrom(val)
                meta["doc_type"] = emailType()
            elif key == "email_to":
                meta[key] = emailTo(val)
                meta["doc_type"] = emailType()
            elif key == "production_begin_bates":
                meta[key] = batesNumber(val)
            elif key == "subject_email_and_loose_files":
                meta[key] = emailTitle(val)
                meta["doc_type"] = looseType()
            elif key == "title":
                meta[key] = title(val)
                meta["doc_type"] = fileType()
            else:
                print(key, val)
                raise Exception("Unknown key")

    process["meta"] = meta

    return process
