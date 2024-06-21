#!/usr/bin/python
# -*- coding: utf-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method,metadata
from gnr.core.gnrbag import Bag

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('subject',width='auto')
        r.fieldcell('to_address',width='18em')
        r.fieldcell('cc_address',width='18em')
        r.fieldcell('bcc_address',width='18em')
        r.fieldcell('uid',width='7em')
        r.fieldcell('__ins_ts',width='7em')
        #r.fieldcell('sent',width='7em') #use send_date instead
        #r.fieldcell('user_id',width='35em')
        r.fieldcell('account_id',width='12em')

    def th_queryBySample(self):
        return dict(fields=[dict(field='send_date',lbl='!!Send date',width='7em'),
                            dict(field='subject', lbl='!!Subject'),
                            dict(field='body_plain',lbl='!!Content'),
                            dict(field='to_address', lbl='To address'),
                            dict(field='from_address', lbl='From address')],cols=5,isDefault=True)

    def th_order(self):
        return '__ins_ts:d'

    def th_query(self):
        return dict(column='subject',op='contains', val='')#,runOnStart=False)
    
    def th_options(self):
        return dict(partitioned=True,liveUpdate=True)

    def th_top_upperbar(self,top):
        bar=top.slotToolbar('5,sections@in_out,*,sections@sendingstatus,*,updatebtn',
                        childname='upper',_position='<bar')
        bar.updatebtn.slotButton('!!Update',action="""this.form.reload();""")
        

    def th_struct_sending_error(self,struct):
        r = struct.view().rows()
        r.fieldcell('subject',width='auto')
        r.fieldcell('to_address',width='18em')
        r.fieldcell('cc_address',width='18em')
        r.fieldcell('bcc_address',width='18em')
        r.fieldcell('error_msg',width='10em')
        r.fieldcell('error_ts',width='8em')
        r.fieldcell('__ins_ts',width='7em')
        r.fieldcell('account_id',width='12em')

    def th_struct_sent(self,struct):
        r = struct.view().rows()
        r.fieldcell('subject',width='auto')
        r.fieldcell('to_address',width='18em')
        r.fieldcell('cc_address',width='18em')
        r.fieldcell('bcc_address',width='18em')
        r.fieldcell('__ins_ts',width='7em')        
        r.fieldcell('send_date',width='8em')
        r.fieldcell('account_id',width='12em')

    @metadata(isMain=True,_if='inout=="o"',_if_inout='^.in_out.current', variable_struct=True)
    def th_sections_sendingstatus(self):
        return [dict(code='drafts',caption='!!Drafts',condition="$__is_draft IS TRUE",includeDraft=True),
                dict(code='to_send',caption='!!Ready to send',isDefault=True,condition='$send_date IS NULL AND $error_msg IS NULL'),
                dict(code='sending_error',caption='!!Sending error',condition='$error_msg IS NOT NULL', struct='sending_error'),
                dict(code='sent',caption='!!Sent',includeDraft=False,condition='$send_date IS NOT NULL', struct='sent'),
                dict(code='all',caption='All',includeDraft=True)]


class ViewOutOnly(View):
        
    def th_top_upperbar(self,top):
        top.slotToolbar('5,sections@sendingstatus,*,sections@msg_type',
                        childname='upper',_position='<bar')

    @metadata(isMain=True, variable_struct=True)
    def th_sections_sendingstatus(self):
        return [dict(code='drafts',caption='!!Drafts',condition="$__is_draft IS TRUE",includeDraft=True),
                dict(code='to_send',caption='!!Ready to send',isDefault=True,condition='$send_date IS NULL AND $error_msg IS NULL'),
                dict(code='sending_error',caption='!!Sending error',condition='$error_msg IS NOT NULL', struct='sending_error'),
                dict(code='sent',caption='!!Sent',includeDraft=False,condition='$send_date IS NOT NULL'),
                dict(code='all',caption='All',includeDraft=True)]


    @metadata(isMain=True)
    def th_sections_msg_type(self):
        msg_types=self.db.table('email.message_type').query().fetch()
        result = [dict(code='all',caption='All',includeDraft=True)]
        for mt in msg_types:
            result.append(dict(code=mt['code'], caption=mt['description'], condition='$message_type=:m', condition_m=mt['code']))
        return result

    def th_options(self):
        return dict()

    def th_condition(self):
        return dict(condition='$in_out=:io',condition_io='O')



