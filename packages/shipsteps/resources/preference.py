# preference.py
class AppPref(object):
        
    def prefpane_shipsteps(self,parent,**kwargs):
        tc = parent.tabContainer(margin='2px',**kwargs)
        self.note_remarks(tc.borderContainer(title='!!Remarks'))
        #self.loghi(tc.borderContainer(title='!!Logos'))
        self.privacy(tc.borderContainer(title='!!Email Privacy'))
        self.extra(tc.borderContainer(title='!!Extra'))

    def note_remarks(self,pane):       
        #pane = parent.contentPane(**kwargs)
        #fb = pane.formbuilder()
        fb = pane.formbuilder(cols=1)
        # Nei **kwargs c'è già il livello di path dati corretto   
        fb.div('', width='60em')
        fb.simpleTextArea('^.remarks_wheat_corn',lbl='Remarks wheat/corn',width='60em', height='100px',editor=True)
        
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