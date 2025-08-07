# encoding: utf-8
from gnr.core.gnrdecorator import public_method
from gnr.web.gnrbaseclasses import TableTemplateToHtml

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('unsealing', pkey='id', name_long='!![en]Unsealing', name_plural='!![en]Unsealing',caption_field='reg')
        self.sysFields(tbl,counter=True)
        tbl.column('arrival_id',size='22', group='_', name_long='arrival_id'
                    ).relation('arrival.id', relation_name='unsealing_arr', mode='foreignkey', onDelete='raise')
        tbl.column('data', dtype='D', name_long='!![en]Date', name_short='!![en]Date')
        tbl.column('reg', name_long='!![en]Certificate no.', name_short='!![en]Cert.no.')
        tbl.column('htmlbag_unsealing', dtype='X', name_long='HTML Doc Unsealing')

    def counter_reg(self,record=None):
        #25/001
        return dict(format='$K$YY/$NNN', code='', period='YY', date_field='data', showOnLoad=True, date_tolerant=True, recycle=True)
    
    @public_method
    def getHTMLDoc(self,unsealing_id=None,record_template=None,**kwargs):
        if not unsealing_id:
            return 'Please open before the unsealing record'
        testo=TableTemplateToHtml(table=self,record_template=record_template).contentFromTemplate(record=unsealing_id)
        return testo