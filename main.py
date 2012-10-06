#!/usr/bin/python
# coding: utf-8


# TODO
# - duplicate

from reporter import Mailer, ReporterCommon


import var


def get():
    reporters = ReporterCommon.__subclasses__()
    for reporter in reporters:
        try:
            obj = reporter()
            obj.report()
        except Exception, err:
            mailer = Mailer()
            mailer.sender = 'error_log@localhost'
            mailer.receiver = var.receiver
            mailer.subject = "movie or ytn news error"
            mailer.attachText(repr(err))
            mailer.send()


if __name__ == "__main__":

    get()
