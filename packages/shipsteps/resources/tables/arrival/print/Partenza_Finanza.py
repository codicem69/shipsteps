from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'Partenza Nave'

class Main(BaseResourcePrint):
    batch_title = 'Partenza Finanza'
    html_res = 'html_res/stampa_partenza_finanza'
    batch_immediate = 'print'

    def table_script_parameters_pane(self, pane, **kwargs):

        fb = pane.formbuilder(cols=1,border_spacing='3px')
        fb.div("""Insert cargo loaded""")
        #In kwargs['record_count'] viene automaticamente immagazzinato il conteggio dei record della selezione
        fb.textbox(value='^.carico_partenza',lbl='Carico a bordo', width='30em', placeholder='se lasci in bianco la descrizione sarà VUOTA')
        fb.dateTextBox(value='^.data_att', lbl='data stampa', default=self.db.workdate, format='dd/mm/yyyy')