class ViewInOnly(View):
    def th_top_upperbar(self,top):
        pass

    def th_condition(self):
        return dict(condition='$in_out=:io',condition_io='I')

    

class ViewFromMailbox(View):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('to_address',width='7em')
        r.fieldcell('from_address',width='7em')
        r.fieldcell('cc_address',width='7em')
        r.fieldcell('bcc_address',width='7em')
        r.fieldcell('uid',width='7em')
        r.fieldcell('body',width='7em')
        r.fieldcell('body_plain',width='7em')
        r.fieldcell('html',width='7em')
        r.fieldcell('subject',width='7em')
        r.fieldcell('send_date',width='7em')
        r.fieldcell('sent',width='7em')
        r.fieldcell('user_id',width='35em')
        r.fieldcell('account_id',width='35em')

class ViewFromDashboard(View):
    
    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('send_date',width='7em',dtype='DH')
        r.fieldcell('to_address',width='12em')
        r.fieldcell('from_address',width='12em')
        r.fieldcell('subject',width='100%')
        r.fieldcell('account_id',hidden=True)
        r.fieldcell('mailbox_id',hidden=True)

    def th_order(self):
        return 'send_date:d'

class Form(BaseComponent):
    py_requires = "gnrcomponents/attachmanager/attachmanager:AttachManager"

    def attemptStruct(self,struct ):

        r = struct.view().rows()
        r.cell('tag',name='Tag', width='7em')
        r.cell('ts',name='Ts')
        r.cell('error',name='Error', width='100%')

    def th_form(self, form):
        bc = form.center.borderContainer(margin='5px')
        top = bc.contentPane(region='top',datapath='.record')
        fb = top.div(margin_right='20px').formbuilder(cols=4,border_spacing='3px',
                                                    fld_width='100%',
                                                    width='100%',
                                                    colswidth='auto')
        fb.field('in_out')
        fb.field('subject', colspan=3)
        fb.field('to_address',colspan=2)
        fb.field('from_address',colspan=2)
        fb.field('cc_address',colspan=2)
        fb.field('bcc_address',colspan=2)
        fb.field('send_date', tag='div')
        fb.field('html',html_label=True)
        fb.field('__is_draft', lbl='!![en]Draft')

        tc = bc.tabContainer(region='center', margin_top='15px')
        tc.contentPane(title='Body').simpleTextArea(value='^.record.body',editor=True)
        sc = tc.stackContainer(title='Attachments')
        sc.plainTableHandler(relation='@attachments',pbl_classes=True)
        sc.attachmentGrid(pbl_classes=True,uploaderButton=True)
        tc.dataController("sc.switchPage(in_out=='O'?1:0)",sc=sc.js_widget,in_out='^#FORM.record.in_out')
        tc.contentPane(title='Body plain', hidden='^.record.body_plain?=!#v').simpleTextArea(value='^.record.body_plain',height='100%')
        errors_pane = tc.contentPane(title='Errors', region='center', datapath='.record')
        errors_bg = errors_pane.bagGrid(frameCode='sending_attempts',title='Attempts',datapath='#FORM.errors',
                                                            struct=self.attemptStruct,
                                                            storepath='#FORM.record.sending_attempt',
                                                            pbl_classes=True,margin='2px',
                                                            delrow=False,datamode='attr')
        errors_bg.top.bar.replaceSlots('addrow','clearerr,2')
        errors_bg.top.bar.clearerr.slotButton('Clear errors').dataRpc(
                    self.db.table('email.message').clearErrors, pkey='=#FORM.record.id', _onResult='this.form.reload();')

        #fb.dataRpc('dummy',self.test_email,data_invio='^shipsteps_arrival.form.email_message.form.record.send_date',_if='data_invio', 
        #                   err_msg='=shipsteps_arrival.form.email_message.form.record.error_msg',tmp_code='=shipsteps_arrival.form.email_message.form.record.template_code',
        #                   _onResult="""if(result.getItem('email')=='email_dogana'){SET shipsteps_arrival.form.record.@arr_tasklist.email_dogana=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_dogana=null;this.form.save();}
        #                                if(result.getItem('email')=='email_arr_shiprec'){SET shipsteps_arrival.form.record.@arr_tasklist.email_ship_rec=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_ship_rec=null;this.form.save();}
        #                                if(result.getItem('email')=='email_frontiera'){SET shipsteps_arrival.form.record.@arr_tasklist.email_frontiera=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_frontiera=null;this.form.save();}
        #                                if(result.getItem('email')=='email_sanimare'){SET shipsteps_arrival.form.record.@arr_tasklist.email_usma=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_usma=null;this.form.save();}
        #                                if(result.getItem('email')=='email_pilot_moor'){SET shipsteps_arrival.form.record.@arr_tasklist.email_pilot_moor=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_pilot_moor=null;this.form.save();}
        #                                if(result.getItem('email')=='email_tug'){SET shipsteps_arrival.form.record.@arr_tasklist.email_tug=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_tug=null;this.form.save();}
        #                                if(result.getItem('email')=='garbage_email'){SET shipsteps_arrival.form.record.@arr_tasklist.email_garbage=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_garbage=null;this.form.save();}
        #                                if(result.getItem('email')=='email_pfso'){SET shipsteps_arrival.form.record.@arr_tasklist.email_pfso=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_pfso=null;this.form.save();}
        #                                if(result.getItem('email')=='email_chemist'){SET shipsteps_arrival.form.record.@arr_tasklist.email_chemist=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_chemist=null;this.form.save();}
        #                                if(result.getItem('email')=='email_gpg'){SET shipsteps_arrival.form.record.@arr_tasklist.email_gpg=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_gpg=null;this.form.save();}
        #                                if(result.getItem('email')=='email_ens'){SET shipsteps_arrival.form.record.@arr_tasklist.email_ens=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_ens=null;this.form.save();}
        #                                if(result.getItem('email')=='not_rifiuti'){SET shipsteps_arrival.form.record.@arr_tasklist.email_garbage_adsp=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_garbage_adsp=null;this.form.save();}
        #                                if(result.getItem('email')=='email_ric_lps'){SET shipsteps_arrival.form.record.@arr_tasklist.email_ric_lps=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_ric_lps=null;this.form.save();}
        #                                if(result.getItem('email')=='email_integrazione_alim'){SET shipsteps_arrival.form.record.@arr_tasklist.email_integr=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_integr=null;this.form.save();}
        #                                if(result.getItem('email')=='email_pmou'){SET shipsteps_arrival.form.record.@arr_tasklist.email_pmou=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_pmou=null;this.form.save();}
        #                                if(result.getItem('email')=='email_lps_cp'){SET shipsteps_arrival.form.record.@arr_tasklist.email_lps_cp=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_lps_cp=null;this.form.save();}
        #                                if(result.getItem('email')=='email_chimico_cp'){SET shipsteps_arrival.form.record.@arr_tasklist.email_certchim_cp=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_certchim_cp=null;this.form.save();}
        #                                if(result.getItem('email')=='email_deroga_garbage'){SET shipsteps_arrival.form.record.@arr_tasklist.email_garbage_cp=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_garbage_cp=null;this.form.save();}
        #                                if(result.getItem('email')=='email_ricevutarifiuti_cp'){SET shipsteps_arrival.form.record.@arr_tasklist.email_ric_rifiuti_cp=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_ric_rifiuti_cp=null;this.form.save();}
        #                                if(result.getItem('email')=='email_tug_dep'){SET shipsteps_arrival.form.record.@arr_tasklist.email_tug_dep=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_tug_dep=null;this.form.save();}
        #                                if(result.getItem('email')=='email_tributi_cp'){SET shipsteps_arrival.form.record.@arr_tasklist.email_tributi_cp=true;this.form.save();}
        #                                else{SET shipsteps_arrival.form.record.@arr_tasklist.email_tributi_cp=null;this.form.save();}""")
    
    #@public_method
    #def test_email(self, data_invio=None,err_msg=None,tmp_code=None,**kwargs):
    #    result=Bag()
    #    if data_invio and err_msg is not None:
    #        result['email']='error'
    #        return result
    #    if data_invio is not None and err_msg==None:
    #        result['email']=tmp_code
    #        return result

    def th_top_custom(self,top):
        bar = top.bar.replaceSlots('form_delete','send_button,5,form_delete')
        bar.send_button.slotButton('Send message', hidden='^#FORM.record.send_date').dataRpc(
                    self.db.table('email.message').sendMessage, pkey='=#FORM.record.id')#,_onResult="""{this.form.reload();}""") 

class FormFromDashboard(Form):

    def th_form(self, form):
        pane = form.record
        pane.div('^.body')
    
    def th_options(self):
        return dict(showtoolbar=False)



