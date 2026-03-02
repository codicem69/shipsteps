#!/usr/bin/env pythonw
# -*- coding: UTF-8 -*-
#
#  Stampa fatture
#
#  Created by Davide Paci on 2021 03
#  Copyright (c) 2007-2021 Softwell. All rights reserved.
 
from gnr.web.batch.btcprint import BaseResourcePrint

caption = 'Stampa Cargo Manifest'

class Main(BaseResourcePrint):
    batch_title = 'Stampa Cargo Manifest'
    batch_immediate='print'
    #Con batch_immediate='print' viene immediatamente aperta la stampa alla conclusione
    html_res = 'html_res/cargo_manifest'
    #templates = 'Ranalli_st'
    page_orientation = 'H'
    #Non utilizziamo il table_script_parameters_pane perché ci limiteremo a stampare la selezione corrente

    def table_script_parameters_pane(self, pane, **kwargs):
        fb = pane.formbuilder(cols=1,border_spacing='3px')
        fb.div("--- Select the letterhead ---")
        fb.dbselect(value='^.cartaint', table='adm.htmltemplate', lbl='Carta Intestata',hasDownArrow=True,
                    selected_name='.name',validate_notnull=True)

    def pre_process(self):
        if self.batch_parameters['cartaint']:

            self.templates=self.batch_parameters['name']

