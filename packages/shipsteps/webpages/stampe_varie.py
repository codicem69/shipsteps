# -*- coding: utf-8 -*-

"Test page description"
from gnr.core.gnrdecorator import public_method, customizable
from gnr.web.gnrbaseclasses import TableScriptToHtml
from gnr.core.gnrbag import Bag

class GnrCustomWebPage(object):
    #py_requires="gnrcomponents/testhandler:TestHandlerFull,th/th"

    py_requires = """public:Public,th/th:TableHandler"""
    maintable = 'pfda.imbarcazione'

    def windowTitle(self):
        return 'Stampa Stickers'


    def main(self,root,**kwargs):

        pane =root.contentPane(height='100%', margin='15px', border='1px solid silver', datapath='stampa_vessel_details')
        fb = pane.formbuilder(cols=2)
        fb.div("SELECT THE VESSEL")
        fb.br()
        fb.dbSelect(value='^.imb_id', dbtable='shipsteps.vessel_details',alternatePkey='imbarcazione_id', auxColumns='@imbarcazione_id.nome',
                    selected_vessel_name='.nome_imb',hasDownArrow=True)
        fb.button('!![en]Print vessel details', action='FIRE .stampaSticker')
        tbl_htmltemplate = self.db.table('adm.htmltemplate')
        templates= tbl_htmltemplate.query(columns='$id,$name', where='').fetch()
        letterhead=''
        for r in range(len(templates)):
            if templates[r][1] == 'A4_vert':
                letterhead = templates[r][0]

        pane.dataRpc(None, self.downloadTemplatePrint, _fired='^.stampaSticker',
                     table='pfda.imbarcazione',
                     record_id='=.imb_id',nome_imb='=.nome_imb',
                     tplname='datinave',letterhead_id=letterhead)

    @public_method
    def downloadTemplatePrint(self,table=None,tplname=None,letterhead_id=None,record_id=None,nome_imb=None,**kwargs):
        from gnr.web.gnrbaseclasses import TableTemplateToHtml
        #print(x)
        htmlbuilder = TableTemplateToHtml(table=self.db.table(table))
        htmlbuilder(record=record_id,letterhead_id=letterhead_id,template=self.loadTemplate('%s:%s' %(table,tplname)))
        sn = self.site.storageNode(f'page:{nome_imb}.pdf')
        htmlbuilder.writePdf(sn)
        self.setInClientData(path='gnr.downloadurl',
                                    value=sn.url(),
                                    fired=True)
