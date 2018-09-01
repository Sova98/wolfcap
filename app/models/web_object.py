# -*- coding: utf-8 -*-

import datetime


class WebObject:
    def formatted_str(self, value):
        if value:
            return value

        return ''

    def formatted(self, value):
        if value:
            return value

        return ''

    def formatted_dt(self, dt: datetime.datetime, mask: str = None):
        if not dt:
            return ''

        if mask:
            return dt.strftime(mask)
        else:
            return dt.strftime('%d.%m.%Y %H:%M:%S')
