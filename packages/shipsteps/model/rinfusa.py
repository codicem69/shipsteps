
class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('rinfusa', pkey='id', name_long='rinfusa', name_plural='rinfuse',caption_field='id', partition_agency_id='agency_id')
        self.sysFields(tbl)

        tbl.column('arrival_id',size='22', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='rinfusa_arr', mode='foreignkey', onDelete='cascade')
        tbl.column('imb_sba', dtype='B', name_short='!![en]Unloading/Loading',default=False)
        tbl.column('navigazione', name_short='!![en]Navigation', values='Internazionale:Internazionale,Nazionale:Nazionale')
        tbl.column('doc_all', name_short='!![en]Attached docs')
        tbl.aliasColumn('agency_id','@arrival_id.agency_id')
        tbl.formulaColumn('nulla_osta',"""CASE WHEN $imb_sba = True THEN 'allo sbarco' ELSE :sba END""",var_sba="all'imbarco")
        tbl.formulaColumn('piano_imb_sba',"""CASE WHEN $imb_sba = True THEN 'scaricazione' ELSE 'caricazione' END""")
        tbl.formulaColumn('load_unl_plan',"""CASE WHEN $imb_sba = True THEN 'unloading plan' ELSE 'loading plan' END""")
        tbl.formulaColumn('data_attuale',"""CASE WHEN $arrival_id <> ''THEN :currdate END""",var_currdate=self.db.workdate)
    def defaultValues(self):
        return dict(doc_all="""COPIA CERTIFICATO IDONEITA' NAVE AL TRASPORTO MERCI ALLA RINFUSA<br>
                            COPIA CERTIFICATO STOWING MANUAL - COPIA SCHEDA DI SICUREZZA DELLA MERCE<br>
                            ANNESSO 5 BIS - FORM FOR CARGO INFORMATION<br>
                            UNLOADING/LOADING PLAN - CHECK LIST - SCHEDA IMSBC CODE""",imb_sba=False)