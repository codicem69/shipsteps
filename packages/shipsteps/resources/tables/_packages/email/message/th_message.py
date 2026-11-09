#!/usr/bin/python
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import metadata, public_method

class View(BaseComponent):

    @metadata(isMain=True,_if='inout=="O"',_if_inout='^.in_out.current', variable_struct=True)
    def th_sections_sendingstatus(self):
        has_proxy = bool(self.db.package('email').getMailProxy(raise_if_missing=False))
        sections = [dict(code='drafts',caption='!!Drafts',condition="$__is_draft IS TRUE",includeDraft=True),
                    dict(code='to_send',caption='!!Ready to send',isDefault=True,condition='$in_queue = 1 AND $send_date IS NULL')]
        if has_proxy:
            sections.append(dict(code='dispatched_to_proxy',caption='!!Dispatched to proxy',
                                 condition='$proxy_ts IS NOT NULL AND $send_date IS NULL AND $error_ts IS NULL'))
        sections.append(dict(code='sending_error',caption='!!Sending error',condition='$error_ts IS NOT NULL', struct='sending_error'))
        sections.append(dict(code='sent',caption='!!Sent',includeDraft=False,condition='$send_date IS NOT NULL', struct='sent'))
        if has_proxy:
            sections.append(dict(code='queue_issues',caption='!!Queue issues',condition='$queue_mismatch <> 0'))
        sections.append(dict(code='all',caption='!!All',includeDraft=True))
        return sections
    
    
class ViewOutOnly(View):
        
    @metadata(isMain=True, variable_struct=True)
    def th_sections_sendingstatus(self):
        has_proxy = bool(self.db.package('email').getMailProxy(raise_if_missing=False))
        sections = [dict(code='drafts',caption='!!Drafts',condition="$__is_draft IS TRUE",includeDraft=True),
                    dict(code='to_send',caption='!!Ready to send',isDefault=True,condition='$in_queue = 1 AND $send_date IS NULL'),
                    dict(code='sending_error',caption='!!Sending error',condition='$error_ts IS NOT NULL', struct='sending_error'),
                    dict(code='sent',caption='!!Sent',includeDraft=False,condition='$send_date IS NOT NULL')]
        if has_proxy:
            sections.append(dict(code='queue_issues',caption='!!Queue issues',condition='$queue_mismatch <> 0'))
        sections.append(dict(code='all',caption='!!All',includeDraft=True))
        return sections


    @metadata(isMain=True)
    def th_sections_msg_type(self):
        msg_types=self.db.table('email.message_type').query().fetch()
        result = [dict(code='all',caption='All',includeDraft=True)]
        for mt in msg_types:
            result.append(dict(code=mt['code'], caption=mt['description'], condition='$message_type=:m', condition_m=mt['code']))
        return result




