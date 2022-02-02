# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tasklist', pkey='id', name_long='!![en]Task list', name_plural='!![en]Task list',
                                     caption_field='id', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='arr_tasklist', mode='foreignkey', onDelete='cascade', one_one='*')
        tbl.column('cheklist', dtype='B', name_short='Check list')
        tbl.column('frontespizio', dtype='B', name_short='Frontespizio nave')
        tbl.column('cartella_nave', dtype='B', name_short='Cartella arrivo nave')
        tbl.column('modulo_nave', dtype='B', name_short='Modulo nave')
        tbl.column('email_dogana', dtype='B', name_short='Email Dogana')
        tbl.column('email_finanza', dtype='B', name_short='Email Finanza')
        tbl.column('email_frontiera', dtype='B', name_short='Email Frontiera')
        tbl.column('email_usma', dtype='B', name_short='Email Usma')
        tbl.column('email_pfso', dtype='B', name_short='email PFSO')
        tbl.column('email_pilot', dtype='B', name_short='Email Pilota')
        tbl.column('email_mooringmen', dtype='B', name_short='Email Ormeggiatori')
        tbl.column('email_tug', dtype='B', name_short='Email Rimorchio')
        tbl.column('email_garbage', dtype='B', name_short='Email Garbage')
        tbl.column('email_chemist', dtype='B', name_short='Email Chimico')
        tbl.column('email_antifire', dtype='B', name_short='Email Antifire')
        tbl.column('email_gpg', dtype='B', name_short='Email GPG')
        tbl.column('email_ens', dtype='B', name_short='Email ENS')

        tbl.aliasColumn('agency_id','@arrival_id.agency_id')

        