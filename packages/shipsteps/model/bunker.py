# encoding: utf-8
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('bunker', pkey='id', name_long='bunker', name_plural='bunker',caption_field='id', partition_agency_id='agency_id')
        self.sysFields(tbl,counter=True)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='bunker_arr', mode='foreignkey', onDelete='cascade')
        tbl.column('rank_off', name_short='!![en]Official rank')
        tbl.column('name_off', name_short='!![en]Official name')
        tbl.column('datetime_bunk', dtype='DH', name_short='!![en]Date/time bunker')
        tbl.column('service', name_short='!![en]Service type', values='Assistenza bunker:Assistenza bunker,Assistenza petroliera:Assistenza petroliera')
        tbl.column('durata', dtype='T', name_short='!![en]Duration time')
        tbl.column('ditta_trasp', name_short='!![en]Transport Company ')
        tbl.column('iscr_dt', name_short='!![en]Inscr.no. Trans/company')
        tbl.column('lg_ditta_transp', name_short='Legale rappresentante')
        tbl.column('ditta_forn', name_short='!![en]Supplier Company')
        tbl.column('iscr_forn', name_short='!![en]Inscr.no. Supply/company')
        tbl.column('stamp_transp', dtype='P', name_short='!![en]Transportation Stamp')
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.aliasColumn('dati_cisterne','@bunker_righe.targa_autista')
        tbl.formulaColumn('data_attuale',"""CASE WHEN $arrival_id <> ''THEN :currdate END""",var_currdate=self.db.workdate)


    