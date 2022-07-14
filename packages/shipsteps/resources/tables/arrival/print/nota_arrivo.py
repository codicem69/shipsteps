from gnr.web.batch.btcprint import BaseResourcePrint
from gnr.core.gnrstring import slugify
from datetime import datetime
import string
#from gnr.core.gnrlang import GnrException

caption = 'Nota Arrivo CP'

class Main(BaseResourcePrint):
    batch_title = 'Nota Arrivo CP'
    html_res = 'html_res/nota_arrivo_cp'
    batch_immediate = 'print'
    batch_thermo_lines = 'batch_steps,batch_main,ts_loop'
    virtual_columns = "@agency_id.fullstyle"

    def table_script_parameters_pane(self, pane, **kwargs):

        fb = pane.formbuilder(cols=2,border_spacing='3px')

        fb.textbox(value='^.car_deck', lbl='!![en]Cargo on deck',default='NIL',validate_notnull=True,colspan=2,width='36em')
        fb.textbox(value='^.pax_sba', lbl='!![en]Passengers to disembark',default='0',validate_notnull=True)
        fb.textbox(value='^.hazmat', lbl='HAZMAT',default='NIL',validate_notnull=True)
        fb.textbox(value='^.evento_str', lbl='!![en]Extraordinary event or demage',default='NIL',validate_notnull=True, colspan=2, width='36em')
        fb.dateTextBox(value='^.data_att', lbl='Data doc.',default=self.db.workdate, validate_notnull=True)
