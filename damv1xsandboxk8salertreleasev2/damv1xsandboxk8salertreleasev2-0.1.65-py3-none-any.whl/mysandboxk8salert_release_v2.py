import html
import json
import sys
import textwrap

# ------- reborn packages --------------
import damv1env as env
import damv1time7 as time7
import damv1time7.mylogger as Q
import damv1time7.mydump as D
import damv1kubectl as dkube
import damv1manipulation as mpl
import damv1templateprojectk8salert as tmpltk8salert
import damv1evernoteprojectk8salert as evrnotek8salert
import damv1telegramprojectk8salert as telegk8salert
# --------------------------------------

fCls = dkube.sanbox()
fCls2 = dkube.sandbox_series_2()
tCls = tmpltk8salert.displayed
eCls = evrnotek8salert.sanbox()
eCls_u = evrnotek8salert.utils()
mCls = telegk8salert.sanbox()

def execution( _number, _nameof_msg_rpt, _namespace, _sincelast, _lst_patterns, _lst_target=[], **kwargs):
    ALLOW_PARAM= False
    bAirtableReact = False
    bShowPrintlf_process_A1 = False
    bWriteDump_process_A1 = True
    bShowCommand_for_getAllInfoPods = False
    bShowCommand_for_getLogInPodsContainer = False
    # --
    count_detected_object = 0
    url_shareable_evernotes = ''

    if int(_number)!= 0 and str(_nameof_msg_rpt).strip()!='' and str(_namespace).strip()!='' and  str(_sincelast).strip()!='' and \
        'list' in str(type(_lst_patterns)) and len(_lst_patterns)!=0 and 'list' in str(type(_lst_target)):
        ALLOW_PARAM = True

    idAirtable=''; threadNumber=0; DiffMinSecondsSilentLogger_forUpdate=0; funct_pyairtable_update, \
    bparam = mpl.kwargs().getValueAllowed(kwargs, '_argFunctAirtable_update', mpl.variable_type.method.value, None)   
    if bparam==True:
        threadNumber, \
        bparam = mpl.kwargs().getValueAllowed(kwargs,'_argThreadNumber',mpl.variable_type.int.value, 0)
        if bparam==True:
            idAirtable, \
            bparam = mpl.kwargs().getValueAllowed(kwargs,'_argIdAirtable',mpl.variable_type.str.value, None)
            if bparam==True: 
                bAirtableReact = True
                DiffMinSecondsSilentLogger_forUpdate, \
                bparam = mpl.kwargs().getValueAllowed(kwargs,'_argDiffMinSecondsSilentLogger_forUpdate',mpl.variable_type.float.value,0)

    if ALLOW_PARAM == True:
        Q.logger(time7.currentTime7(),'')
        Q.logger(time7.currentTime7(),'      [ Begin k8s_alert_release - {0} ] シミュレーション'.format(_number),  _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                                                _argThreadNumber = threadNumber, \
                                                                                                                _argIdAirtable = idAirtable)
        Q.logger(time7.currentTime7(),'        Arguments (パラメタ値):')
        Q.logger(time7.currentTime7(),'         - name of message :', _nameof_msg_rpt)
        Q.logger(time7.currentTime7(),'         - namespace :', _namespace)
        Q.logger(time7.currentTime7(),'         - sincelast :', _sincelast)
        wrap_patterns = textwrap.shorten(str(_lst_patterns), width=123, placeholder="...")
        Q.logger(time7.currentTime7(),'         - patterns :', wrap_patterns)
        wrap_target = textwrap.shorten(str(_lst_target), width=123, placeholder="...")
        Q.logger(time7.currentTime7(),'         - targets :', wrap_target)
        Q.logger(time7.currentTime7(),'      ', '.'*83)

        ## LOADING PROCESS # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        DICT_RELEASE_PodC = []
        START_DATE_TIME7 = time7.currentTime7()
        Q.logger(time7.currentTime7(),'       (1) - Loading Process ( ローディング )', _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                     _argThreadNumber = threadNumber, \
                                                                                     _argIdAirtable = idAirtable)

        # scenario 1 :: [condition used AIRTABLE] option 'type' project
        try: 
            dict_rawiPodC = []
            dict_rawiPodC = fCls.getLst_info_allPods_by_ns_v2(_namespace, bShowCommand_for_getAllInfoPods)
            dict_layer1Filter_PodC = fCls.filter_dict_iPodC_the_get_unique_dicts(dict_rawiPodC, _lst_target)
            dict_layer2Filter_PodC = mpl.listofdictionary().sorted_listOfDictionary_inChildRange(dict_layer1Filter_PodC,'containers','restart')
            DICT_RELEASE_PodC = dict_layer2Filter_PodC
        except Exception as e: Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        ## START PROCESS # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        # Result :
        # - lst_grpline     --> for report in Evernote
        # - lst_dtect_obj   --> for message in Telegran
        outstr = [];lst_grplines = [];lst_line = [];number=0;lst_dtect_obj = [];lst_sshexecparamiko_failed = [];lst_OBJECT_DETECTED = []
        if len(DICT_RELEASE_PodC) !=0 and len(_lst_patterns)!= 0:
            f = fCls.printlf_infHeadPodContainers(DICT_RELEASE_PodC, bWriteDump_process_A1, 'DUMP_PROCESS.txt', bShowPrintlf_process_A1)
            Q.logger(time7.currentTime7(),'       (2) - Start Process ( はじめる )', _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                    _argThreadNumber = threadNumber, \
                                                                                    _argIdAirtable = idAirtable)
            try:
                for idx , pod in enumerate(DICT_RELEASE_PodC):
                    pod_idx, pod_name, pod_namespace, dict_cont = fCls.trans_infParentContainer(idx,pod)
                    fCls.printlf_infParentContainer(f, bWriteDump_process_A1, bShowPrintlf_process_A1, pod_idx, pod_name, pod_namespace, dict_cont) 
                    lst_line.clear()
                    caseDeploymentName = ''
                    if len(dict_cont)!=0:
                        ## - - - - - - - - - - - - - - - - - - - -
                        ## 2023-01-18 | Collect Information
                        ## - - - - - - - - - - - - - - - - - - - -
                        lst_infCase = []
                        get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''
                        if len(dict_cont) == 1: get_bStatus_complete_sshcmd, get_exception_message_handler, lst_infCase = fCls2.getJson_infoLabel_IoName_singlePods_by_podname_ns(pod_name, pod_namespace, False)
                        else: get_bStatus_complete_sshcmd, get_exception_message_handler, lst_infCase = fCls2.getJson_infoLabel_Component_singlePods_by_podname_ns(pod_name, pod_namespace, False)

                        if len(lst_infCase)!=0:
                            caseDeploymentName = lst_infCase[0]['labels component name']

                        if get_bStatus_complete_sshcmd == False:
                            ## collected report error of process ( 1/5 ) - - - - - - - - - - - - - -
                            res = mpl.listofdictionary().dictCollectReportProcess( \
                                    f'{_namespace}::{pod_name}',\
                                    f'caseDeploymentName: {pod_name}', \
                                    get_exception_message_handler \
                                    )
                            if "'dict'" in str(type(res)):
                                if len(res)!=0:
                                    lst_sshexecparamiko_failed.append(res)
                            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                        ## - - - - - - - - - - - - - - - - - - - -
                        else:
                            for cont in dict_cont:
                                Cont_STATUS = ''
                                get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''

                                get_bStatus_complete_sshcmd, get_exception_message_handler, \
                                cont_name, cont_restart, cont_started, cont_stateStartedAt, cont_exitCode, cont_stateReason, \
                                cont_lastStateReason, cont_lastStateStartedAt, cont_lastStateFinishedAt, \
                                cont_STATUS, cont_REASON, cont_AGE = fCls.trans_infAllContainer_v2(cont)

                                if get_bStatus_complete_sshcmd == True and str(Cont_STATUS).strip() == '': Cont_STATUS = f'({str(fCls.getStatus_singlePods(pod_name,pod_namespace))})'

                                fCls.printlf_infAllContainer(f, bWriteDump_process_A1, bShowPrintlf_process_A1, \
                                cont_name, cont_restart, cont_started, cont_stateStartedAt, cont_exitCode, cont_stateReason, \
                                cont_lastStateReason, cont_lastStateStartedAt, cont_lastStateFinishedAt, \
                                cont_STATUS, cont_REASON, cont_AGE)

                                if get_bStatus_complete_sshcmd == False:
                                    ## collected report error of process ( 2/5 ) - - - - - - - - - - - - - -
                                    res = mpl.listofdictionary().dictCollectReportProcess( \
                                            f'{_namespace}::{pod_name}::{cont_name}', \
                                            f'For Loop: {cont_name}', \
                                            get_exception_message_handler \
                                            )
                                    if "'dict'" in str(type(res)):
                                        if len(res)!=0:
                                            lst_sshexecparamiko_failed.append(res)
                                    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                                else: # If status execsshparamiko completed in function trans_infAllContainer
                                    for pattern in _lst_patterns:
                                        pattern = pattern.strip()

                                        # scenario 2 :: [condition used AIRTABLE] option 'type' project

                                        get_bStatus_complete_sshcmd = False; get_exception_message_handler = ''
                                        if bAirtableReact == False:
                                            get_bStatus_complete_sshcmd, get_exception_message_handler, outstr = fCls.getLst_log_pod_by_pattern_andTarget_v2(   _sincelast, pod_name, cont_name, _namespace, pattern, _lst_target, \
                                                                                                    _argShowCommandkubectl=bShowCommand_for_getLogInPodsContainer)                                    
                                        else:
                                            get_bStatus_complete_sshcmd, get_exception_message_handler, outstr = fCls.getLst_log_pod_by_pattern_andTarget_v2(   _sincelast,pod_name, cont_name, _namespace, pattern, _lst_target, \
                                                                                                    _argDiffMinSecondsSilentLogger_forUpdate = DiffMinSecondsSilentLogger_forUpdate, \
                                                                                                    _argFunctAirtable_update = funct_pyairtable_update, _argThreadNumber=threadNumber, _argIdAirtable=idAirtable, \
                                                                                                    _argShowCommandkubectl=bShowCommand_for_getLogInPodsContainer)

                                        if get_bStatus_complete_sshcmd == False:
                                            ## collected report error of process ( 3/5 ) - - - - - - - - - - - - - -
                                            res = mpl.listofdictionary().dictCollectReportProcess( \
                                                    f'{_namespace}::{pod_name}::{cont_name}', \
                                                    f'For Loop: {pattern}' , \
                                                    get_exception_message_handler \
                                                    )
                                            if "'dict'" in str(type(res)):
                                                if len(res)!=0:
                                                    lst_sshexecparamiko_failed.append(res)
                                            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

                                        if mpl.variable_type.list.value in str(type(outstr)):
                                            if len(outstr)!=0:
                                                lenofstr = len(outstr);value_line = str(outstr[0][2:lenofstr-2])
                                                # Clean lines :
                                                value_line = eCls_u.remove_ANSI_escape_sequence(value_line)
                                                lst_line.append(tCls.tmplt_evrntLines.value.format(\
                                                    value_str_patterns = html.escape(pattern),\
                                                    value_str_sincelast = html.escape(_sincelast),\
                                                    value_str_line = html.escape(value_line)))

                                                Q.logger('\n{0}'.format(str(time7.currentTime7())),f'             Detect a ( 見つける ) {_namespace}::{pod_name} | {cont_name}', _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                                                                                                                _argThreadNumber = threadNumber, \
                                                                                                                                                                                _argIdAirtable = idAirtable)
                                                Q.logger('{0}'.format(str(time7.currentTime7())),f'             --> pattern ( パタン ): "{pattern}"', _argFunctAirtable_update = funct_pyairtable_update, \
                                                                                                                                                    _argThreadNumber = threadNumber, 
                                                                                                                                                    _argIdAirtable = idAirtable)
                                                ## - - - - - - - - - - - - - - - - - - - -
                                                ## Core of collect information
                                                ## - - - - - - - - - - - - - - - - - - - -
                                                dict_data = {}
                                                dict_data['idx'] = pod_idx
                                                dict_data['pod'] = pod_name
                                                dict_data['namespace'] = pod_namespace
                                                dict_data['case deployment name'] = caseDeploymentName
                                                dict_data['container'] = cont_name
                                                dict_data['restart'] = cont_restart
                                                dict_data['started'] = cont_started
                                                dict_data['state startedAt'] = cont_stateStartedAt
                                                dict_data['last exitCode'] = cont_exitCode
                                                dict_data['state reason'] = cont_stateReason
                                                dict_data['last state reason'] = cont_lastStateReason
                                                dict_data['last state startedAt'] = cont_lastStateStartedAt
                                                dict_data['last state finishedAt'] = cont_lastStateFinishedAt
                                                dict_data['status'] = cont_STATUS
                                                dict_data['reason'] = cont_REASON
                                                dict_data['age'] = cont_AGE
                                                lst_OBJECT_DETECTED.append(dict_data)
                                                ## - - - - - - - - - - - - - - - - - - - -

                                            else:
                                                print('\r',end='')

                                if len(lst_line)!=0:
                                    number+=1
                                    if cont_STATUS=='Running':
                                        color_status = 'Green'
                                    else: color_status = '#FF5733' # Orange Color
                                    lst_grplines.append(tCls.tmplt_evrntgrpLines.value.format(\
                                        value_str_number = html.escape(str(number)),\
                                        value_str_ns = html.escape(_namespace), \
                                        value_str_po = html.escape(pod_name), \
                                        value_str_cont = html.escape(cont_name), \
                                        value_str_color_status = html.escape(color_status), \
                                        value_str_status = html.escape(cont_STATUS), \
                                        value_str_restart = html.escape(cont_restart), \
                                        value_str_age = html.escape(cont_AGE), \
                                        value_str_lstlines = ''.join(lst_line)))
                                    Q.logger('{0}'.format(str(time7.currentTime7())),f'             ..[ Line ( ライン ) - {str(number)} : Done ( ダン ) ]',  _argFunctAirtable_update =  funct_pyairtable_update, \
                                                                                                                                                            _argThreadNumber = threadNumber, 
                                                                                                                                                            _argIdAirtable = idAirtable)
                                    line_dtect_obj = tCls.tmplt_telemsg_str_dtect_obj.value.format(\
                                            value_str_obj = mpl.telegram.escape_strparse_markdownv1(pod_name + ' | ' + cont_name), \
                                            value_obj_restart = mpl.telegram.escape_strparse_markdownv1(cont_restart), \
                                            value_obj_age = mpl.telegram.escape_strparse_markdownv1(cont_AGE))
                                    lst_dtect_obj.append(line_dtect_obj)
            except Exception as e:
              Q.logger(time7.currentTime7(),'           Error Handling ( エラー ):',str(e),_argThreadNumber = threadNumber, _argIdAirtable = idAirtable)

        Q.logger('{0}'.format(str(time7.currentTime7())),' '*100)  # netralize 'Scanning target regex'

        ## ACTION ROLLOUT RESTART DEPLOYMENT #  - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        lst_event_result_rollout_restart = []
        if len(lst_OBJECT_DETECTED)!=0:
            FULLFILENAME_DUMP_WRAPPER = 'DUMP_WRAPPER_ROLLOUT_RESTART_DEPLOYMENT.txt'
            file = D.printlf_dump_v1(True,FULLFILENAME_DUMP_WRAPPER, None, ' ')            
            D.printlf_dump_v1(True,'', file,' ')
            D.printlf_dump_v1(True,'', file,' ')
            material_execute = {x['case deployment name']:x for x in lst_OBJECT_DETECTED}.values()  # --> MAKE UNIQUE OF LIST DICTIONARY

            status_wrapper_completed = False; lst_failed = []
            for deployment in list(material_execute):
                status_wrapper_completed, get_exception_message_handler, res_rolloutrestart, res_slUp, res_slDown, lst_failed, \
                event_podname_scaledUp, event_podname_scaledDown= fCls2.execute_wrapperRollout_restartDeployment(deployment['namespace'],deployment['case deployment name'], file)
                D.printlf_dump_v1(True,'', file,' '*6,'- Status completed wrapper-rollout-restart-deployment:', str(status_wrapper_completed))
                D.printlf_dump_v1(True,'', file,' '*6,'- Deployment:', deployment['case deployment name'])
                D.printlf_dump_v1(True,'', file,' ')
                D.printlf_dump_v1(True,'', file,' ')

                row_result = {}
                row_result['namespace'] = str(deployment['namespace']).strip()
                row_result['deployment'] = str(deployment['case deployment name']).strip()
                row_result['response rollout restart'] = str(res_rolloutrestart)
                row_result['pod scaled up name'] = str(event_podname_scaledUp).strip()
                row_result['pod scaled up response'] = str(res_slUp)
                row_result['pod scaled down name'] = str(event_podname_scaledDown).strip()
                row_result['pod scaled down response'] = str(res_slDown)

                lst_event_result_rollout_restart.append(row_result)

                if len(lst_failed)!=0:
                    ## collected report error of process ( 4/5 ) - - - - - - - - - - - - - -
                    res = mpl.listofdictionary().dictCollectReportProcess( \
                            f'{deployment["namespace"]}::{deployment["case deployment name"]}', \
                            f'For Loop: ACTION ROLLOUT RESTART DEPLOYMENT ( ssh exec )'  , \
                            'get list filed in ssh connection', \
                            lst_failed \
                            )
                    if "'dict'" in str(type(res)):
                        if len(res)!=0:
                            lst_sshexecparamiko_failed.append(res)
                    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                if status_wrapper_completed == False:
                    ## collected report error of process ( 5/5 ) - - - - - - - - - - - - - -
                    res = mpl.listofdictionary().dictCollectReportProcess( \
                            f'{deployment["namespace"]}::{deployment["case deployment name"]}', \
                            f'For Loop: ACTION ROLLOUT RESTART DEPLOYMENT ( wrapper )' , \
                            get_exception_message_handler \
                            )
                    if "'dict'" in str(type(res)):
                        if len(res)!=0:
                            lst_sshexecparamiko_failed.append(res)
                    ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if len(lst_event_result_rollout_restart)!=0:
            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            ## Level 1
            namespace_deployment = list({dictionary['namespace']: dictionary for dictionary in lst_event_result_rollout_restart}.values())[0]['namespace']
            lst_event_result_rollout_restart_filter_successful = list(filter(lambda x: x['response rollout restart'] == 'True', lst_event_result_rollout_restart))
            lst_event_result_rollout_restart_filter_fail = list(filter(lambda x: x['response rollout restart'] == 'False', lst_event_result_rollout_restart))
            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            ## Level 2
            lst_deployment_rollout_restart_success = []
            if len(lst_event_result_rollout_restart_filter_successful)!=0:
                for event in lst_event_result_rollout_restart_filter_successful:
                    line_deploy_restart_successful = tCls.tmplt_telemsg_str_restart_deploy_succeed.value.format(\
                        value_str_deploy =  mpl.telegram.escape_strparse_markdownv1(event['deployment']), \
                        value_pods_scaledup =  mpl.telegram.escape_strparse_markdownv1(event['pod scaled up name'])\
                        )
                    lst_deployment_rollout_restart_success.append(line_deploy_restart_successful)
                lst_event_result_rollout_restart_filter_successful.clear()

            lst_deployment_rollout_restart_fail = []
            if len(lst_event_result_rollout_restart_filter_fail)!=0:
                for event in lst_event_result_rollout_restart_filter_fail:
                    line_deploy_restart_fail = tCls.tmplt_telemsg_str_restart_deploy_failed.value.format(\
                        value_str_deploy =  mpl.telegram.escape_strparse_markdownv1(event['deployment'])
                        )
                    lst_deployment_rollout_restart_fail.append(line_deploy_restart_fail)
                lst_event_result_rollout_restart_filter_fail.clear()
            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


        ## REPORT OF THE PROCESS ABOVE #  - -- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Q.logger(time7.currentTime7())
        Q.logger(time7.currentTime7(), ' '*8,' *'*25)
        if len(lst_sshexecparamiko_failed)!=0: Q.logger(time7.currentTime7(), ' '*9, f'Check length lst_sshexecparamiko_failed : {str(len(lst_sshexecparamiko_failed))} .')
        else: Q.logger(time7.currentTime7(), ' '*9, 'No data availbale for the lst_sshexecparamiko_failed.')
        Q.logger(time7.currentTime7(), ' '*8,' *'*25)
        Q.logger(time7.currentTime7())
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

        ## EVERNOTE INTEGRATING #  インテグレーテット - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        evrnt_urlshareable = None
        if len(lst_grplines) != 0:
            nameof_msg_rpt = _nameof_msg_rpt.strip()
            contexid = str(time7.generate_uuids_byTime7())
            Q.logger('{0}'.format(str(time7.currentTime7())),'       (3) - Evernote integrating ( レポート )')
            ## new revision 20 Januari 2023  - - - - - - - - - - - - - - - - - - - - - 
            tmplt_line_another1 = ''
            if len(lst_sshexecparamiko_failed)!=0:
                tmplt_line_another1 = tCls.tmplt_evrntgrpAnother1.value.format(\
                    value_str_another1_title = 'Error of the process above ( {0} objects )'.format(str(len(lst_sshexecparamiko_failed))), \
                    value_str_another1_text = lst_sshexecparamiko_failed
                    )
                lst_sshexecparamiko_failed.clear()
            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            try: evrnt_urlshareable = eCls.evernote_generate_report_v2(contexid, nameof_msg_rpt, lst_grplines, tCls.tmplt_evrntwrapper_v2.value, str(tmplt_line_another1).strip())
            # try: evrnt_urlshareable = eCls.evernote_generate_report(contexid, nameof_msg_rpt, lst_grplines, tCls.tmplt_evrntwrapper.value)
            # try: evrnt_urlshareable = eCls.evernote_generate_report(contexid, nameof_msg_rpt, lst_grplines, tCls.tmplt_evrntwrapper.value, \
            #                             _argShowErrorExplain=True)
            except Exception as e: Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))

        ## TELEGRAM INTEGRATING #  インテグレーテット - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        if len(lst_dtect_obj)!=0:
            Q.logger(time7.currentTime7(),'       (4) - Telegram integrating ( メッセージ )')
            dtect_obj = '\n  \-\| '.join(lst_dtect_obj)
            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            ## Level 3
            count_deployment_success_restart = 0
            lines_deploymeny_success_restart = mpl.telegram.escape_strparse_markdownv1(str(''))
            if len(lst_deployment_rollout_restart_success)!=0:
                count_deployment_success_restart = len(lst_deployment_rollout_restart_success)
                lines_deploymeny_success_restart = '\n  \=\| '.join(lst_deployment_rollout_restart_success)

            count_deployment_fail_restart = 0
            lines_deploymeny_fail_restart = mpl.telegram.escape_strparse_markdownv1(str(''))
            if len(lst_deployment_rollout_restart_fail)!=0:
                count_deployment_fail_restart = len(lst_deployment_rollout_restart_fail)
                lines_deploymeny_fail_restart = '\n  \=\| '.join(lst_deployment_rollout_restart_fail)
            ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
            ## Level 4
            wrapper_deploy_success = tCls.tmplt_telemsg_deploy_succeed.value.format(\
                value_str_count_deployment_success_restart = mpl.telegram.escape_strparse_markdownv1(str(count_deployment_success_restart)),\
                value_str_deployment_ns = mpl.telegram.escape_strparse_markdownv1(str(namespace_deployment)),\
                value_str_deployment_rollout_restart_succeed = lines_deploymeny_success_restart
                )

            wrapper_deploy_success_raw = tCls.tmplt_telemsg_deploy_succeed.value.format(\
                value_str_count_deployment_success_restart = mpl.telegram.escape_strparse_markdownv1(str(count_deployment_success_restart)),\
                value_str_deployment_ns = mpl.telegram.escape_strparse_markdownv1(str(namespace_deployment)),\
                value_str_deployment_rollout_restart_succeed = '{value_str_deployment_rollout_restart_succeed}'
                )

            wrapper_deploy_failed = tCls.tmplt_telemsg_deploy_failed.value.format(\
                value_str_count_deployment_fail_restart = mpl.telegram.escape_strparse_markdownv1(str(count_deployment_fail_restart)),\
                value_str_deployment_ns = mpl.telegram.escape_strparse_markdownv1(str(namespace_deployment)),\
                value_str_deployment_rollout_restart_failed = lines_deploymeny_fail_restart
                )

            wrapper_deploy_failed_raw = tCls.tmplt_telemsg_deploy_failed.value.format(\
                value_str_count_deployment_fail_restart = mpl.telegram.escape_strparse_markdownv1(str(count_deployment_fail_restart)),\
                value_str_deployment_ns = mpl.telegram.escape_strparse_markdownv1(str(namespace_deployment)),\
                value_str_deployment_rollout_restart_failed = '{value_str_deployment_rollout_restart_failed}'
                )

            label_limit_tele = '[Entities too long / 4096 character]'
            length_wrapper_raw = len(wrapper_raw)
            length_dtect_obj = len(dtect_obj)
            length_wrapper_deploy_success = len(wrapper_deploy_success)
            length_wrapper_deploy_failed = len(wrapper_deploy_failed)

            wrapper_raw = mpl.telegram.escape_strparse_markdownv1(str(''))
            wrapper_raw = tCls.tmplt_telemsg_v3.value.format(\
                value_str_messagename = mpl.telegram.escape_strparse_markdownv1(nameof_msg_rpt), \
                value_str_contextid = mpl.telegram.escape_strparse_markdownv1(contexid), \
                value_str_StartDateTime7 = mpl.telegram.escape_strparse_markdownv1(START_DATE_TIME7), \
                value_str_count_dtect_obj = mpl.telegram.escape_strparse_markdownv1(str(len(lst_dtect_obj))), \
                value_str_ns = mpl.telegram.escape_strparse_markdownv1(namespace_deployment), \
                value_str_dtect_obj = '{value_str_dtect_obj}', \
                value_deploy_succeed = '{value_deploy_succeed}', \
                value_deploy_failed = '{value_deploy_failed}', \
                value_str_url_shareable = evrnt_urlshareable \
                )

            telemsg = wrapper_raw.format(\
                value_str_dtect_obj = dtect_obj if (length_wrapper_raw + length_dtect_obj) < 4096 else label_limit_tele, \
                value_deploy_succeed = '' if count_deployment_success_restart == 0 else wrapper_deploy_success if (length_wrapper_raw + length_dtect_obj + length_wrapper_deploy_success) < 4096 else wrapper_deploy_success_raw.format(value_str_deployment_rollout_restart_succeed = label_limit_tele), \
                value_deploy_failed = '' if count_deployment_fail_restart == 0 else wrapper_deploy_failed if (length_wrapper_raw + length_dtect_obj + length_wrapper_deploy_success + length_wrapper_deploy_failed) < 4096 else wrapper_deploy_failed_raw.format(value_str_deployment_rollout_restart_failed = label_limit_tele)
                )

            Q.logger(time7.currentTime7(),'             Sending message to Telegram ( メッセージを送る )')
            mCls.sendmessage_telegram(telemsg)

        ## ERASE OLD REPORT #  イレーズ レポート - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
        ## - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        reports = None
        try: reports = eCls.evernote_erase_old_notes()
        except Exception as e: Q.logger(time7.currentTime7(),'Error Handling ( エラー ):',str(e))
        if str(reports)!= 'None' and str(reports).strip()!='':
            Q.logger(time7.currentTime7(),' '*15 ,reports)


        # NOTES :
        # lst_dtect_obj is same count for lst_OBJECT_DETECTED
        # decribe of lst_dtect_obj --> with template line of point
        # describe of lst_OBJECT_DETECTED --> with list information point
        count_detected_object = int(len(lst_dtect_obj))
        url_shareable_evernotes = str(evrnt_urlshareable)
    return count_detected_object, url_shareable_evernotes