# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('tasklist', pkey='id', name_long='!![en]Task list', name_plural='!![en]Task list',
                                     caption_field='id', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='arr_tasklist', mode='foreignkey', onDelete='cascade', one_one='*')
        tbl.column('checklist', dtype='B', name_short='Check list')
        tbl.column('frontespizio', dtype='B', name_short='!![en]Vessel Frontispiece')
        tbl.column('cartella_nave', dtype='B', name_short='!![en]Vessel folder')
        tbl.column('modulo_nave', dtype='B', name_short='!![en]Vessel Module')
        tbl.column('tab_servizi', dtype='B', name_short='!![en]Services table')
        tbl.column('front_carico', dtype='B', name_short='!![en]Cargo Frontispiece')
        tbl.column('email_dogana', dtype='B', name_short='!![en]Email Custom GdF')
        tbl.column('email_frontiera', dtype='B', name_short='!![en]Email Immigration')
        tbl.column('email_usma', dtype='B', name_short='Email Usma')
        tbl.column('email_pfso', dtype='B', name_short='Email PFSO')
        tbl.column('email_pilot_moor', dtype='B', name_short='!![en]Email Pilot Moor')
        tbl.column('email_tug', dtype='B', name_short='Email Tug')
        tbl.column('email_garbage', dtype='B', name_short='Email Garbage')
        tbl.column('email_chemist', dtype='B', name_short='Email Chemist')
        tbl.column('email_antifire', dtype='B', name_short='Email Antifire')
        tbl.column('email_gpg', dtype='B', name_short='Email GPG')
        tbl.column('email_ens', dtype='B', name_short='Email ENS')
        tbl.column('form_gdf', dtype='B', name_short='Form GdF')
        tbl.column('form_immigration', dtype='B', name_short='!![en]Immigration form')
        
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.aliasColumn('email_account','@arrival_id.email_account_id')
        
   
