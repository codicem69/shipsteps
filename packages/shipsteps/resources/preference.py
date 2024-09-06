# preference.py
class AppPref(object):

    def permission_shipsteps(self, **kwargs):
        return 'user'
        
    def prefpane_shipsteps(self,parent,**kwargs):
        tc = parent.tabContainer(margin='2px',**kwargs)
        self.note_remarks(tc.borderContainer(title='!!Remarks'))
        #self.loghi(tc.borderContainer(title='!!Logos'))
        self.privacy(tc.borderContainer(title='!!Email Privacy'))
        self.extra(tc.borderContainer(title='!!Extra'))

    def note_remarks(self,pane):       
        #pane = parent.contentPane(**kwargs)
        #fb = pane.formbuilder()
       # bc = pane.borderContainer(region='center', margin='10px')
        fb = pane.formbuilder(cols=1)
        #fb = bc.contentPane(region='top',height='150px').formbuilder(cols=1)
        # Nei **kwargs c'è già il livello di path dati corretto   
        fb.div('', width='60em')
        fb.simpleTextArea('^.remarks_wheat_corn',lbl='Remarks wheat/corn',width='60em', height='100px',editor=True)
        #grid = bc.contentPane(region='center').quickGrid(value='^.remarks')
        #grid.tools('delrow,addrow,export')
        #grid.column('code', width='30em', name='!![en]Code', edit=True)
        #grid.column('description', width='60em', name='!![en]Description', edit=True)
    #def loghi(self,pane):  
    #    fb = pane.formbuilder(cols=1)    
    #    fb.img(src='^.logo_cc',lbl='Logo CC',
    #                border='2px dotted silver',
    #                crop_width='250px',
    #                crop_height='371px',
    #                edit=True,
    #                placeholder=True,
    #                upload_filename='logo_cc',
    #                upload_folder='site:image')
    #    fb.img(src='^.logo_cp',lbl='Logo CP',
    #                border='2px dotted silver',
    #                crop_width='100px',
    #                crop_height='100px',
    #                edit=True,
    #                placeholder=True,
    #                upload_filename='logo_cc',
    #                upload_folder='site:image')

    def privacy(self,pane):       
        #pane = parent.contentPane(**kwargs)
        #fb = pane.formbuilder()
        fb = pane.formbuilder(cols=1)
        # Nei **kwargs c'è già il livello di path dati corretto   
        fb.div('', width='100em')
        fb.simpleTextArea('^.privacy_email',lbl='Email Privacy',width='100em', height='200px',editor=True)
    
    def extra(self,pane):
        fb = pane.formbuilder(cols=2)
        fb.checkbox('^.ue',lbl='Disabilita paesi UE per pratiche Sanimare', default=False)
        fb.br()
        fb.checkbox('^.pmou',lbl='Disabilita invio PMOU notification', default=False)
        fb.checkbox('^.garbage_adsp',lbl='Disabilita invio Garbage ADSP', default=False)
        fb.checkbox('^.rifiuti_cp',lbl='Disabilita invio ricevuta rifiuti CP', default=False)
        fb.checkbox('^.ref_num', lbl='Disabilita Reference number', default=True)
        fb.checkbox(value='^.delrow_arr', lbl='!![en]Enable Delrow bottom on arrival')
        fb.br()
        fb.div('!![en]<strong>Times for shorepass</strong>')
        fb.br()
        fb.timeTextBox('^.start',lbl='!![en]Start time')
        fb.timeTextBox('^.end',lbl='!![en]End time') 

#class UserPref(object):
#    def prefpane_shipsteps(self, parent, **kwargs):
#        pane = parent.contentPane(**kwargs)
#        fb = pane.formbuilder(cols=1, border_spacing='3px',datapath='.arrivi')
#        fb.checkbox(value='^.delrow_arr', lbl='!![en]Enable Delrow bottom on arrival')

