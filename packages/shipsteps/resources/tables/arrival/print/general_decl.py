from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'General declaration arrival'

class Main(BaseResourcePrint):
    batch_title = 'General declaration arrival'
    html_res = 'html_res/general_declaration'
    batch_immediate = 'print'

    def table_script_parameters_pane(self, pane, **kwargs):

        fb = pane.formbuilder(cols=2,border_spacing='3px')

        #fb.textbox(value='^.motivo_approdo', lbl='Motivo approdo',validate_notnull=True, colspan=2, width='40em')
        fb.textbox(value='^.cargo_decl', lbl='Cargo declaration',default='1',validate_notnull=True)
        fb.textbox(value='^.store_list', lbl='Store list',default='1',validate_notnull=True)
        fb.textbox(value='^.crew_list', lbl='Crew list',default='1',validate_notnull=True)
        fb.textbox(value='^.pax_list', lbl='Pax list',default='1',validate_notnull=True)
        fb.textbox(value='^.crew_effects', lbl='Crew effects',default='1',validate_notnull=True)
        fb.textbox(value='^.healt_decl', lbl='Healt declaration',default='1',validate_notnull=True)
        fb.dateTextBox(value='^.data_att', lbl='Data doc.',default=self.db.workdate, validate_notnull=True)

        fb.dataController("""if(msg=='sbarco')genro.publish("floating_message",{message:msg_txt, messageType:"message"});if(msg=='imbarco')genro.publish("floating_message",{message:"Error", messageType:"error"});""", msg='^.motivo_approdo',msg_txt = 'Email ready to be sent')
        #fb.dataController("if(msg=='sbarco') {alert('Message created')}", msg='^.motivo_approdo')

