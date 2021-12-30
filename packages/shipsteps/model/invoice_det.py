# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('invoice_det', pkey='id', name_long='!![en]Invoice details', name_plural='!![en]Invoice details',caption_field='fullname')
        self.sysFields(tbl)

        tbl.column('rag_sociale', name_short='!![en]Company name')
        tbl.column('address', name_short='!![en]Address')
        tbl.column('cap', name_short='!![en]CAP')
        tbl.column('city', name_short='!![en]City place')
        tbl.column('vat', name_short='!![en]Vat number')
        tbl.column('cf', name_short='!![en]Fiscal code')
        tbl.column('cod_univoco',size='6', name_short='!![en]Unique code')
        tbl.column('pec', name_short='Email pec')
        tbl.formulaColumn('fullname',"""$rag_sociale ||'-'|| $address ||'-'|| $cap ||'-'|| $city || ' - Vat: ' || coalesce($vat,'') || 'unique code: ' ||
                             coalesce($cod_univoco,'') || 'pec: ' || coalesce($pec,'') """ )
        