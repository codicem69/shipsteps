# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('services_for_email', pkey='id', name_long='!![en]Service for email', name_plural='!![en]Services for email',
                                            caption_field='description_serv',lookup=True)
        self.sysFields(tbl)

        tbl.column('description_serv', name_short='!![en]Service description')
        