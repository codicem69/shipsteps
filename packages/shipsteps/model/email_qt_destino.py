# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('email_qt_destino', pkey='id', name_long='email_qt_destino', name_plural='email_qt_destino',
                        caption_field='email_descr')
        self.sysFields(tbl,counter='sof_id')

        tbl.column('sof_id',size='22', name_long='sof_id'
                    ).relation('sof.id', relation_name='sof_email_qt', mode='foreignkey', onDelete='cascade')
        tbl.column('dest', name_short='!![en]Destination',values='to:to,cc:cc')  
        tbl.column('description', name_short='!![en]Name description')
        tbl.column('email', name_short='Email SOF')
        tbl.column('email_type', size=':3', name_short='!![en]Email type', values='to:to,cc:cc,ccn:ccn')
        #tbl.aliasColumn('agency_id','@sof_id.@arrival_id.agency_id')
        tbl.formulaColumn('email_int',"$dest || ' ' || $description || '<br>'", dtype='T')
        tbl.formulaColumn('email_descr',"""CASE WHEN $description IS NULL THEN $email ELSE $description END""" )